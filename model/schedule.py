""" Meeting schedule and booking models (same pattern as model/user.py)

Meetings are not typed in by hand: sync_meetings() pulls the weekly schedule from the center's own meeting
calendar on powayrecoverycenter.org (an EventON calendar listing every program that meets there) and
upserts it here, so this calendar changes when the center changes theirs.
Bookings are one user's reserved spots (one or more) at one meeting on one calendar date.
"""
import html
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import func, inspect, text
from sqlalchemy.exc import IntegrityError

from __init__ import app, db


TIMEZONE = ZoneInfo('America/Los_Angeles')
DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']  # feed: 0 = Sunday

# Meeting Guide type codes used by the feed
TYPE_LABELS = {
    'O': 'Open', 'C': 'Closed', 'D': 'Discussion', 'SP': 'Speaker', 'ST': 'Step Study',
    'B': 'Big Book', 'BE': 'Newcomer', 'LIT': 'Literature', 'TR': 'Tradition Study',
    'M': 'Men', 'W': 'Women', 'SEN': 'Seniors', 'Y': 'Young People', 'LGBTQ': 'LGBTQ',
    'ONL': 'Online', 'TC': 'Location Temporarily Closed', 'X': 'Wheelchair Access',
    'MED': 'Meditation', 'CF': 'Child-Friendly', 'ABSI': 'As Bill Sees It', 'A': 'Secular',
}
ATTENDANCE_LABELS = {'in_person': 'In person', 'hybrid': 'In person + Zoom', 'online': 'Online'}

# Programs that meet at the center (slugs match model/program.py and the site's /groups/<slug> pages)
PROGRAM_NAMES = {
    'aa': 'AA', 'al-anon': 'Al-Anon', 'alateen': 'Alateen', 'aca': 'ACA',
    'na': 'NA', 'ca': 'CA', 'ga': 'GA', 'sa': 'SA',
}
# How a meeting's title names its program; anything else at the center is an AA meeting
PROGRAM_PATTERNS = [
    ('al-anon', r'\bal-?anon\b'), ('alateen', r'\balateen\b'), ('aca', r'\baca\b|adult children'),
    ('na', r'\bna\b|narcotics'), ('ca', r'\bca\b|cocaine'), ('ga', r'\bga\b|gam-anon|gamblers'),
    ('sa', r'\bsa\b|sexaholics'),
]
# Kinds of meeting read from the title (stored as labels)
KIND_PATTERNS = [
    ('Open', r'\bopen\b'), ('Closed', r'\bclosed\b'), ('Women', r'\bwom[ae]n|\bladies\b'),
    ('Men', r'\bm[ae]ns?\b'), ('Speaker', r'\bspeaker'), ('Discussion', r'\bdiscussion'),
    ('Study', r'\bstudy\b|12\s*[x×]\s*12|big book'), ('Seniors', r'\bseniors?\b'),
]


def today():
    """ Today's date in Poway, so the calendar rolls over at local midnight """
    return datetime.now(TIMEZONE).date()


def feed_day(d):
    """ Python weekday (Monday = 0) to feed day (Sunday = 0) """
    return (d.weekday() + 1) % 7


class Meeting(db.Model):
    """
    Meeting Model: one weekly meeting at the center.

    Attributes:
        id (Column): Primary key.
        _source_id (Column): The meeting's id in the source feed, used to upsert on each sync.
        _name, _day (0 = Sunday), _start, _end ("HH:MM"), _location, _types (comma codes),
        _attendance, _notes, _url (Column): Copied from the feed.
        _program (Column): Which recovery program runs it (aa, al-anon, na, ga, sa...; see PROGRAM_NAMES).
        _capacity (Column): Spots per session; admins can change it, syncs never overwrite it.
        _active (Column): False once the meeting disappears from the feed (bookings are kept).
        updated_at (Column): Last sync that touched this meeting.
    """
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    _source_id = db.Column(db.String(64), unique=True, nullable=False)
    _name = db.Column(db.String(255), nullable=False)
    _day = db.Column(db.Integer, nullable=False)
    _start = db.Column(db.String(5), nullable=False)
    _end = db.Column(db.String(5), nullable=True)
    _location = db.Column(db.String(255), nullable=True)
    _types = db.Column(db.String(255), nullable=True)
    _attendance = db.Column(db.String(32), nullable=True)
    _program = db.Column(db.String(16), nullable=True)
    _notes = db.Column(db.Text, nullable=True)
    _url = db.Column(db.String(512), nullable=True)
    _capacity = db.Column(db.Integer, nullable=False)
    _active = db.Column(db.Boolean, default=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    bookings = db.relationship('Booking', backref='meeting', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def day(self):
        return self._day

    @property
    def capacity(self):
        return self._capacity

    @property
    def active(self):
        return self._active

    def end_time(self):
        """ The feed often leaves end time blank; assume a one hour meeting """
        if self._end:
            return self._end
        hour, minute = map(int, self._start.split(':'))
        return f"{(hour + 1) % 24:02d}:{minute:02d}"

    def starts_at(self, on_date):
        hour, minute = map(int, self._start.split(':'))
        return datetime(on_date.year, on_date.month, on_date.day, hour, minute, tzinfo=TIMEZONE)

    def has_started(self, on_date):
        return datetime.now(TIMEZONE) >= self.starts_at(on_date)

    def runs_on(self, on_date):
        return self._active and self._day == feed_day(on_date)

    def set_capacity(self, capacity):
        self._capacity = capacity
        db.session.commit()
        return self

    def read(self):
        codes = [c for c in (self._types or '').split(',') if c]
        return {
            "id": self.id,
            "name": self._name,
            "day": self._day,
            "day_name": DAY_NAMES[self._day],
            "start": self._start,
            "end": self.end_time(),
            "start_formatted": format_time(self._start),
            "end_formatted": format_time(self.end_time()),
            "location": self._location or "",
            "types": [TYPE_LABELS.get(c, c) for c in codes],
            "attendance": ATTENDANCE_LABELS.get(self._attendance, ""),
            "program": self._program or "aa",
            "program_name": PROGRAM_NAMES.get(self._program or "aa", ""),
            "notes": self._notes or "",
            "url": self._url or "",
            "capacity": self._capacity,
            "active": self._active,
        }

    def booked_spots(self, on_date, exclude_user=None):
        """ Spots reserved for this meeting on one date (optionally not counting one user's) """
        query = db.session.query(func.coalesce(func.sum(Booking._spots), 0)) \
            .filter(Booking._meeting_id == self.id, Booking._date == on_date)
        if exclude_user is not None:
            query = query.filter(Booking._user_id != exclude_user.id)
        return query.scalar()

    def read_session(self, on_date, user=None):
        """ This meeting on one date, with live spot counts """
        booked = self.booked_spots(on_date)
        mine = self.bookings.filter_by(_date=on_date, _user_id=user.id).first() if user else None
        data = self.read()
        data.update({
            "date": on_date.isoformat(),
            "booked": booked,
            "spots_left": max(0, self._capacity - booked),
            "started": self.has_started(on_date),
            "booked_by_me": mine is not None,
            "my_spots": mine.spots if mine else 0,
            "max_spots_per_user": app.config['SCHEDULE_MAX_SPOTS_PER_USER'],
        })
        return data


class Booking(db.Model):
    """
    Booking Model: one user's reservation for one session.

    Attributes:
        id (Column): Primary key.
        _user_id (Column): The user who reserved.
        _meeting_id (Column): The meeting.
        _date (Column): The calendar date of that meeting's session.
        _spots (Column): How many spots this user reserved (e.g. bringing a family member).
        created_at (Column): When the spot was reserved.
    """
    __tablename__ = 'bookings'
    __table_args__ = (db.UniqueConstraint('_user_id', '_meeting_id', '_date', name='unique_user_session'),)

    id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    _meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id', ondelete='CASCADE'), nullable=False)
    _date = db.Column(db.Date, nullable=False)
    _spots = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Deleting a user (admin DELETE /api/user) also removes their bookings
    user = db.relationship('User', backref=db.backref('bookings', cascade='all, delete-orphan', lazy='dynamic'))

    def __init__(self, user, meeting, on_date, spots=1):
        self._user_id = user.id
        self._meeting_id = meeting.id
        self._date = on_date
        self._spots = spots

    @property
    def date(self):
        return self._date

    @property
    def spots(self):
        return self._spots

    def set_spots(self, spots):
        self._spots = spots
        db.session.commit()
        return self

    def create(self):
        """ Add the booking; returns None if this user already has this session """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self, user=None):
        data = self.meeting.read_session(self._date, user)
        data["booking_id"] = self.id
        data["reserved_at"] = self.created_at.isoformat() if self.created_at else None
        return data

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def format_time(hhmm):
    hour, minute = map(int, hhmm.split(':'))
    return f"{hour % 12 or 12}:{minute:02d} {'AM' if hour < 12 else 'PM'}"


def parse_date(value):
    """ "YYYY-MM-DD" to a date, or None """
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


# ---- Sync from the live meeting feed ----

_sync_lock = threading.Lock()
sync_status = {"last_synced": None, "last_attempt": 0.0, "error": None, "count": 0}


def _post_json(url, fields):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(fields).encode(),
                                 headers={"User-Agent": "PowayRecoveryCenterAPI/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))


def _get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PowayRecoveryCenterAPI/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))


def _text(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fragment or ''))).strip()


def fetch_center_calendar():
    """
    The center's meetings as weekly items: one per meeting per weekday, from the next two weeks of
    the powayrecoverycenter.org EventON calendar (two weeks so a meeting cancelled for one week isn't lost).
    Each event's page content holds its room and Zoom link.
    """
    site = app.config['SCHEDULE_SITE_URL']
    start = datetime.combine(today() - timedelta(days=today().weekday()), datetime.min.time(), TIMEZONE)
    end = start + timedelta(days=14)
    sc = {'calendar_type': 'weekly', 'focus_start_date_range': int(start.timestamp()),
          'focus_end_date_range': int(end.timestamp()) - 1, 'event_count': 0, 'hide_past': 'no',
          'event_past_future': 'all', 'number_of_months': 1, 'event_order': 'ASC', 'sort_by': 'sort_date', 'lang': 'L1'}
    fields = {'action': 'eventon_init_load', **{f'cals[prc][sc][{k}]': v for k, v in sc.items()}}
    occurrences = _post_json(f'{site}/?evo-ajax=eventon_init_load', fields)['cals']['prc']['json']
    details = {e['id']: e for e in _get_json(f'{site}/wp-json/wp/v2/ajde_events?per_page=100')}

    items = {}
    for occ in occurrences:
        begins = datetime.fromtimestamp(int(occ['event_start_unix']), TIMEZONE)
        ends = datetime.fromtimestamp(int(occ['event_end_unix']), TIMEZONE)
        event_id = int(occ['ID'])
        key = f"prc-{event_id}-{feed_day(begins.date())}"
        if key in items:
            continue
        info = details.get(event_id, {})
        content = (info.get('content') or {}).get('rendered', '')
        room = _text(content)
        zoom = re.search(r'href="(https://[^"]*zoom\.us/[^"]+)"', content)
        items[key] = {
            'id': key,
            'name': _text(occ.get('event_title')),
            'day': feed_day(begins.date()),
            'start': begins.strftime('%H:%M'),
            'end': ends.strftime('%H:%M') if ends > begins else None,
            'room': room,
            'zoom': html.unescape(zoom.group(1)) if zoom else None,
            'url': info.get('link'),
        }
    return list(items.values())


def program_of(title):
    lowered = title.lower()
    return next((slug for slug, pattern in PROGRAM_PATTERNS if re.search(pattern, lowered)), 'aa')


def kinds_of(title):
    lowered = title.lower()
    return [label for label, pattern in KIND_PATTERNS if re.search(pattern, lowered)]


def location_of(room):
    """ "Suite 11 / Zoom Info*" -> "Poway Recovery Center, Suite 11" (Zoom details go in the notes) """
    place = re.split(r'zoom', room, flags=re.IGNORECASE)[0].strip(' /*-')
    return f"Poway Recovery Center, {place}" if place else "Poway Recovery Center"


def sync_meetings():
    """
    Pull the center's calendar and upsert its meetings. Meetings no longer listed are marked
    inactive (their bookings are kept). If the calendar can't be reached, the last synced schedule stays.
    Returns sync_status.
    """
    with _sync_lock, app.app_context():
        sync_status["last_attempt"] = time.time()
        try:
            items = fetch_center_calendar()
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError) as error:
            sync_status["error"] = f"Could not reach the center's meeting calendar: {error}"
            app.logger.error(sync_status["error"])
            return sync_status

        seen = set()
        for item in items:
            seen.add(item['id'])
            meeting = Meeting.query.filter_by(_source_id=item['id']).first()
            if meeting is None:
                meeting = Meeting(_source_id=item['id'], _capacity=app.config['SCHEDULE_DEFAULT_CAPACITY'])
                db.session.add(meeting)
            meeting._name = item['name']
            meeting._day = item['day']
            meeting._start = item['start']
            meeting._end = item['end']
            meeting._location = location_of(item['room'])
            meeting._types = ','.join(kinds_of(item['name']))
            meeting._program = program_of(item['name'])
            meeting._attendance = 'hybrid' if item['zoom'] or 'zoom' in item['room'].lower() else 'in_person'
            meeting._notes = f"Zoom: {item['zoom']}" if item['zoom'] else ''
            meeting._url = item['url']
            meeting._active = True
            meeting.updated_at = datetime.now(timezone.utc)
        for meeting in Meeting.query.filter(Meeting._active.is_(True)).all():
            if meeting._source_id not in seen:
                meeting._active = False
        db.session.commit()

        sync_status.update(last_synced=datetime.now(timezone.utc).isoformat(), error=None, count=len(items))
        return sync_status


def sync_if_stale():
    """ Re-sync when the last attempt is older than SCHEDULE_REFRESH_SECONDS (called on schedule reads) """
    if time.time() - sync_status["last_attempt"] >= app.config['SCHEDULE_REFRESH_SECONDS'] and not _sync_lock.locked():
        sync_meetings()


def initSchedules():
    """ Create the meeting/booking tables and load the current schedule """
    with app.app_context():
        db.create_all()
        # Databases made before bookings could hold several spots: add the column (create_all won't)
        if '_spots' not in [c['name'] for c in inspect(db.engine).get_columns('bookings')]:
            with db.engine.begin() as conn:
                conn.execute(text('ALTER TABLE bookings ADD COLUMN _spots INTEGER NOT NULL DEFAULT 1'))
        # Databases made before meetings knew their program
        if '_program' not in [c['name'] for c in inspect(db.engine).get_columns('meetings')]:
            with db.engine.begin() as conn:
                conn.execute(text('ALTER TABLE meetings ADD COLUMN _program VARCHAR(16)'))
    sync_meetings()


def booking_window_end():
    return today() + timedelta(days=app.config['SCHEDULE_BOOKING_DAYS'])

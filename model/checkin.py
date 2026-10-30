""" Recovery tracker check-in model (same pattern as model/schedule.py Booking)

One row per user per week: 1-5 ratings for mood, sleep, cravings and stress,
the recovery actions they took that week, and an optional note.
A week that drops dangerously low is flagged (alerted) so admins/counselors see it on GET /api/checkins/alerts.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from __init__ import app, db


TIMEZONE = ZoneInfo('America/Los_Angeles')
MAX_NOTE_CHARS = 280

# key: (how a very hard week reads, whether a high rating is the harder one)
METRICS = {
    'mood': ("your mood was very low", False),
    'sleep': ("sleep was very poor", False),
    'cravings': ("cravings were overwhelming", True),
    'stress': ("stress was very high", True),
}
# Recovery actions a user can tick for the week (labels live in js/recovery-tracker.js)
ACTIONS = ('meeting', 'support', 'exercise', 'selfcare')
# Alert when this many metrics sit at the hardest end, or the week's average wellness (1-5) is this low or lower
ALERT_HARDEST_COUNT = 2
ALERT_AVERAGE_WELLNESS = 1.75


def current_week():
    """ Monday of this week at the center, as a date """
    today = datetime.now(TIMEZONE).date()
    return today - timedelta(days=today.weekday())


class CheckIn(db.Model):
    """
    CheckIn Model: one user's ratings for one week.

    Attributes:
        id (Column): Primary key.
        _user_id (Column): The user who checked in.
        _week (Column): Monday of the week (America/Los_Angeles).
        _mood, _sleep, _cravings, _stress (Column): 1-5 ratings (high cravings or stress is the harder end).
        _actions (Column): Comma separated ACTIONS keys done that week.
        _note (Column): Optional note, up to MAX_NOTE_CHARS.
        _alerted (Column): Set once the week dropped low enough to alert counselors; stays set for that week.
        created_at / updated_at (Column): When it was first saved and last changed.
    """
    __tablename__ = 'checkins'
    __table_args__ = (db.UniqueConstraint('_user_id', '_week', name='unique_user_week'),)

    id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    _week = db.Column(db.Date, nullable=False)
    _mood = db.Column(db.Integer, nullable=False)
    _sleep = db.Column(db.Integer, nullable=False)
    _cravings = db.Column(db.Integer, nullable=False)
    _stress = db.Column(db.Integer, nullable=False)
    _actions = db.Column(db.String(255), default='', nullable=False)
    _note = db.Column(db.String(MAX_NOTE_CHARS), default='', nullable=False)
    _alerted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Deleting a user (admin DELETE /api/user) also removes their check-ins
    user = db.relationship('User', backref=db.backref('checkins', cascade='all, delete-orphan', lazy='dynamic'))

    def __init__(self, user, week):
        self._user_id = user.id
        self._week = week

    @property
    def week(self):
        return self._week

    @property
    def alerted(self):
        return self._alerted

    @staticmethod
    def validate(body):
        """ Returns (ratings, actions, note, error) from a request body """
        ratings = {}
        for key in METRICS:
            value = body.get(key)
            if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
                return None, None, None, f"Please rate {key} from 1 to 5"
            ratings[key] = value
        actions = body.get('actions') or []
        if not isinstance(actions, list) or any(a not in ACTIONS for a in actions):
            return None, None, None, "Unknown recovery action"
        note = str(body.get('note') or '').strip()
        if len(note) > MAX_NOTE_CHARS:
            return None, None, None, f"Notes can be up to {MAX_NOTE_CHARS} characters"
        return ratings, [a for a in ACTIONS if a in actions], note, None

    def save(self, ratings, actions, note):
        """ Set this week's answers; returns the concerns if the week is low enough to alert counselors """
        for key, value in ratings.items():
            setattr(self, '_' + key, value)
        self._actions = ','.join(actions)
        self._note = note
        self.updated_at = datetime.now(timezone.utc)
        concerns = self.concerns()
        if concerns:
            self._alerted = True
        if self.id is None:
            db.session.add(self)
        db.session.commit()
        return concerns

    def concerns(self):
        """ Why this week is alarming, or [] when it isn't """
        wellness = {key: 6 - getattr(self, '_' + key) if invert else getattr(self, '_' + key)
                    for key, (_, invert) in METRICS.items()}
        hardest = [METRICS[key][0] for key, value in wellness.items() if value == 1]
        if len(hardest) >= ALERT_HARDEST_COUNT or sum(wellness.values()) / len(wellness) <= ALERT_AVERAGE_WELLNESS:
            return hardest or ["every area was very hard"]
        return []

    def read(self):
        return {
            "id": self.id,
            "week": self._week.isoformat(),
            **{key: getattr(self, '_' + key) for key in METRICS},
            "actions": [a for a in (self._actions or '').split(',') if a],
            "note": self._note or "",
            "alerted": self._alerted,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def read_alert(self):
        """ What counselors see: the scores plus who to reach out to """
        data = self.read()
        data.update(name=self.user.name, uid=self.user.uid, email=self.user.email or "", phone=self.user.phone or "",
                    concerns=self.concerns())
        return data


def initCheckIns():
    """ Create the checkins table """
    with app.app_context():
        db.create_all()

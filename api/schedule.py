""" Schedule API: meeting calendar and spot booking (same pattern as api/user.py)

All schedule data lives here; the frontend calendar only calls these endpoints.
"""
from datetime import timedelta

from flask import Blueprint, request, current_app, g, jsonify
from flask_restful import Api, Resource

from __init__ import db
from api.jwt_authorize import token_required, current_user_or_none
from model.schedule import (Meeting, Booking, sync_meetings, sync_if_stale, sync_status,
                            today, parse_date, booking_window_end, DAY_NAMES)


schedule_api = Blueprint('schedule_api', __name__, url_prefix='/api/schedule')
api = Api(schedule_api)

MAX_DAYS = 42  # Six weeks covers a full month grid


def source_info():
    return {
        "source": current_app.config['SCHEDULE_SOURCE_NAME'],
        "source_url": current_app.config['SCHEDULE_SOURCE_URL'],
        "last_synced": sync_status["last_synced"],
        "sync_error": sync_status["error"],
    }


def find_session(body):
    """ Returns (meeting, date, error response) for a {meeting_id, date} request body """
    meeting = db.session.get(Meeting, body.get('meeting_id') or 0)
    on_date = parse_date(body.get('date'))
    if meeting is None:
        return None, None, ({"message": "Meeting not found"}, 404)
    if on_date is None:
        return None, None, ({"message": "date must be YYYY-MM-DD"}, 400)
    if not meeting.runs_on(on_date):
        return None, None, ({"message": f"{meeting.read()['name']} does not meet on {DAY_NAMES[(on_date.weekday() + 1) % 7]}s"}, 400)
    return meeting, on_date, None


def check_spots(meeting, on_date, body):
    """ Returns (spots, error response) for a reservation of body['spots'] (default 1) spots """
    if on_date > booking_window_end():
        return None, ({"message": f"Bookings open {current_app.config['SCHEDULE_BOOKING_DAYS']} days ahead"}, 400)
    if on_date < today():
        return None, ({"message": "That date has already passed"}, 400)
    if meeting.has_started(on_date):
        return None, ({"message": "This meeting has already started"}, 400)
    limit = current_app.config['SCHEDULE_MAX_SPOTS_PER_USER']
    try:
        spots = int(body.get('spots', 1))
    except (TypeError, ValueError):
        return None, ({"message": "spots must be a number"}, 400)
    if not 1 <= spots <= limit:
        return None, ({"message": f"You can reserve 1 to {limit} spots per meeting"}, 400)
    left = meeting.capacity - meeting.booked_spots(on_date, exclude_user=g.current_user)
    if spots > left:
        return None, ({"message": "This meeting is full" if left <= 0 else f"Only {left} spot{'s' if left != 1 else ''} left"}, 409)
    return spots, None


class ScheduleAPI:
    class _Calendar(Resource):
        def get(self):
            """
            Sessions for each day from ?start=YYYY-MM-DD (default today) for ?days=N (default 7, max 42).
            Logged-in users also see which sessions they have booked.
            """
            sync_if_stale()
            start = parse_date(request.args.get('start')) if request.args.get('start') else today()
            if start is None:
                return {"message": "start must be YYYY-MM-DD"}, 400
            try:
                days = min(MAX_DAYS, max(1, int(request.args.get('days', 7))))
            except ValueError:
                return {"message": "days must be a number"}, 400

            user = current_user_or_none()
            meetings = Meeting.query.filter(Meeting._active.is_(True)).order_by(Meeting._start, Meeting._name).all()
            window_end = booking_window_end()
            calendar = []
            for offset in range(days):
                on_date = start + timedelta(days=offset)
                calendar.append({
                    "date": on_date.isoformat(),
                    "day_name": DAY_NAMES[(on_date.weekday() + 1) % 7],
                    "is_today": on_date == today(),
                    "is_past": on_date < today(),
                    "bookable": today() <= on_date <= window_end,
                    "sessions": [m.read_session(on_date, user) for m in meetings if m.runs_on(on_date)],
                })
            return jsonify({
                "today": today().isoformat(),
                "booking_window_end": window_end.isoformat(),
                "logged_in": user is not None,
                "days": calendar,
                **source_info(),
            })

    class _Meetings(Resource):
        def get(self):
            """ The weekly recurring schedule """
            sync_if_stale()
            meetings = Meeting.query.filter(Meeting._active.is_(True)).order_by(Meeting._day, Meeting._start).all()
            return jsonify({"meetings": [m.read() for m in meetings], **source_info()})

        @token_required("Admin")
        def put(self):
            """ Admin only: set spots per session {id, capacity} """
            body = request.get_json(silent=True) or {}
            meeting = db.session.get(Meeting, body.get('id') or 0)
            if meeting is None:
                return {"message": "Meeting not found"}, 404
            try:
                capacity = int(body.get('capacity'))
            except (TypeError, ValueError):
                return {"message": "capacity must be a number"}, 400
            if not 1 <= capacity <= 500:
                return {"message": "capacity must be between 1 and 500"}, 400
            return jsonify(meeting.set_capacity(capacity).read())

    class _Bookings(Resource):
        @token_required()
        def get(self):
            """ The current user's upcoming bookings """
            bookings = Booking.query.filter(Booking._user_id == g.current_user.id, Booking._date >= today()) \
                .order_by(Booking._date).all()
            sessions = sorted((b.read(g.current_user) for b in bookings if b.meeting.active),
                              key=lambda s: (s["date"], s["start"]))
            return jsonify(sessions)

        @token_required()
        def post(self):
            """ Reserve spots {meeting_id, date, spots (default 1)} """
            body = request.get_json(silent=True) or {}
            meeting, on_date, error = find_session(body)
            if error:
                return error
            spots, error = check_spots(meeting, on_date, body)
            if error:
                return error
            booking = Booking(g.current_user, meeting, on_date, spots).create()
            if booking is None:
                return {"message": "You already have a reservation here; change its spots instead"}, 409
            resp = jsonify(booking.read(g.current_user))
            resp.status_code = 201
            return resp

        @token_required()
        def put(self):
            """ Change how many spots an existing reservation holds {meeting_id, date, spots} """
            body = request.get_json(silent=True) or {}
            meeting, on_date, error = find_session(body)
            if error:
                return error
            booking = meeting.bookings.filter_by(_user_id=g.current_user.id, _date=on_date).first()
            if booking is None:
                return {"message": "Reservation not found"}, 404
            spots, error = check_spots(meeting, on_date, body)
            if error:
                return error
            return jsonify(booking.set_spots(spots).read(g.current_user))

        @token_required()
        def delete(self):
            """ Cancel a reservation {meeting_id, date} """
            body = request.get_json(silent=True) or {}
            on_date = parse_date(body.get('date'))
            booking = Booking.query.filter_by(_user_id=g.current_user.id, _meeting_id=body.get('meeting_id'),
                                              _date=on_date).first() if on_date else None
            if booking is None:
                return {"message": "Reservation not found"}, 404
            meeting = booking.meeting
            booking.delete()
            return jsonify(meeting.read_session(on_date, g.current_user))

    class _Sync(Resource):
        @token_required("Admin")
        def post(self):
            """ Admin only: refresh the schedule from the feed now """
            status = sync_meetings()
            if status["error"]:
                return {"message": status["error"]}, 502
            return {"message": f"Synced {status['count']} meetings", **source_info()}

    api.add_resource(_Calendar, '')
    api.add_resource(_Meetings, '/meetings')
    api.add_resource(_Bookings, '/bookings')
    api.add_resource(_Sync, '/sync')

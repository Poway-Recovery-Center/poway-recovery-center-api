""" Reflection Wall API: anonymous notes shared with everyone (model/reflection.py)

GET    /api/reflections            newest notes (?tag=win to filter), each with its heart count and whether this visitor hearted it
POST   /api/reflections            post {text, tag}; appears for everyone right away
POST   /api/reflections/<id>/hold  send a heart (once per visitor per note)
DELETE /api/reflections/<id>       admin only: remove a note
GET    /api/reflections/tags       the kinds of reflection the form and filters offer

Visitors are anonymous: a random id in the prc_visitor cookie keeps hearts to one per note,
and a hashed client address limits how often one person can post.
"""
import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, jsonify, current_app, make_response
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from __init__ import db
from api.jwt_authorize import token_required
from model.reflection import Reflection, ReflectionHold, TAGS, MAX_TEXT_CHARS


reflection_api = Blueprint('reflection_api', __name__, url_prefix='/api')
api = Api(reflection_api)

VISITOR_COOKIE = 'prc_visitor'
VISITOR_MAX_AGE = 60 * 60 * 24 * 365  # 1 year
WALL_LIMIT = 100  # notes returned per request
# Posting limit per client address
POST_LIMIT = 5
POST_WINDOW = timedelta(minutes=10)

# The wall's guidelines ask people to leave out contact details; links are also the usual spam
_CONTACT_PATTERN = re.compile(
    r"https?://|www\.|\b[\w.+-]+@[\w-]+\.[\w.]+\b|\b[\w-]+\.(?:com|net|org|io|co|xyz|ru)\b|(?:\d[\s().-]?){7,}",
    re.IGNORECASE,
)


def visitor_id():
    """ This visitor's anonymous id from the cookie, or None on their first visit """
    value = request.cookies.get(VISITOR_COOKIE, '')
    return value if re.fullmatch(r'[A-Za-z0-9_-]{16,64}', value) else None


def with_visitor_cookie(resp, visitor):
    """ Keep the visitor cookie set (same cookie settings as the login cookie in api/user.py) """
    production = current_app.config['IS_PRODUCTION']
    resp.set_cookie(VISITOR_COOKIE, visitor, max_age=VISITOR_MAX_AGE, httponly=True, path='/',
                    secure=production, samesite='None' if production else 'Lax')
    return resp


def poster_hash():
    """ Hashed client address for rate limiting (the raw address is never stored).
    The last X-Forwarded-For entry is the one added by our own proxy, so clients can't fake it. """
    address = request.access_route[-1] if request.access_route else (request.remote_addr or '')
    return hmac.new(current_app.config['SECRET_KEY'].encode(), address.encode(), hashlib.sha256).hexdigest()


def held_by(visitor):
    if not visitor:
        return frozenset()
    rows = db.session.query(ReflectionHold.reflection_id).filter_by(_visitor=visitor).all()
    return frozenset(r[0] for r in rows)


class ReflectionAPI:
    class _Wall(Resource):
        def get(self):
            """ Newest notes first, optionally only one tag """
            visitor = visitor_id() or secrets.token_urlsafe(24)
            query = Reflection.query
            tag = request.args.get('tag')
            if tag in TAGS:
                query = query.filter_by(_tag=tag)
            notes = query.order_by(Reflection.created_at.desc(), Reflection.id.desc()).limit(WALL_LIMIT).all()
            held = held_by(visitor)
            return with_visitor_cookie(jsonify([n.read(held) for n in notes]), visitor)

        def post(self):
            """ Post {text, tag}; anyone can post, and it shows for everyone right away """
            body = request.get_json(silent=True) or {}
            text = ' '.join(str(body.get('text') or '').split())  # collapse runs of spaces and line breaks
            tag = body.get('tag')
            if not text:
                return {"message": "Write a few words first, then post."}, 400
            if len(text) > MAX_TEXT_CHARS:
                return {"message": f"Reflections can be up to {MAX_TEXT_CHARS} characters."}, 400
            if tag not in TAGS:
                return {"message": "Pick what kind of reflection this is."}, 400
            if _CONTACT_PATTERN.search(text):
                return {"message": "Please leave out links, emails and phone numbers so the wall stays anonymous."}, 400

            poster = poster_hash()
            since = datetime.now(timezone.utc) - POST_WINDOW
            recent = Reflection.query.filter(Reflection._poster == poster, Reflection.created_at >= since).count()
            if recent >= POST_LIMIT:
                return {"message": "You've shared a lot in a short time. Please wait a few minutes before posting again."}, 429

            note = Reflection(text, tag, poster).create()
            visitor = visitor_id() or secrets.token_urlsafe(24)
            resp = make_response(jsonify({"message": "Posted. Thank you for sharing.", "reflection": note.read()}), 201)
            return with_visitor_cookie(resp, visitor)

    class _Note(Resource):
        @token_required("Admin")
        def delete(self, id):
            """ Admin only: remove a note and its hearts """
            note = db.session.get(Reflection, id)
            if note is None:
                return {"message": "Reflection not found"}, 404
            note.delete()
            return {"message": "Reflection removed"}

    class _Hold(Resource):
        def post(self, id):
            """ Send a heart to a note; a visitor can heart each note once """
            note = db.session.get(Reflection, id)
            if note is None:
                return {"message": "That reflection is no longer on the wall."}, 404
            visitor = visitor_id() or secrets.token_urlsafe(24)
            try:
                db.session.add(ReflectionHold(reflection_id=note.id, _visitor=visitor))
                db.session.commit()
            except IntegrityError:
                db.session.rollback()  # already hearted: just return the current count
            return with_visitor_cookie(jsonify(note.read(held_by(visitor))), visitor)

    class _Tags(Resource):
        def get(self):
            """ The kinds of reflection, in display order """
            return jsonify([{"value": k, "label": label, "filter_label": plural} for k, (label, plural) in TAGS.items()])

    api.add_resource(_Wall, '/reflections')
    api.add_resource(_Note, '/reflections/<int:id>')
    api.add_resource(_Hold, '/reflections/<int:id>/hold')
    api.add_resource(_Tags, '/reflections/tags')

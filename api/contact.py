""" Contact API: the site's Contact Us form (same pattern as api/user.py) """
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from __init__ import db
from api.jwt_authorize import token_required, current_user_or_none
from model.contact import ContactMessage
from model.user import User


contact_api = Blueprint('contact_api', __name__, url_prefix='/api')
api = Api(contact_api)

MAX_MESSAGE_CHARS = 2000


class ContactAPI:
    class _CRUD(Resource):
        def post(self):
            """ Send a message {name, message, topic?, email?, phone?}; anyone can send one """
            body = request.get_json(silent=True) or {}
            name = str(body.get('name') or '').strip()
            message = str(body.get('message') or '').strip()
            email = str(body.get('email') or '').strip()
            phone = str(body.get('phone') or '').strip()
            if not name:
                return {"message": "Please tell us your name"}, 400
            if not message:
                return {"message": "Please write a message"}, 400
            if len(message) > MAX_MESSAGE_CHARS:
                return {"message": f"Messages can be up to {MAX_MESSAGE_CHARS} characters"}, 400
            error = User.validate(email=email, phone=phone)
            if error:
                return {"message": error}, 400

            ContactMessage(name, message, body.get('topic'), email, phone, current_user_or_none()).create()
            return {"message": "Thanks, your message was sent. We'll reply as soon as we can."}, 201

        @token_required("Admin")
        def get(self):
            """ Admin only: every message, newest first """
            messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
            return jsonify([m.read() for m in messages])

        @token_required("Admin")
        def put(self):
            """ Admin only: mark a message handled or not {id, handled} """
            body = request.get_json(silent=True) or {}
            message = db.session.get(ContactMessage, body.get('id') or 0)
            if message is None:
                return {"message": "Message not found"}, 404
            return jsonify(message.set_handled(body.get('handled', True)).read())

    class _Topics(Resource):
        def get(self):
            """ The topics the form offers """
            return jsonify([{"value": k, "label": v} for k, v in ContactMessage.TOPICS.items()])

    api.add_resource(_CRUD, '/contact')
    api.add_resource(_Topics, '/contact/topics')

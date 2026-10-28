""" Mood Room API: matches what the person typed to a grounding room (rooms and keywords live in model/mood.py) """
from flask import Blueprint, request
from flask_restful import Api, Resource

from model.mood import match_room


mood_api = Blueprint('mood_api', __name__, url_prefix='/api')
api = Api(mood_api)

MAX_TEXT_CHARS = 2000


class MoodAPI:
    class _Room(Resource):
        def post(self):
            """ Find a room for {text}; anyone can use it and nothing is stored """
            body = request.get_json(silent=True) or {}
            text = str(body.get('text') or '')
            if len(text) > MAX_TEXT_CHARS:
                return {"message": f"Please keep it under {MAX_TEXT_CHARS} characters"}, 400
            return match_room(text)

    api.add_resource(_Room, '/mood')

""" Recovery tracker API: weekly check-ins for the logged-in user (model/checkin.py) """
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

from api.jwt_authorize import token_required
from model.checkin import CheckIn, current_week


checkin_api = Blueprint('checkin_api', __name__, url_prefix='/api')
api = Api(checkin_api)


class CheckInAPI:
    class _CRUD(Resource):
        @token_required()
        def get(self):
            """ This user's check-ins, oldest first, and the current week {week, checkins} """
            checkins = g.current_user.checkins.order_by(CheckIn._week).all()
            return jsonify({"week": current_week().isoformat(), "checkins": [c.read() for c in checkins]})

        @token_required()
        def post(self):
            """ Save this week's check-in {mood, sleep, cravings, stress, actions, note}; saving again updates the week """
            ratings, actions, note, error = CheckIn.validate(request.get_json(silent=True) or {})
            if error:
                return {"message": error}, 400
            week = current_week()
            checkin = g.current_user.checkins.filter_by(_week=week).first()
            created = checkin is None
            if created:
                checkin = CheckIn(g.current_user, week)
            concerns = checkin.save(ratings, actions, note)
            message = "Check-in saved." if created else "This week's check-in was updated."
            return {"message": message, "checkin": checkin.read(), "concerns": concerns}, 201 if created else 200

    class _Alerts(Resource):
        @token_required("Admin")
        def get(self):
            """ Admin only: every week that alerted counselors, newest first """
            alerts = CheckIn.query.filter_by(_alerted=True).order_by(CheckIn._week.desc(), CheckIn.updated_at.desc()).all()
            return jsonify([c.read_alert() for c in alerts])

    api.add_resource(_CRUD, '/checkins')
    api.add_resource(_Alerts, '/checkins/alerts')

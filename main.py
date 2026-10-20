"""
Poway Recovery Center API - entry point (same role as Open Coding Society flask main.py)

Run it with:
    python main.py

On start it creates the user management database (instance/volumes/user_management.db),
adds the default users, syncs the meeting schedule, and serves the API on http://localhost:8587
"""
from flask import jsonify

from __init__ import app, db
from api.chat import chat_api
from api.contact import contact_api
from api.schedule import schedule_api
from api.user import user_api
from model.contact import initContacts
from model.schedule import initSchedules
from model.user import initUsers


# Register URIs for API endpoints
app.register_blueprint(user_api)
app.register_blueprint(chat_api)
app.register_blueprint(contact_api)
app.register_blueprint(schedule_api)


@app.route('/')
def index():
    return jsonify({"service": "Poway Recovery Center API", "status": "ok"})


# Create the database, default users, and current meeting schedule whenever the app starts (python main.py or gunicorn)
initUsers()
initSchedules()
initContacts()

if __name__ == "__main__":
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Server running: http://localhost:{app.config['FLASK_PORT']}")
    app.run(debug=True, host="0.0.0.0", port=app.config['FLASK_PORT'], use_reloader=False)

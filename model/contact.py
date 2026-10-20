""" Contact message model (same pattern as model/user.py)

Messages sent from the site's Contact Us form; admins read them on their profile page.
"""
from datetime import datetime, timezone

from __init__ import app, db


class ContactMessage(db.Model):
    """
    ContactMessage Model

    Attributes:
        id (Column): Primary key.
        _name (Column): Sender's name.
        _email (Column): Optional email to reply to.
        _phone (Column): Optional phone to reply to.
        _topic (Column): What the message is about (see TOPICS).
        _message (Column): The message text.
        _user_id (Column): The sender's account, when they were logged in.
        _handled (Column): Set by an admin once the message has been answered.
        created_at (Column): When it was sent.
    """
    __tablename__ = 'contact_messages'

    TOPICS = {
        'general': 'General question',
        'meetings': 'Meetings and schedule',
        'volunteer': 'Volunteering',
        'website': 'Website or account help',
    }

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _email = db.Column(db.String(255), nullable=True)
    _phone = db.Column(db.String(32), nullable=True)
    _topic = db.Column(db.String(32), nullable=False)
    _message = db.Column(db.Text, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    _handled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, name, message, topic='general', email=None, phone=None, user=None):
        self._name = name.strip()
        self._message = message.strip()
        self._topic = topic if topic in self.TOPICS else 'general'
        self._email = email.strip().lower() if email else None
        self._phone = phone.strip() if phone else None
        self._user_id = user.id if user else None

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def set_handled(self, handled):
        self._handled = bool(handled)
        db.session.commit()
        return self

    def read(self):
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email or "",
            "phone": self._phone or "",
            "topic": self._topic,
            "topic_label": self.TOPICS.get(self._topic, self._topic),
            "message": self._message,
            "handled": self._handled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def initContacts():
    """ Create the contact_messages table """
    with app.app_context():
        db.create_all()

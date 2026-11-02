""" Reflection Wall model (same pattern as model/contact.py)

Anonymous notes anyone can post on the home page's Reflection Wall; they appear for everyone right away.
Hearts ("holds") are one per visitor per note, tracked by an anonymous visitor id cookie (see api/reflection.py).
Admins can remove notes from the backend's Reflections page.
"""
from datetime import datetime, timezone

from __init__ import app, db


MAX_TEXT_CHARS = 280

# Kinds of reflection the form offers, in display order (value: (label, filter label))
TAGS = {
    'win': ('Small win', 'Small wins'),
    'truth': ('Gentle truth', 'Gentle truths'),
    'thanks': ('Gratitude', 'Gratitude'),
    'hope': ('Note of hope', 'Hope'),
}


class Reflection(db.Model):
    """
    Reflection Model

    Attributes:
        id (Column): Primary key.
        _text (Column): The note (up to MAX_TEXT_CHARS).
        _tag (Column): Kind of reflection (see TAGS).
        _poster (Column): Hashed client address, only used to rate limit posting.
        created_at (Column): When it was posted.
    """
    __tablename__ = 'reflections'

    id = db.Column(db.Integer, primary_key=True)
    _text = db.Column(db.String(MAX_TEXT_CHARS), nullable=False)
    _tag = db.Column(db.String(16), nullable=False)
    _poster = db.Column(db.String(64), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    holds = db.relationship('ReflectionHold', backref='reflection', cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, text, tag='win', poster=None):
        self._text = text.strip()[:MAX_TEXT_CHARS]
        self._tag = tag if tag in TAGS else 'win'
        self._poster = poster

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self, held_ids=frozenset()):
        return {
            "id": self.id,
            "text": self._text,
            "tag": self._tag,
            "tag_label": TAGS[self._tag][0] if self._tag in TAGS else self._tag,
            "holds": self.holds.count(),
            "held": self.id in held_ids,
            "created_at": self.created_at.replace(tzinfo=timezone.utc).isoformat() if self.created_at else None,
        }


class ReflectionHold(db.Model):
    """ One heart: a visitor sending support to a reflection (unique per visitor per note) """
    __tablename__ = 'reflection_holds'
    __table_args__ = (db.UniqueConstraint('reflection_id', '_visitor', name='uq_reflection_hold'),)

    id = db.Column(db.Integer, primary_key=True)
    reflection_id = db.Column(db.Integer, db.ForeignKey('reflections.id', ondelete='CASCADE'), nullable=False, index=True)
    _visitor = db.Column(db.String(64), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


def initReflections():
    """ Create the reflections and reflection_holds tables """
    with app.app_context():
        db.create_all()

from datetime import datetime

from yacut import db

from .constants import MAX_CUSTOM_ID_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_CUSTOM_ID_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.short
        }

    def from_dict(self, url_data):
        self.original = url_data['url']
        self.short = url_data['custom_id']

    @classmethod
    def create(cls, original, short):
        url_map = cls(
            original=original,
            short=short
        )
        db.session.add(url_map)
        return url_map
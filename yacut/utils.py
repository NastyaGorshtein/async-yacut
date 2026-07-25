from random import choice

from .constants import (
    ALLOWED_SYMBOLS,
    DEFAULT_SHORT_ID_LENGTH,
    MAX_CUSTOM_ID_LENGTH
)
from .models import URLMap


def get_unique_short_id():
    while True:
        short_id = ''.join(
            choice(ALLOWED_SYMBOLS)
            for _ in range(DEFAULT_SHORT_ID_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def is_valid_short_id(short_id):
    if len(short_id) > MAX_CUSTOM_ID_LENGTH:
        return False

    for symbol in short_id:
        if symbol not in ALLOWED_SYMBOLS:
            return False

    return True
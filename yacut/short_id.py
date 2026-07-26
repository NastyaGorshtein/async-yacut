import re

from random import choice

from .constants import (
    ALLOWED_SYMBOLS,
    DEFAULT_SHORT_ID_LENGTH,
    MAX_CUSTOM_ID_LENGTH,
    SHORT_ID_PATTERN
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
    return (
        len(short_id) <= MAX_CUSTOM_ID_LENGTH
        and re.fullmatch(SHORT_ID_PATTERN, short_id) is not None
    )
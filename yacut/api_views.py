from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import (
    DUPLICATE_MESSAGE,
    INVALID_NAME_MESSAGE,
    NOT_FOUND_MESSAGE,
    NO_BODY_MESSAGE,
    NO_URL_MESSAGE,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .short_id import get_unique_short_id, is_valid_short_id


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    request_data = request.get_json(silent=True)

    if request_data is None:
        raise InvalidAPIUsage(NO_BODY_MESSAGE)

    if 'url' not in request_data:
        raise InvalidAPIUsage(NO_URL_MESSAGE)

    custom_id = request_data.get('custom_id')

    if custom_id:
        if not is_valid_short_id(custom_id):
            raise InvalidAPIUsage(INVALID_NAME_MESSAGE)

        if (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first() is not None
        ):
            raise InvalidAPIUsage(DUPLICATE_MESSAGE)

        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    url_map = URLMap.create(
        original=request_data['url'],
        short=short_id
    )
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True
        )
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        raise InvalidAPIUsage(
            NOT_FOUND_MESSAGE,
            HTTPStatus.NOT_FOUND
        )

    return jsonify({
        'url': url_map.original
    })
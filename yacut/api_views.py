import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    MAX_SHORT_URL_LENGTH,
    MIN_SHORT_URL_LENGTH,
    SHORT_PATTERN
)
from .error_handlers import InvalidAPIUsage
from .models import ShortLinkCreationError, URLMap


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    """Функция получения ссылки"""
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if custom_id:
        if (not MIN_SHORT_URL_LENGTH <= len(custom_id)
                <= MAX_SHORT_URL_LENGTH
                or not re.match(SHORT_PATTERN, custom_id)):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

    try:
        url_map = URLMap.create(
            original=data['url'],
            custom_id=data.get('custom_id')
        )
    except ShortLinkCreationError as e:
        raise InvalidAPIUsage(str(e))

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def api_redirect_to_original(short):
    """Функция переадресации на оригинальную ссылку"""
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original}), HTTPStatus.OK

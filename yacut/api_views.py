from http import HTTPStatus
import re

from flask import jsonify, request, url_for

from . import app, db
from .constants import (
    FORBIDEN_URLS,
    MAX_SHORT_URL_LENGTH,
    MIN_SHORT_URL_LENGTH,
    SHORT_PATTERN
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    """Функция получения ссылки"""
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    original_link = data['url']
    custom_id = data.get('custom_id')

    if custom_id:
        if URLMap.get(custom_id) is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        if custom_id in FORBIDEN_URLS:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки запрещен'
            )
        if not (
            MIN_SHORT_URL_LENGTH <= len(custom_id) <= MAX_SHORT_URL_LENGTH
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if not re.match(SHORT_PATTERN, custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        short = custom_id
    else:
        short = URLMap.generate_unique_short()

    url_map = URLMap(
        original=original_link,
        short=short
    )

    db.session.add(url_map)
    db.session.commit()

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
    return jsonify({"url": url_map.original}), HTTPStatus.OK

from http import HTTPStatus

from flask import jsonify, request

from . import app
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

import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import FORBIDEN_URLS
from .utilits import generate_unique_short


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    try:
        data = request.get_json(silent=True)
    except Exception as e:
        print(f"Ошибка при парсинге JSON: {e}")
        data = None

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    original_link = data['url']
    custom_id = data.get('custom_id')

    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        if custom_id in FORBIDEN_URLS:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки запрещен'
            )
        if len(custom_id) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if not re.match('^[A-Za-z0-9]+$', custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        short = custom_id
    else:
        short = generate_unique_short()

    url_map = URLMap(
        original=original_link,
        short=short
    )

    db.session.add(url_map)
    db.session.commit()

    base_url = request.host_url.rstrip('/')
    short_url = f"{base_url}/{short}"

    return jsonify({
        'url': original_link,
        'short_link': short_url
    }), 201


@app.route('/api/id/<short>/', methods=['GET'])
def api_redirect_to_original(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({"url": url_map.original}), 200

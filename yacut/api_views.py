import re

from flask import jsonify, request

from . import app, db
from .constants import VALID_CHARS
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url = URLMap.query.filter_by(short=short).first()
    if not URLMap.query.filter_by(short=short).first():
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url=url.original), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(original=data['url']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id()
    if not re.match(VALID_CHARS, data['custom_id']) or len(
        data['custom_id']
    ) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201
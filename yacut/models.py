from datetime import datetime
import random
import re
import string

from flask import url_for

from .constants import (
    FORBIDEN_URLS,
    MAX_SHORT_URL_LENGTH,
    URL_MAX_LENGHT,
    MIN_SHORT_URL_LENGTH,
    SHORT_PATTERN,
    MAX_SHORT_URL_LENGTH
)
from yacut import db


class ShortLinkCreationError(Exception):
    """Исключение для ошибок создания короткой ссылки."""
    pass


class URLMap(db.Model):
    """Модель записи короткой ссылки и её оригинального варианта"""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_MAX_LENGHT), nullable=False)
    short = db.Column(db.String(MAX_SHORT_URL_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for(
                'redirect_to_original',
                short=self.short,
                _external=True
            )
        }

    @staticmethod
    def generate_unique_short(length=6):
        """Генерирует уникальный короткий идентификатор для ссылки."""
        short = ''.join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )
        while (
            URLMap.query.filter_by(short=short).first() is not None
            or short in FORBIDEN_URLS
        ):
            short = URLMap.generate_unique_short()
        return short

    @staticmethod
    def get(short):
        """"Метод возвращает запись ко короткому идентификатору."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original, custom_id=None):
        """Создает и сохраняет новую короткую ссылку."""
        if custom_id:
            if not (
                MIN_SHORT_URL_LENGTH <= len(custom_id) <= MAX_SHORT_URL_LENGTH
            ):
                raise ShortLinkCreationError(
                    'Указано недопустимое имя для короткой ссылки'
                )

            if not re.match(SHORT_PATTERN, custom_id):
                raise ShortLinkCreationError(
                    'Указано недопустимое имя для короткой ссылки'
                )

            if URLMap.query.filter_by(short=custom_id).first() is not None:
                raise ShortLinkCreationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )

            if custom_id in FORBIDEN_URLS:
                raise ShortLinkCreationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )

            short = custom_id
        else:
            short = URLMap.generate_unique_short()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        return url_map

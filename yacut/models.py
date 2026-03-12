from datetime import datetime
import random
import string

from flask import url_for

from .constants import FORBIDEN_URLS, MAX_SHORT_URL_LENGTH, URL_MAX_LENGHT
from yacut import db


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
                external=True
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
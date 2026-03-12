from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import (
    MAX_SHORT_URL_LENGTH,
    MIN_SHORT_URL_LENGTH,
    SHORT_PATTERN
)


class URLMapForm(FlaskForm):
    """Форма для главной страницы создания коротких ссылкок"""
    original_link = URLField(
        'Добавьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(
                message='Некорректный URL.'
                'Убедитесь, что ссылка начинается с http:// или https://'
            )
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                min=MIN_SHORT_URL_LENGTH,
                max=MAX_SHORT_URL_LENGTH,
                message=(
                    f'Длина ссылки должна быть'
                    f' от {MIN_SHORT_URL_LENGTH}'
                    f' до {MAX_SHORT_URL_LENGTH} символов'
                )
            ),
            Regexp(
                regex=SHORT_PATTERN,
                message='Допустимы только латинские буквы и цифры'
            )
        ]
    )


class UploadFilesForm(FlaskForm):
    """Форма для страницы загрузок файлов"""
    files = MultipleFileField()

from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL
from flask_wtf.file import MultipleFileField


MIN_SHORT_LENGTH = 1
MAX_SHORT_LENGTH = 16
SHORT_PATTERN = '^[A-Za-z0-9]+$'


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
                min=MIN_SHORT_LENGTH,
                max=MAX_SHORT_LENGTH,
                message=(
                    f'Длина ссылки должна быть '
                    f'от {MIN_SHORT_LENGTH} до {MAX_SHORT_LENGTH} символов'
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

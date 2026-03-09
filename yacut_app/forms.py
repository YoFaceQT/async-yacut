from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import MultipleFileField


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16, message='Cсылка не может быть длиннее 16 символов')
        ]
    )


class UploadFilesForm(FlaskForm):
    files = MultipleFileField()

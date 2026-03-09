from flask_wtf import FlaskForm
from wtforms import URLField
from wtforms.validators import Length
from flask_wtf.file import MultipleFileField


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[
            Length(1, 256, message='Ссылка не может быть длинее 256 символов')
        ]
    )
    custom_id = URLField(
        'Добавьте свой вариант короткой сслыки',
        validators=[
            Length(1, 16, message='Ссылка не может быть длинее 16 символов')
        ]
    )


class UploadFilesForm(FlaskForm):
    files = MultipleFileField()

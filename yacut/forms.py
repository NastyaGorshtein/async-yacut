from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .constants import (
    ALLOWED_SYMBOLS,
    MAX_CUSTOM_ID_LENGTH
)


def validate_custom_id(form, field):
    if not field.data:
        return

    for symbol in field.data:
        if symbol not in ALLOWED_SYMBOLS:
            raise ValidationError(
                'Допустимы только латинские буквы и цифры'
            )


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле')
        ]
    )

    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=MAX_CUSTOM_ID_LENGTH),
            validate_custom_id
        ]
    )

    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[FileRequired()]
    )

    submit = SubmitField('Загрузить')
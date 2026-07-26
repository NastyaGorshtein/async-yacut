from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    SHORT_ID_PATTERN,
    MAX_CUSTOM_ID_LENGTH
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
            Regexp(
                SHORT_ID_PATTERN,
                message='Допустимы только латинские буквы и цифры'
            )
        ]
    )

    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[FileRequired()]
    )

    submit = SubmitField('Загрузить')
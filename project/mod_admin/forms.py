from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from project.models import Manufacturer


def manufacturers_choices():
    return Manufacturer.query.all()


class ProductCreateForm(FlaskForm):
    Title = StringField('Найменування', [InputRequired(message='Название товара обязательно')])
    Manufacturer = QuerySelectField(
        'Виробник',
        query_factory=manufacturers_choices,
        get_label='CompanyName'
    )
    Price = StringField('Ціна', [InputRequired(message='Цена товара обязательно')])
    Photo = FileField('Фото')
    Submit = SubmitField('Додати')

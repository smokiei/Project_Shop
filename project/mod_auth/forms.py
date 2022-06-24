from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email


# Define the login form (WTForms)
class LoginForm(FlaskForm):
    email = StringField('Ім’я або Email',
                        [InputRequired(message='Forgot your email address?')],
                        render_kw={'placeholder': 'Ім’я або Email'}
                        )
    password = PasswordField('Пароль',
                             [InputRequired(message='Must provide a password. ;-)')],
                             render_kw={'placeholder': 'Пароль'}
                             )
    remember = BooleanField('Запом’ятати мене')
    submit = SubmitField('Увійти')


class SignUpForm(FlaskForm):
    username = StringField('Ім’я',
                           [InputRequired(message='Forgot your email address?')],
                           render_kw={'placeholder': 'Ім’я'}
                           )
    email = StringField('Email',
                        [Email(), InputRequired(message='Forgot your email address?')],
                        render_kw={'placeholder': 'Email'}
                        )
    password = PasswordField('Пароль',
                             [InputRequired(message='Must provide a password. ;-)')],
                             render_kw={'placeholder': 'Пароль'}
                             )
    submit = SubmitField('Зареєструватися')

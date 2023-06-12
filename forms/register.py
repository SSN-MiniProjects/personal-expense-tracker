from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError
from models.login_credentials import (
    get_user_by_email
)

class Register(FlaskForm):
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='password_create',
                             validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_email = get_user_by_email(email.data)
        if existing_email is not None:
            raise ValidationError('This email already exists!')
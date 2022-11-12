from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError, InputRequired, Length
from database import fetchUserByEmail

class LoginForm(FlaskForm):
    email = StringField('Email',
                         id='email_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='password_login',
                             validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='password_create',
                             validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_email = fetchUserByEmail(email.data)
        if existing_email != []:
            raise ValidationError('This email already exists!')

class Transaction(FlaskForm):
    # login_id = StringField(render_kw={"placeholder": "Login ID"})
    transaction = StringField(validators=[
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Transaction"})
    mode = StringField(validators=[
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Mode"})
    category = StringField(validators=[
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Category"})
    datestamp = StringField(validators=[
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Date"})
    note = StringField(validators=[
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Note"})
    submit = SubmitField('Submit Transaction')
    def validate_transaction(self, transaction):
        if int(transaction.data) < 0:
            raise ValidationError('Enter a valid amount')
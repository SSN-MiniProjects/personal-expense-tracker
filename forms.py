from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField,SelectField,BooleanField
from wtforms.validators import Email, DataRequired, ValidationError, InputRequired, Length
import phonenumbers
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
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Expense Amount"})
    mode = SelectField('Mode', choices=["Online","Cash"],validators=[
                           InputRequired()], render_kw={"placeholder": "Category"})
    category = SelectField('Category', choices=["Housing","Transport","Food","Family","Medical","Debt Payment","Entertainment","Food","Other"],validators=[
                           InputRequired()])
    datestamp = DateField('Start Date', format='%Y-%m-%d',validators=[
                           InputRequired()], render_kw={"placeholder": "Date"})
    note = StringField(validators=[
                           InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Note"})
    submit = SubmitField('Submit Transaction')
    def validate_transaction(self, transaction):
        if int(transaction.data) < 0:
            raise ValidationError('Enter a valid amount')

class Customize(FlaskForm):
    # login_id = StringField(render_kw={"placeholder": "Login ID"})
    name = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Name"})
    budget = StringField('Budget', validators=[InputRequired()], render_kw={"placeholder": "Budget"})
    total_spent = StringField('Total_Spent', validators=[DataRequired()], render_kw={"placeholder": "Total Spent"})
    phone = StringField('Phone', validators=[DataRequired()], render_kw={"placeholder": "Phone"})
    profession = StringField(validators=[InputRequired(), Length(min=1, max=40)], render_kw={"placeholder": "Profession"})
    alert = BooleanField()
    submit = SubmitField('Submit Transaction')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        
    def validate_budget(self, budget):
        if int(budget.data) < 0:
            raise ValidationError('Enter a valid budget')
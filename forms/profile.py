from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError, StopValidation
import phonenumbers


class UserProfile(FlaskForm):
    name = StringField()
    budget = StringField('Budget')
    phone = StringField('Phone', render_kw={"placeholder" : "Enter 10-digit number with country code"})
    profession = StringField()
    alert = BooleanField(default= False)
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        if phone.data == '':
            raise StopValidation
        
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        
    def validate_budget(self, budget):

        if int(budget.data) < 0:
            raise ValidationError('Enter a valid budget')
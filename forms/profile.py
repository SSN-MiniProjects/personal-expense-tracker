from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError
import phonenumbers


class UserProfile(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Name"})
    budget = FloatField('Budget', validators=[InputRequired()], render_kw={"placeholder": "Budget"})
    phone = StringField('Phone', validators=[DataRequired()], render_kw={"placeholder": "Phone"})
    profession = StringField(validators=[InputRequired(), Length(min=1, max=40)], render_kw={"placeholder": "Profession"})
    alert = BooleanField()
    submit = SubmitField('Update Profile')

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
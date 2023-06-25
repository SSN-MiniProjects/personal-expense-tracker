from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError, StopValidation


class UserEvent(FlaskForm):
    name = StringField(validators=[
                           InputRequired()
                           ],)
    budget = StringField('Budget',validators=[
                           InputRequired()
                           ],)
    submit = SubmitField('Submit')

    def validate_budget(self, budget):

        if int(budget.data) <= 0:
            raise ValidationError('Enter a valid budget')
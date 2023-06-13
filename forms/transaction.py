from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
import datetime



class Transaction(FlaskForm):
    # login_id = StringField(render_kw={"placeholder": "Login ID"})
    transaction = FloatField(label="Expense Amount", validators=[
                           InputRequired()
                           ],
                           )
    mode = SelectField('Mode', choices=["Online","Cash"],validators=[
                           InputRequired()], render_kw={"placeholder": "Category"})
    category = SelectField('Category', choices=["Housing","Transport","Food","Family","Medical","Debt Payment","Entertainment","Food","Other"],validators=[
                           InputRequired()])
    datestamp = DateField('Start Date', format='%Y-%m-%d',validators=[
                           InputRequired()], render_kw={"placeholder": "Date"})
    note = StringField(validators = [Length(min=1, max=20)], render_kw={"placeholder": "Note"})
    submit = SubmitField('Submit')


    def validate_transaction(self, transaction):
        if int(transaction.data) < 0:
            raise ValidationError('Enter a valid amount')
    
    def validate_date(self, field):
        if field.data > datetime.date.today():
            raise ValidationError("The date cannot be in the Future!")


class TransactionFile(FlaskForm):
    file = FileField('csv', validators=[
        FileAllowed(['csv'], 'CSV only!')])
    submit1 = SubmitField('submit')
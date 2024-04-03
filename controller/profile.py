from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError, StopValidation
import phonenumbers
from flask_login import login_required, current_user

from config.factory import AppFlask
from services.users import UserProfileService

app = AppFlask().instance


class UserProfileForm(FlaskForm):
    name = StringField()
    budget = StringField('Budget')
    phone = StringField('Phone', render_kw={"placeholder": "Enter 10-digit number with country code"})
    profession = StringField()
    alert = BooleanField(default=False)
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        if not UserProfileService.is_valid_phone(phone.data):
            raise StopValidation('Enter a valid phone number')

    def validate_budget(self, budget):
        if int(budget.data) < 0:
            raise ValidationError('Enter a valid budget')


def update_profile():
    details = UserProfileService.get(current_user.email)
    form = UserProfileForm(
        name=details["name"],
        budget=details["budget"],
        phone=details["phone"],
        profession=details["profession"],
        alert=details["alert"])

    if not form.validate_on_submit():
        return render_template('customize.html', form=form)
    name = form.name.data
    budget = float(form.budget.data)
    phone = form.phone.data
    profession = form.profession.data
    alert = form.alert.data
    UserProfileService.update(current_user.email, name, budget, phone, profession, alert)
    flash("Profile updated successfully", "success")
    return redirect(url_for('customize'))

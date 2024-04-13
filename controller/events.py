from flask import flash, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, ValidationError
from flask_login import login_required, current_user
import humanize
from config.constants import ErrorConstants, InputErrorMessages
from config.factory import AppFlask
from services.events import EventService
from utilities.common import CommonUtils

app = AppFlask().instance


class UserEvent(FlaskForm):
    name = StringField(validators=[
        InputRequired()
    ], )
    budget = FloatField('Budget', validators=[
        InputRequired()
    ], )
    submit = SubmitField('Submit')

    def validate_budget(self, budget):
        if not budget.data or int(budget.data) <= 0:
            self.budget.errors.clear()
            raise ValidationError(InputErrorMessages.NOT_VALID_BUDGET)


def create_event():
    form = UserEvent()
    user_email = current_user.email

    if not form.validate_on_submit():
        return render_template('add_event.html', form=form)

    template = render_template('add_event.html', form=form)
    name = form.name.data
    budget = form.budget.data

    if EventService.is_existed_by_name(user_email, name):
        flash(ErrorConstants.DUPLICATE_EVENT_NAME, "error")
        return template

    EventService.create(user_email, name, budget)
    flash("Event added successfully", "success")
    return redirect(url_for('event_list'))


def show_event_list():
    user_email = current_user.email
    events = EventService.get_list(user_email)

    def update_budget_percentage(event):
        event["budget_percentage"] = EventService.get_budget_percentage(user_email, event["id"], event["budget"])
        return event

    events = list(map(update_budget_percentage, events))
    return render_template("event_list.html", events=events)


def get_event(id):
    user_email = current_user.email
    if not EventService.is_existed_by_id(user_email, id):
        flash(ErrorConstants.EVENT_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    result = EventService.get(user_email, id)[0]
    event_details = {
        "id": result["id"],
        "name": result["name"],
        "budget": humanize.intcomma(result["budget"]),
        "budget_percentage": CommonUtils.calculate_budget_percentage(result["spent"], result["budget"]),
        "spent": humanize.intcomma(result["spent"]),

    }
    event_transactions = EventService.get_transactions(id)
    return render_template("view_event.html", event=event_details, transactions=event_transactions)


def update_specific_event(id):
    user_email = current_user.email
    if not EventService.is_existed_by_id(user_email, id):
        flash(ErrorConstants.EVENT_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    event_details = EventService.get(user_email, id)[0]
    form = UserEvent(name=event_details["name"], budget=event_details["budget"])
    if not form.validate_on_submit():
        return render_template('update_event.html', form=form)
    EventService.update(event_details['id'], form.name.data, form.budget.data)
    flash(event_details["name"] + " updated !", "success")
    return redirect(url_for('get_specific_event', id=event_details["id"]))


def delete_event(id):
    user_email = current_user.email
    if not EventService.is_existed_by_id(user_email, id):
        flash(ErrorConstants.EVENT_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    EventService.delete(id, user_email)
    flash("Event deleted", "success")
    return redirect(url_for('event_list'))

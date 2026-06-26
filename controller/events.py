from flask import flash, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, ValidationError
from flask_login import current_user
import humanize

from config.authentication import SessionUser
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

    if not form.validate_on_submit():
        return render_template('add_event.html', form=form)

    template = render_template('add_event.html', form=form)
    name = form.name.data
    budget = form.budget.data

    session_user : SessionUser = current_user
    login_id = session_user.get_login_id()
    if EventService.is_existed_by_name(login_id, name):
        flash(ErrorConstants.DUPLICATE_EVENT_NAME, "error")
        return template

    EventService.create(login_id, name, budget)
    flash("Event added successfully", "success")
    return redirect(url_for('event_list'))


def show_event_list():
    events = EventService.get_list(current_user.login_id)
    result = []
    for event in events:
        result.append({
            "id": event["id"],
            "name": event["name"],
            "budget": event["budget"],
            "budget_percentage": EventService.get_budget_percentage(current_user.login_id, event["id"], event["budget"])
        })
    return render_template("event_list.html", events=result)


def get_event(id):
    session_user : SessionUser = current_user
    login_id = session_user.get_login_id()
    if not EventService.is_existed_by_id(login_id, id):
        flash(ErrorConstants.EVENT_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    result = EventService.get(login_id, id)[0]
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
    session_user : SessionUser = current_user
    login_id = session_user.get_login_id()
    if not EventService.is_existed_by_id(login_id, id):
        flash(ErrorConstants.EVENT_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    event_details = EventService.get(login_id, id)[0]
    form = UserEvent(name=event_details["name"], budget=event_details["budget"])
    if not form.validate_on_submit():
        return render_template('update_event.html', form=form)
    EventService.update(event_details['id'], form.name.data, form.budget.data)
    flash(event_details["name"] + " updated !", "success")
    return redirect(url_for('get_specific_event', id=event_details["id"]))


def delete_event(id):
    session_user : SessionUser = current_user

    if not EventService.is_existed_by_id(session_user.get_login_id(), id):
        flash(ErrorConstants.EVENT_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    EventService.delete(id, session_user.get_login_id())
    flash("Event deleted", "success")
    return redirect(url_for('event_list'))

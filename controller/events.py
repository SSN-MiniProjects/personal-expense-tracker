from flask import flash, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError
from flask_login import login_required, current_user

from config.constants import ErrorConstants
from config.factory import AppFlask
from services.events import EventService

app = AppFlask().instance


class UserEvent(FlaskForm):
    name = StringField(validators=[
        InputRequired()
    ], )
    budget = StringField('Budget', validators=[
        InputRequired()
    ], )
    submit = SubmitField('Submit')

    def validate_budget(self, budget):
        if int(budget.data) <= 0:
            raise ValidationError('Enter a valid budget')


@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = UserEvent()
    user_email = current_user.email
    template = render_template('add_event.html', form=form)

    if not form.validate_on_submit():
        return template

    if form.validate_on_submit():
        name = form.name.data
        budget = form.budget.data

        if EventService.is_existed(user_email, name) is not None:
            flash(ErrorConstants.DUPLICATE_EVENT_NAME, "error")
            return template

        EventService.create(user_email, name, budget)
        flash("Event added successfully", "success")
        return redirect(url_for('event_list'))


@app.route('/event_list', methods=['GET'])
@login_required
def event_list():
    user_email = current_user.email
    events = EventService.get_event_list(user_email)
    return render_template("event_list.html", events=events)


@app.route('/event_list/<int:id>', methods=['GET'])
@login_required
def get_specific_event(id):
    user_email = current_user.email
    check_event = get_event_by_id(user_email, id)

    if len(check_event) == 0:
        flash("Event not found", "error")
        return redirect(url_for('dashboard'))

    result = check_event[0]
    event_details = {
        "id": result["id"],
        "name": result["name"],
        "budget": humanize.intcomma(result["budget"]),
        "budget_percentage": round(result["spent"] / result["budget"] * 100, 2),
        "spent": humanize.intcomma(result["spent"]),

    }

    event_transactions = get_transactions_by_event(id)
    return render_template("view_event.html", event=event_details, transactions=event_transactions)


@app.route('/event_list/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    user_email = current_user.email
    check_event = get_event_by_id(user_email, id)

    if len(check_event) == 0:
        flash("Event not found", "error")
        return redirect(url_for('dashboard'))

    event_details = check_event[0]
    form = UserEvent(name=event_details["name"], budget=event_details["budget"])

    if form.validate_on_submit():
        name = form.name.data
        budget = form.budget.data
        print(name, budget)
        update_event_by_id(event_details['id'], name, budget)
        flash(event_details["name"] + " updated !", "success")
        return redirect(url_for('get_specific_event', id=event_details["id"]))

    return render_template('update_event.html', form=form)


@app.route('/event_list/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_specific_event(id):
    user_email = current_user.email
    check_event = get_event_by_id(user_email, id)

    if len(check_event) == 0:
        flash("Event not found", "error")
        return redirect(url_for('dashboard'))

    delete_event_by_id(id)
    flash("Event deleted", "success")
    return redirect(url_for('event_list'))

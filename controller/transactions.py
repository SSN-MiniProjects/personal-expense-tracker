from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed
import datetime

from config.constants import ErrorConstants
from config.db import TransactionFormChoices
from flask_login import login_required, current_user
from flask import request, redirect, render_template, flash, url_for
from config.factory import AppFlask
from services.events import EventService
from services.transactions import TransactionService

app = AppFlask().instance


class Transaction(FlaskForm):
    transaction = FloatField(label="Expense Amount", validators=[
        InputRequired()
    ],
                             )
    mode = SelectField('Mode', choices=TransactionFormChoices.MODE, validators=[
        InputRequired()], render_kw={"placeholder": "Category"})
    category = SelectField('Category', choices=TransactionFormChoices.CATEGORY, validators=[
        InputRequired()])
    datestamp = DateField('Date of Expense', default=datetime.datetime.today, format='%Y-%m-%d', validators=[
        InputRequired()], render_kw={"placeholder": "Date"})
    note = StringField()
    event = SelectField()
    submit = SubmitField('Submit')

    def validate_transaction(self, transaction):
        if int(transaction.data) <= 0:
            raise ValidationError('Enter a valid amount')

    def validate_datestamp(self, field):
        if field.data > datetime.date.today():
            raise ValidationError("The date cannot be in the Future!")


class TransactionFile(FlaskForm):
    file = FileField('csv', validators=[
        FileAllowed(['csv'], 'CSV only!')])
    submit1 = SubmitField('submit')


def add_new_expense():
    event_id = request.args.get('event_id')
    user_email = current_user.email
    form = Transaction()
    events = EventService.get_list(user_email)

    l = [(None, None)]
    for event in events:
        pair = (event["id"], event["name"])
        if str(event["id"]) == event_id:
            l.insert(0, pair)
        else:
            l.append(pair)
    form.event.choices = l

    template = render_template('add_transaction.html', form=form, error="Nil")
    if not form.validate_on_submit():
        return template

    if form.validate_on_submit():
        transaction = form.transaction.data
        mode = form.mode.data
        category = form.category.data
        datestamp = form.datestamp.data
        note = form.note.data
        event = form.event.data

        if event == 'None':
            event = None
        else:
            event = int(event)

        TransactionService.create(user_email, transaction, mode, category, datestamp, note, event)
        flash("Expense added successfully", "success")
        if request.args.get('event_id') is None:
            return redirect(url_for('view_transaction'))
        else:
            return redirect(url_for('get_specific_event', id=event_id))


def view_all_expenses():
    query = request.args.get('options')
    filters = {
        "category": TransactionFormChoices.CATEGORY,
        "mode": TransactionFormChoices.MODE,
        "event": []
    }
    user_email = current_user.email
    user_events = EventService.get_list(user_email)
    for event in user_events:
        filters["event"].append(event["name"])
    temp_result = TransactionService.get_by_email(user_email)
    result = []
    if (query == 'dates_between'):
        input1 = datetime.datetime.strptime(request.args.get('input1'), "%Y-%m-%d")
        input2 = datetime.datetime.strptime(request.args.get('input2'), "%Y-%m-%d")
        for item in temp_result:
            item_date = datetime.datetime.strptime(str(item['datestamp']), "%Y-%m-%d")
            if input1 <= item_date <= input2:
                result.append(item)
    elif (query == 'amounts_range'):
        input1 = int(request.args.get('input1'))
        input2 = int(request.args.get('input2'))
        for item in temp_result:
            item_amount = item['transaction']
            if input1 <= item_amount <= input2:
                result.append(item)
    elif (query == 'mode'):
        input1 = request.args.get('input1')
        for item in temp_result:
            if item['mode'] == input1:
                result.append(item)
    elif (query == 'category'):
        input1 = request.args.get('input1')
        for item in temp_result:
            if item['category'] == input1:
                result.append(item)
    elif (query == 'event'):
        input1 = request.args.get('input1')
        for item in temp_result:
            if item['event'] == input1:
                result.append(item)
    else:
        result = temp_result
    return render_template('view_transaction.html', res=result, filters=filters)


def update_expense(id):
    user_email = current_user.email
    specific_transaction = TransactionService.get_by_email_id(user_email, id)
    if len(specific_transaction) == 0:
        flash(ErrorConstants.TRANSACTION_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    data = specific_transaction[0]
    form = Transaction(
        transaction=data["transaction"],
        mode=data["mode"],
        category=data["category"],
        datestamp=data["datestamp"],
        note=data["note"],
    )
    user_events = EventService.get_list(user_email)
    choice_list = [(None, None)]
    for event in user_events:
        pair = (event["id"], event["name"])
        if event["id"] == data["event"]:
            choice_list.insert(0, pair)
        else:
            choice_list.append(pair)
    form.event.choices = choice_list
    template = render_template('update_transaction.html', form=form)
    if not form.validate_on_submit():
        return template
    transaction = form.transaction.data
    mode = form.mode.data
    category = form.category.data
    datestamp = form.datestamp.data
    note = form.note.data
    event = form.event.data
    TransactionService.update(data['id'], user_email, transaction, mode, category, datestamp, note, event)
    flash("Transaction updated", "success")
    if request.args.get('event_id') is None:
        return redirect(url_for('view_transaction'))
    else:
        return redirect(url_for('get_specific_event', id=request.args.get('event_id')))


def delete_expense(id: int):
    user_email: str = current_user.email
    if not TransactionService.is_existed_by_id(user_email, id):
        flash(ErrorConstants.TRANSACTION_NOT_FOUND, "error")
        return redirect(url_for('dashboard'))
    TransactionService.delete(user_email, id)
    flash("Transaction deleted", "success")
    if request.args.get('event_id') is None:
        return redirect(url_for('view_transaction'))
    else:
        return redirect(url_for('get_specific_event', id=request.args.get('event_id')))

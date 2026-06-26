from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed
import datetime

from config.authentication import SessionUser
from config.constants import ErrorConstants, ExpenseHistoryFiterOptions, TransactionMessages, InputErrorMessages, \
    Templates, FlashMessageCategory
from config.db import TransactionFormChoices
from flask_login import current_user
from flask import request, redirect, render_template, flash, url_for
from config.factory import AppFlask
from services.events import EventService
from services.transactions import TransactionService

from services.expense_history_filter import ExpenseHistoryFilter

app = AppFlask().instance


class Transaction(FlaskForm):
    transaction = FloatField(label="Expense Amount", validators=[
        InputRequired()
    ])
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
        if not transaction.data or int(transaction.data) <= 0:
            self.transaction.errors.clear()
            raise ValidationError(InputErrorMessages.NOT_VALID_AMOUNT)

    def validate_datestamp(self, field):
        if field.data > datetime.date.today():
            raise ValidationError(InputErrorMessages.NOT_VALID_DATE)


class TransactionFile(FlaskForm):
    file = FileField('csv', validators=[
        FileAllowed(['csv'], 'CSV only!')])
    submit1 = SubmitField('submit')


def add_new_expense():
    query = request.args.get('event_id')

    event_id = query
    session_user : SessionUser = current_user
    login_id = session_user.get_login_id()
    form = Transaction()
    events = EventService.get_list(login_id)

    l = [(None, None)]
    for event in events:
        pair = (event["id"], event["name"])
        if str(event["id"]) == event_id:
            l.insert(0, pair)
        else:
            l.append(pair)
    form.event.choices = l

    if not form.validate_on_submit():
        return render_template('add_transaction.html', form=form)

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

    TransactionService.create(login_id, transaction, mode, category, datestamp, note, event)
    flash(TransactionMessages.EXPENSE_ADDED_SUCCESS, FlashMessageCategory.SUCCESS)
    if query is None:
        return redirect(url_for('view_transaction'))
    else:
        return redirect(url_for('get_specific_event', id=event_id))


def view_all_expenses():

    session_user: SessionUser = current_user
    login_id = session_user.get_login_id()
    user_events = EventService.get_list(login_id)

    filters = {
        "category": TransactionFormChoices.CATEGORY,
        "mode": TransactionFormChoices.MODE,
        "event": [event["name"] for event in user_events]
    }

    all_expenses = TransactionService.get_by_login_id(login_id)
    query = request.args.get('options')
    if query is None:
        return render_template(Templates.VIEW_TRANSACTION, res=all_expenses, filters=filters)

    first_argument = request.args.get('input1')
    second_argument = request.args.get('input2')

    expense_history_filter = ExpenseHistoryFilter(all_expenses)

    if query == ExpenseHistoryFiterOptions.DATES_BETWEEN:
        filtered_data = expense_history_filter.by_date_range(first_argument, second_argument)

    elif query == ExpenseHistoryFiterOptions.AMOUNTS_RANGE:
        filtered_data = expense_history_filter.by_amount_range(first_argument, second_argument)

    elif query == ExpenseHistoryFiterOptions.MODE:
        filtered_data = expense_history_filter.by_mode(first_argument)

    elif query == ExpenseHistoryFiterOptions.CATEGORY:
        filtered_data = expense_history_filter.by_category(first_argument)

    elif query == ExpenseHistoryFiterOptions.EVENT:
        filtered_data = expense_history_filter.by_event(first_argument)

    else:
        filtered_data = all_expenses

    return render_template(Templates.VIEW_TRANSACTION, res=filtered_data, filters=filters)


def update_expense(id):
    session_user : SessionUser = current_user
    login_id = session_user.get_login_id()
    specific_transaction = TransactionService.get_by_id(login_id, id)
    if len(specific_transaction) == 0:
        flash(ErrorConstants.TRANSACTION_NOT_FOUND, FlashMessageCategory.ERROR)
        return redirect(url_for('dashboard'))
    data = specific_transaction[0]
    form = Transaction(
        transaction=data["transaction"],
        mode=data["mode"],
        category=data["category"],
        datestamp=data["datestamp"],
        note=data["note"],
    )
    user_events = EventService.get_list(login_id)
    choice_list = [(None, None)]
    for event in user_events:
        pair = (event["id"], event["name"])
        if event["id"] == data["event"]:
            choice_list.insert(0, pair)
        else:
            choice_list.append(pair)
    form.event.choices = choice_list
    if not form.validate_on_submit():
        return render_template(Templates.UPDATE_TRANSACTION, form=form)
    transaction = form.transaction.data
    mode = form.mode.data
    category = form.category.data
    datestamp = form.datestamp.data
    note = form.note.data
    event = form.event.data
    TransactionService.update(data['id'], transaction, mode, category, datestamp, note, event)
    flash(TransactionMessages.EXPENSE_UPDATED_SUCCESS, FlashMessageCategory.SUCCESS)
    query = request.args.get('event_id')
    if query is None:
        return redirect(url_for('view_transaction'))
    else:
        return redirect(url_for('get_specific_event', id=query))


def delete_expense(id: int):
    session_user : SessionUser = current_user
    login_id = session_user.get_login_id()
    transaction = TransactionService.get_by_id(login_id, id)
    if not transaction:
        flash(ErrorConstants.TRANSACTION_NOT_FOUND, FlashMessageCategory.ERROR)
        return redirect(url_for('dashboard'))
    TransactionService.delete(id)
    flash(TransactionMessages.EXPENSE_DELETED, FlashMessageCategory.SUCCESS)
    query = request.args.get('event_id')
    if query is None:
        return redirect(url_for('view_transaction'))
    else:
        return redirect(url_for('get_specific_event', id=query))

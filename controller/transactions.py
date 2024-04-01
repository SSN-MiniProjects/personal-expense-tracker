from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
import datetime
from config.db import TransactionFormChoices
from flask_login import login_required

from config.factory import AppFlask

app = AppFlask().instance

class Transaction(FlaskForm):
    # login_id = StringField(render_kw={"placeholder": "Login ID"})
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
@app.route('/add_transaction', methods=['GET','POST'])
@login_required
def add_new_transaction():
    event_id = request.args.get('event_id')
    user_email = current_user.email
    form = Transaction()
    events = get_user_events(user_email)

    l = [(None, None)]
    for event in events:
        pair = (event["id"], event["name"])
        if str(event["id"]) == event_id:
            l.insert(0, pair)
        else:
            l.append(pair)
    form.event.choices = l
    if form.validate_on_submit():
        transaction = form.transaction.data
        mode = form.mode.data
        category = form.category.data
        datestamp = form.datestamp.data
        note = form.note.data
        event = form.event.data
        add_transaction(user_email, transaction, mode, category, datestamp, note, event)
        flash("Expense added successfully", "success")
        if request.args.get('event_id') is None:
            return redirect(url_for('view_transaction'))
        else:
            return redirect(url_for('get_specific_event', id= event_id))

    return render_template('add_transaction.html', form = form, error = "Nil")


@app.route('/view_transaction', methods=['GET', 'POST'])
@login_required
def view_transaction():
    query = request.args.get('options')
    filters = {
        "category": TransactionFormChoices.CATEGORY,
        "mode": TransactionFormChoices.MODE,
        "event": []
    }

    user_email = current_user.email
    user_events = get_user_events(user_email)
    for event in user_events:
        filters["event"].append(event["name"])

    temp_result = get_transactions(user_email)
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


@app.route('/view_transaction/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_specific_transaction(id):
    user_email = current_user.email
    check_transaction = get_transaction_by_id(user_email, id)

    if len(check_transaction) == 0:
        flash("Transaction not found", "error")
        return redirect(url_for('dashboard'))

    data = check_transaction[0]
    form = Transaction(
        transaction=data["transaction"],
        mode=data["mode"],
        category=data["category"],
        datestamp=data["datestamp"],
        note=data["note"],
    )
    user_events = get_user_events(user_email)
    l = [(None, None)]
    for event in user_events:
        pair = (event["id"], event["name"])
        if event["id"] == data["event"]:
            l.insert(0, pair)
        else:
            l.append(pair)

    form.event.choices = l

    if form.validate_on_submit():
        transaction = form.transaction.data
        mode = form.mode.data
        category = form.category.data
        datestamp = form.datestamp.data
        note = form.note.data
        event = form.event.data
        update_transaction_by_id(data['id'], user_email, transaction, mode, category, datestamp, note, event)
        flash("Transaction updated", "success")
        if request.args.get('event_id') is None:
            return redirect(url_for('view_transaction'))
        else:
            return redirect(url_for('get_specific_event', id=request.args.get('event_id')))

    return render_template('update_transaction.html', form=form)


@app.route('/view_transaction/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_specific_transaction(id):
    user_email = current_user.email
    check_transaction = get_transaction_by_id(user_email, id)

    if len(check_transaction) == 0:
        flash("Transaction not found", "error")
        return redirect(url_for('dashboard'))

    delete_transaction_by_id(id, user_email)
    flash("Transaction deleted", "success")
    if request.args.get('event_id') is None:
        return redirect(url_for('view_transaction'))
    else:
        return redirect(url_for('get_specific_event', id=request.args.get('event_id')))

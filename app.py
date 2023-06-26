from flask import Flask, render_template, url_for, redirect, flash, make_response, request,send_file
import flask
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from datetime import date,datetime
from reportlab.lib import colors  
from reportlab.lib.pagesizes import letter, inch  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from werkzeug.utils import secure_filename
import pandas
import datetime

from config.db import (
    init_db
)

import humanize

from models.login_credentials import (
    get_user_by_email,
    get_user_by_id,
    add_user_credential,
    get_user_count
)

from models.users_profiles import (
    add_user_profile,
    get_spent_and_budget,
    update_user_profile,
    get_user_profile
)

from models.transactions import (
    add_transaction,
    get_transactions,
    get_day_expense,
    get_month_expense,
    get_year_expense,
    get_transactions_by_event,
    get_transaction_by_id,
    update_transaction_by_id,
    delete_transaction_by_id
)

from models.users_events import (
    add_user_event,
    get_user_events,
    get_event_by_id,
    update_event_by_id,
    delete_event_by_id
)

from forms.login import (
    Login
)

from forms.register import (
    Register
)

from forms.profile import (
    UserProfile
)

from forms.events import (
    UserEvent
)

from forms.transaction import (
    Transaction, TransactionFile
)


from utilities.visualisations import (
    get_month_graph_data, get_year_graph_data, get_category_graph_data
)

import hashlib

from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'B7-1A3E'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "error"

init_db()


class SessionUser:   

    def __init__(self, id, email):
        self.id = id
        self.email = email

    def to_json(self):        
        return {
                "email": self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)

@login_manager.user_loader
def load_user(id):
    user = get_user_by_id(id)
    if user is None:
        return None
    usr_obj = SessionUser(user["id"], user["email"])
    return usr_obj


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    error = None
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        hashedPassword = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()
        if user is not None:
            if user["password"] == hashedPassword:
                usr_obj = SessionUser(user["id"], user["email"])
                login_user(usr_obj, remember=True)
                next = flask.request.args.get('next')
                resp = make_response(redirect(next or url_for('dashboard')))
                resp.set_cookie('email', user['email'])
                flash("Logged In","success")
                return resp

            else:
                flash("Incorrect Password","error")
        else:
            flash("Account Not Found","error")

    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    user_email = request.cookies.get('email')

    Daily = get_month_graph_data(user_email, date.today())
    Monthly = get_year_graph_data(user_email, date.today())
    Category = get_category_graph_data(user_email, date.today())
    
    result = get_spent_and_budget(user_email)
    total_spent = result["total_expense"]
    budget = result["budget"]
    budget_percentage = round(total_spent/budget*100,2) if budget > 0 else -1
    user_count = get_user_count()
    today_expense = get_day_expense(user_email, date.today().strftime("%Y-%m-%d"))
    current_month_expense = get_month_expense(user_email, date.today().strftime("%Y-%m-%d"))
    current_year_expense = get_year_expense(user_email, date.today().strftime("%Y-%m-%d"))

    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    
    CardData = {
        "TotalExpense": humanize.intcomma(total_spent),
        "TodayExpense" : humanize.intcomma(today_expense),
        "CurrentMonthExpense" : humanize.intcomma(current_month_expense),
        "CurrentYearExpense" : humanize.intcomma(current_year_expense),
        "BudgetPercentage": budget_percentage,
        "UserCount": humanize.intcomma(user_count),
    }

    Month_vice_data = [month_names[i-1] for i in Monthly[0]]

    GraphData = {
        "ChartArea": {"labels": Daily[0], "data": Daily[1]},
        "ChartPie": {"labels": Category[0], "data": Category[1]},
        "ChartBar": {"labels": Month_vice_data, "data": Monthly[1]}
    }
    return render_template('dashboard.html', GraphData = GraphData, CardData = CardData)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged Out', 'success')
    resp = make_response(redirect(location=url_for('login')))
    resp.set_cookie('email', expires=0)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        entered_email = form.email.data
        entered_password = form.password.data

        existing_email = get_user_by_email(entered_email)
        if existing_email is not None:
            flash('This email already exists', 'error')
        else:
            resp = make_response(render_template('email_confirmation.html', email= entered_email))
            resp.set_cookie('email', entered_email)

            # insert the new user credential
            add_user_credential(entered_email, entered_password)

            res = get_user_by_email(entered_email)
            login_id = res["id"]

            # insert new user profile for created credential
            add_user_profile(login_id)
            resp = make_response(redirect(location=url_for('login')))

            return resp

    return render_template('register.html', form=form)


@app.route('/add_transaction', methods=['GET','POST'])
@login_required
def add_new_transaction():
    event_id = request.args.get('event_id') 
    user_email = request.cookies.get('email')
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
        return redirect(url_for('view_transaction'))

    return render_template('add_transaction.html', form = form, error = "Nil")


@app.route('/add_event', methods=['GET','POST'])
@login_required
def add_event():
    form = UserEvent()
    user_email = request.cookies.get('email')

    if form.validate_on_submit():
        name = form.name.data
        budget = form.budget.data
        add_user_event(user_email, name, budget)
        flash("Event added successfully", "success")
        return redirect(url_for('event_list'))

    return render_template('add_event.html', form = form)



@app.route('/customize', methods=['GET','POST'])
@login_required
def customize():
    user_email = request.cookies.get('email')
    details = get_user_profile(user_email)
    
    form = UserProfile(
        name = details["name"], 
        budget = details["budget"],
        phone = details["phone"],
        profession = details["profession"],
        alert = details["alert"])
    
    if form.validate_on_submit():
        name = form.name.data
        budget = float(form.budget.data)
        phone = form.phone.data
        profession = form.profession.data
        alert = form.alert.data
        update_user_profile(user_email, name, budget, phone, profession, alert)
        flash("Profile updated successfully", "success")
        return redirect(url_for('customize'))

    return render_template('customize.html', form = form)
 
@app.route('/view_transaction', methods=['GET','POST'])
@login_required
def view_transaction():
    query = request.args.get('options')
    filters = {
        "category" : ["Food","Health", "Transport", "Shopping", "Entertainment", "Bills","Debt Payment","Other"],
        "mode" : ['Online', 'Cash']
    }
    
    user_email = request.cookies.get('email')
    temp_result = get_transactions(user_email)
    result = []
    if(query=='dates_between'):
        input1 = datetime.datetime.strptime(request.args.get('input1'),"%Y-%m-%d")
        input2 = datetime.datetime.strptime(request.args.get('input2'),"%Y-%m-%d")
        for item in temp_result:
            item_date =  datetime.datetime.strptime(str(item['datestamp']),"%Y-%m-%d")
            if input1 <= item_date <= input2:
                result.append(item)
    elif(query=='amounts_range'):
        input1 = int(request.args.get('input1'))
        input2 = int(request.args.get('input2'))
        for item in temp_result:
            item_amount = item['transaction']
            if input1 <= item_amount <= input2:
                result.append(item)
    elif (query=='mode'):
        input1 = request.args.get('input1')
        for item in temp_result:
            if item['mode'] == input1:           
                result.append(item)
    elif (query=='category'):
        input1 = request.args.get('input1')
        for item in temp_result:
            if item['category'] == input1:           
                result.append(item)
    else:
        result=temp_result


    return render_template('view_transaction.html',res= result, filters = filters)       


@app.route('/event_list', methods=['GET'])
@login_required 
def event_list():
    user_email = request.cookies.get('email')
    events = get_user_events(user_email)
    return render_template("event_list.html", events = events)

@app.route('/event_list/<int:id>', methods=['GET'])
@login_required 
def get_specific_event(id):
    user_email = request.cookies.get('email')
    event_details = get_event_by_id(id)[0]
    event_transactions = get_transactions_by_event(id)
    return render_template("view_event.html", event = event_details, transactions=event_transactions)


@app.route('/event_list/<int:id>/update', methods=['GET', 'POST'])
@login_required 
def update_event(id):
    event_details = get_event_by_id(id)[0]
    form = UserEvent(name = event_details["name"], budget = event_details["budget"])
    
    if form.validate_on_submit():
        name = form.name.data
        budget = form.budget.data
        print(name, budget)
        update_event_by_id(event_details['id'], name, budget)
        flash(event_details["name"] + " updated !", "success")
        return redirect(url_for('get_specific_event', id= event_details["id"]))

    return render_template('update_event.html', form = form)

@app.route('/view_transaction/<int:id>/update', methods=['GET', 'POST'])
@login_required 
def update_specific_transaction(id):
    data = get_transaction_by_id(id)[0]
    user_email = request.cookies.get('email')
    form = Transaction(
        transaction = data["transaction"], 
        mode = data["mode"],
        category = data["category"],
        datestamp = data["datestamp"],
        note = data["note"],
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
        update_transaction_by_id(data['id'], user_email,transaction, mode, category, datestamp, note, event)
        flash("Transaction updated", "success")
        return redirect(url_for('event_list'))

    return render_template('update_transaction.html', form = form)



@app.route('/view_transaction/<int:id>/delete', methods=['GET', 'POST'])
@login_required 
def delete_specific_transaction(id):
    user_email = request.cookies.get('email')
    delete_transaction_by_id(id, user_email)
    flash("Transaction deleted", "success")
    return redirect(url_for('view_transaction'))

@app.route('/event_list/<int:id>/delete', methods=['GET', 'POST'])
@login_required 
def delete_specific_event(id):
    delete_event_by_id(id)
    flash("Event deleted", "success")
    return redirect(url_for('event_list'))
 
# @app.route('/generate_report', methods=['GET'])
# def generate_report():

#     email = request.cookies.get('email')

#     # creating a pdf file to add tables 
#     file_name = f"Report-{email}.pdf"  
#     my_doc = SimpleDocTemplate(file_name, pagesize = letter)  
#     my_obj = []

#     # defining Data to be stored on table  
    
#     my_data = [  
#     ["ID", "Expense Amount", "Mode", "Date", "Note"],
#     ]  
#     res = get_transactions(email)
#     if res is None:
#         flash("Please add transactions", "error")

#     for i in range(len(res)):
#         temp = [i,res[i]["transaction"],res[i]["mode"],res[i]["datestamp"],res[i]["note"]]
#         my_data.append(temp)

#     # Creating the table with 6 rows
#     row_count = len(res) + 1  
#     my_table = Table(my_data, 1 * [1.6 * inch], row_count * [0.5 * inch])  
#     # setting up style and alignments of borders and grids  
#     my_table.setStyle(  
#     TableStyle(  
#         [  
#             ("ALIGN", (1, 1), (0, 0), "LEFT"),  
#             ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
#             ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),  
#             ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
#             ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),  
#             ("BOX", (0, 0), (-1, -1), 2, colors.black),  
#         ]  
#     )  
#     )  
#     my_obj.append(my_table)  
#     my_doc.build(my_obj)
#     path = file_name
#     return send_file(path, as_attachment=True)
    

if __name__ == "__main__":
	app.run(debug=True)

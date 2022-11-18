from forms import LoginForm, RegisterForm, Transaction, Customize
from flask import Flask, render_template, url_for, redirect, flash, make_response, request,send_file
import flask
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from sendgrid_integration import SendGrid
from database import insert_user_credential, insert_user_profile, fetchUserByEmail, fetchUserById, insert_user_transaction,fetch_user_transactions,global_view_query, update_user_customize, initialise
from utility import get_month_graph_data,get_year_graph_data,get_card_details,get_category_graph_data, get_card_details
from datetime import date
from reportlab.lib import colors  
from reportlab.lib.pagesizes import letter, inch  
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'B7-1A3E'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "error"

sendgrid_obj = SendGrid()


class User:   

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
def load_user(user_id):
    user = fetchUserById(user_id)
    if user == []:
        return None
    user = user[0]
    usr_obj = User(user["ID"], user["EMAIL"])
    return usr_obj


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = fetchUserByEmail(form.email.data)
        if user != []:
            user = user[0]
            if user["PASSWORD"] == form.password.data:
                usr_obj = User(user["ID"], user["EMAIL"])
                login_user(usr_obj)
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('email', user['EMAIL'])
                return resp

            else:
                error = "Invalid Credentials"
        else:
            error = "There is no account registered with this email"

    return render_template('login.html', form=form, error = error)

@app.route('/dashboard')
@login_required
def dashboard():
    useremail = request.cookies.get('email')
    datestr = date.today().strftime("%Y-%m-%d")
    Monthly = get_month_graph_data(useremail,date.today())
    Annual = get_year_graph_data(useremail,date.today())
    Category = get_category_graph_data(useremail,date.today())
    Cards= get_card_details(useremail)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if(Cards[0]['BUDGET']==0):
        Cards[0]['BUDGET']=1
    CardData={
        "MonthlyExpense":Cards[0]['TOTAL_SPENT'],
        "AnnualExpense":sum(Annual[1]),
        "BudgetPercentage":Cards[0]['TOTAL_SPENT']/Cards[0]['BUDGET']*100,
        "UserCount":Cards[1],
    }
    Month_vice_data=[month_names[i-1] for i in Annual[0]]
    GraphData={
        "ChartArea":{"labels": Monthly[0],"data":Monthly[1]},
        "ChartPie":{"labels":Category[0],"data":Category[1]},
        "ChartBar":{"labels":Month_vice_data,"data":Annual[1]}
    }
    return render_template('dashboard.html',GraphData=GraphData,CardData=CardData)


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    resp = make_response(redirect(location=url_for('login')))
    resp.set_cookie('email', expires=0)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        entered_email = form.email.data
        entered_password = form.password.data
        resp = make_response(render_template('email_confirmation.html', email= entered_email))
        resp.set_cookie('email', entered_email)
        resp.set_cookie('password', entered_password, max_age=3000)
        otp = sendgrid_obj.confirmation_mail(entered_email)
        if otp == None:
            return render_template('register.html', form=form, error="Please try again!")
        
        resp.set_cookie('otp', str(otp),max_age=3000)
        return resp

    return render_template('register.html', form=form)


@app.route('/confirm_email', methods=['POST'])
def confirm_email():
    otp_generated = request.cookies.get('otp')
    # otp_generated = 5000
    email = request.cookies.get('email')
    password = request.cookies.get('password')
    if otp_generated is None:
        print("otp expired")
        return render_template('email_confirmation.html', email= email, expired="OTP expired!")
    
    otp_received = request.form['otp']

    if str(otp_generated) == otp_received:
        # insert the new user credential
        insert_user_credential(email, password)

        res = fetchUserByEmail(email)
        login_id = res[0]["ID"]

        # insert new user profile for created credential
        insert_user_profile(login_id)
        resp = make_response(redirect(location=url_for('login')))

        # delete the otp and password cookies before rendering the page
        resp.set_cookie('password', expires=0)
        resp.set_cookie('otp', expires=0)
        return resp

    else:
        resp = make_response(render_template('email_confirmation.html', email= email, error="OTP mismatch! Retry"))
        return resp

@login_required
@app.route('/add_transaction', methods=['GET','POST'])
def add_transaction():
    form = Transaction();
    useremail = request.cookies.get('email')
    if form.validate_on_submit():
        transaction = form.transaction.data
        mode = form.mode.data
        category = form.category.data
        datestamp = form.datestamp.data
        note = form.note.data 
        insert_user_transaction(useremail, transaction, mode, category, datestamp, note)
        result = get_card_details(useremail)[0]
        total_expense = result["TOTAL_SPENT"]
        budget = result["BUDGET"]
        alert_mail = None
        if total_expense > budget:
            alert_mail = sendgrid_obj.alert_overbudget(useremail, budget, total_expense)
        
        if alert_mail:
            print("success: sending alert mail")
        else:
            print("failed: sending alert mail")
        
        flash("Expense added successfully", "success")
        return redirect(url_for('home'))
    return render_template('add_transaction.html', form=form, error = "Nil")

@app.route('/customize', methods=['GET','POST'])
@login_required
def add_customization():
    form = Customize();
    useremail = request.cookies.get('email')
    if form.validate_on_submit():
        name = form.name.data
        budget = form.budget.data
        phone = form.phone.data
        profession = form.profession.data
        alert = form.alert.data
        update_user_customize(useremail, name, budget, phone, profession, alert)
        flash("Profile updated successfully", "success")
        return redirect(url_for('home'))
    return render_template('customize.html', form=form)
 
    
@app.route('/view_transaction', methods=['GET','POST'])
def view_transaction():
    return render_template('view_transaction.html',fetch_user_transactions= fetch_user_transactions)

@app.route('/base', methods=['GET'])
def view_base():
    return render_template('base.html')

@app.route('/ref', methods=['GET'])
def view_ref():
    return render_template('reference.html')
        

@app.route('/generate_report', methods=['GET'])
def genrate_report():
    # creating a pdf file to add tables 
    file_name = "Report.pdf"  
    my_doc = SimpleDocTemplate(file_name, pagesize = letter)  
    my_obj = []  
    # defining Data to be stored on table  
    email = request.cookies.get('email')
    my_data = [  
    ["ID", "Amount","Mode","Date",	"Note"],
    ]  
    res = fetch_user_transactions(email)
    if res == []:
        flash("Please add transactions", "error")
        return redirect('home')
    for i in range(len(res)):
        temp = [i,res[i]["TRANSACTION"],res[i]["MODE"],res[i]["DATESTAMP"],res[i]["NOTE"]]
        my_data.append(temp)
    # Creating the table with 6 rows
    row_count = len(res) + 1  
    my_table = Table(my_data, 1 * [1.6 * inch], row_count * [0.5 * inch])  
    # setting up style and alignments of borders and grids  
    my_table.setStyle(  
    TableStyle(  
        [  
            ("ALIGN", (1, 1), (0, 0), "LEFT"),  
            ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
            ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),  
            ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),  
            ("BOX", (0, 0), (-1, -1), 2, colors.black),  
        ]  
    )  
    )  
    my_obj.append(my_table)  
    my_doc.build(my_obj)
    path = file_name
    return send_file(path, as_attachment=True)
    

app.run("0.0.0.0", 5000,debug=True)

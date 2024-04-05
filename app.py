import os

from dotenv import load_dotenv

from config.authentication import SessionUser
from models.users_credentials import UserModel

load_dotenv()

from controller.authentication import registration, start_login, start_logout
from controller.dashboard import view_dashboard
from controller.events import create_event, get_event, show_event_list, update_specific_event, delete_event
from controller.profile import update_profile
from controller.transactions import add_new_expense, view_all_expenses, update_expense, delete_expense

from flask_bootstrap import Bootstrap
from config.constants import SecurityConstants
from config.db import init_db
from config.factory import AppFlask, LoginManagerFlask
from flask_login import login_required

init_db()
app = AppFlask().instance
Bootstrap(app)
app.config['SECRET_KEY'] = SecurityConstants.APP_SECRET_KEY
login_manager = LoginManagerFlask().instance
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(id):
    user = UserModel.find_by_id(id)
    if not user:
        return None
    usr_obj = SessionUser(user["id"], user["email"])
    return usr_obj


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    return registration()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return start_login()


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    return start_logout()


@app.route('/dashboard')
@login_required
def dashboard():
    return view_dashboard()


@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    return create_event()


@app.route('/event_list', methods=['GET'])
@login_required
def event_list():
    return show_event_list()


@app.route('/event_list/<int:id>', methods=['GET'])
@login_required
def get_specific_event(id):
    return get_event(id)


@app.route('/event_list/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    return update_specific_event(id)


@app.route('/event_list/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_specific_event(id):
    return delete_event(id)


@app.route('/customize', methods=['GET', 'POST'])
@login_required
def customize():
    return update_profile()


@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_new_transaction():
    return add_new_expense()


@app.route('/view_transaction', methods=['GET', 'POST'])
@login_required
def view_transaction():
    return view_all_expenses()


@app.route('/view_transaction/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_specific_transaction(id):
    return update_expense(id)


@app.route('/view_transaction/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_specific_transaction(id):
    return delete_expense(id)


if __name__ == "__main__":
    app.run(debug=bool(os.getenv("DEBUG")))

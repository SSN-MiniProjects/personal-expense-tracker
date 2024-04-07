import flask
from flask import make_response, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from config.authentication import SessionUser
from config.constants import ErrorConstants
from config.factory import AppFlask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired

from services.users import UserService


class LoginForm(FlaskForm):
    email = StringField('Email',
                        id='email_login',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='password_login',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='password_create',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


app = AppFlask().instance


def registration():
    form = RegisterForm()
    register_template = 'register.html'
    if not form.validate_on_submit():
        return render_template(register_template, form=form)
    email = form.email.data
    password = form.password.data
    if UserService.is_existed(email):
        flash(ErrorConstants.DUPLICATE_EMAIL_REG, 'error')
        return render_template(register_template, form=form)
    UserService.register(email, password)
    return make_response(redirect(location=url_for('login')))


def start_login():
    form = LoginForm()
    login_template = 'login.html'
    if not form.validate_on_submit():
        return render_template(login_template, form=form)
    email = form.email.data
    if not UserService.is_existed(email):
        flash(ErrorConstants.ACCOUNT_NOT_FOUND, "error")
        return render_template(login_template, form=form)
    password = form.password.data
    if not UserService.validate_password(email, password):
        flash(ErrorConstants.WRONG_PASSWORD, "error")
        return render_template(login_template, form=form)
    user = UserService.get(email)
    usr_obj = SessionUser(user["id"], user["email"])
    login_user(usr_obj, remember=True)
    redirecting_page = redirect(flask.request.args.get('next') or url_for('dashboard'))
    success_response = make_response(redirecting_page)
    flash("Logged In", "success")
    return success_response


def start_logout():
    logout_user()
    flash('Logged Out', 'success')
    return redirect(url_for('login'))

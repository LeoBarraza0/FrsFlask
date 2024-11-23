from flask import render_template, flash, redirect, request, url_for 
from Login.app.auth.forms import RegistrationForm, LoginForm
from Login.app.auth import authentication 
from Login.app.auth.models import User 
from flask_login import login_user, logout_user, login_required, current_user 
from bs4 import BeautifulSoup 
from lxml import etree 
import requests 
@authentication.route("/register", methods=["GET", "POST"]) 
def register_user(): 
    if current_user.is_authenticated: 
        flash("You are already logged in the system") 
        return redirect(url_for("authentication.log_in_user")) 
    form = RegistrationForm() 
    if form.validate_on_submit(): 
        User.create_user( user=form.name.data, email=form.email.data, password=form.password.data ) 
        flash("Registration Done...") 
        return redirect(url_for("authentication.log_in_user")) 
    return render_template("registration.html", form=form) 
@authentication.route("/") 
def index(): 
    return render_template("menuprod.html") 

@authentication.route("/login", methods=["GET", "POST"]) 
def log_in_user(): 
    if current_user.is_authenticated: 
        flash("You are already logged in the system") 
        return redirect(url_for("authentication.homepage")) 
    form = LoginForm() 
    if form.validate_on_submit(): 
        user = User.query.filter_by(user_email=form.email.data).first() 
        if not user or not user.check_password(form.password.data): 
            flash("Invalid credentials...") 
            return redirect(url_for("authentication.log_in_user")) 
        login_user(user, form.stay_loggedin.data) 
        return redirect(url_for("authentication.homepage")) 
    return render_template("login.html", form=form) 


@authentication.route("/homepage") 
@login_required 
def homepage(): 
    return render_template('homepage.html') 
@authentication.route("/logout", methods=["GET"]) 
@login_required 
def log_out_user(): 
    logout_user() 
    return redirect(url_for("authentication.log_in_user")) 

@authentication.app_errorhandler(404) 
def page_not_found(error): 
    return render_template('404.html'), 404

@authentication.route("/comprar") 
@login_required 
def comprar(): 
    return render_template('checkout.html') 

@authentication.route("/pago") 
@login_required 
def pagar(): 
    return render_template('pago.html') 

@authentication.route("/productos") 
@login_required 
def productos(): 
    return render_template('productos.html')

@authentication.route("/ver") 
@login_required 
def ver(): 
    return render_template('productos2.html') 
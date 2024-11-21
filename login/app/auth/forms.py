from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User

def email_exists(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError("Email already exists. !!!!")




class RegistrationForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(4,16, message="De 4 a 16 letras")])
    email = StringField("E-mail", validators=[DataRequired(), Email(), email_exists])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm", message="Password must match!!!")])
    confirm = PasswordField("Confirm", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email= StringField("E-mail", validators=[DataRequired(), Email()])
    password= PasswordField("Password", validators=[DataRequired()])
    stay_loggedin= BooleanField("Remember Me!")
    submit= SubmitField("Login")


class ScrapyForm(FlaskForm):
    search_article = StringField("Article", validators=[DataRequired()])
    submit = SubmitField("Search Article")
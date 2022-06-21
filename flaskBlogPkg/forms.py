from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, BooleanField

__all__ = ("RegistrationForm", "LoginForm")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired(), validators.Length(min=2, max=15)])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    #for multiplier of regex rule use {0,} or '*'
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=2, max=15),
                                                     validators.Regexp('^[a-zA-Z0-9@\$\_\#]{0,}$')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.InputRequired(), validators.EqualTo('password')])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[validators.InputRequired(), validators.Length(min=2, max=15)])
    password = PasswordField('Password', validators=[validators.InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

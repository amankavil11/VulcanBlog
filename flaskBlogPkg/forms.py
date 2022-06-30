from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, BooleanField
from flaskBlogPkg.models import user

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
    
    def validate_username(self, username):
        User = user.query.filter_by(username=username.data).first()
        if User:
            raise validators.ValidationError('That username already exists. Please choose another username')
    
    def validate_email(self, email):
        User = user.query.filter_by(email=email.data).first()
        if User:
            raise validators.ValidationError('An account with that email already exists.')


class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[validators.InputRequired(), validators.Length(min=2, max=40)])
    password = PasswordField('Password', validators=[validators.InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

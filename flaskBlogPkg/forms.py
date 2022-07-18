from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, PasswordField, SubmitField, BooleanField, TextAreaField
from flaskBlogPkg.models import user
from flask_login import current_user


#Below allows you to dictate what can be imported when '*' is used in import statement
#__all__ = ("RegistrationForm", "LoginForm")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired(), validators.Length(min=2, max=15)])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    #for multiplier of regex rule use {0,} or '*'
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=2, max=15),
                                                     validators.Regexp('^[a-zA-Z0-9@\$\_\#]{0,}$')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.InputRequired(), validators.EqualTo('password')])
    submit = SubmitField("Sign Up")
    
    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        User = user.query.filter_by(username=username.data).first()
        if User:
            raise validators.ValidationError('That username already exists. Please choose another username')
    
    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        User = user.query.filter_by(email=email.data).first()
        if User:
            raise validators.ValidationError('An account with that email already exists.')


class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[validators.InputRequired(), validators.Length(min=2, max=40)])
    password = PasswordField('Password', validators=[validators.InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired(), validators.Length(min=2, max=15)])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'heic'])])
    submit = SubmitField("Update")
    
    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        if username.data != current_user.username:
            User = user.query.filter_by(username=username.data).first()
            if User:
                raise validators.ValidationError('That username already exists. Please choose another username')
    
    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        if email.data != current_user.email:
            User = user.query.filter_by(email=email.data).first()
            if User:
                raise validators.ValidationError('An account with that email already exists.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[validators.InputRequired()])
    content = TextAreaField('Content', validators=[validators.InputRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    submit = SubmitField('Request Password Reset')
    
    @staticmethod
    def validate_email(self, email):
        User = user.query.filter_by(email=email.data).first()
        if not User:
            raise validators.ValidationError('There is no account associated with that email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=2, max=15),
                                                     validators.Regexp('^[a-zA-Z0-9@\$\_\#]{0,}$')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.InputRequired(), validators.EqualTo('password')])
    submit = SubmitField("Reset Password")

from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField


class PostForm(FlaskForm):
    title = StringField('Title', validators=[validators.InputRequired()])
    content = TextAreaField('Content', validators=[validators.InputRequired()])
    submit = SubmitField('Post')

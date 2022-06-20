from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import *
from datetime import datetime

#template_folder **kwargs is used to change default "template" folder name, in this case to HTML templates
app = Flask(__name__, template_folder="HTML templates")

app.config['SECRET_KEY'] = '34665436c8c5f81e7aadc5b9b015089c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///site.db'
db = SQLAlchemy(app)


#try to always use lowercase class(aka models) names when using SQLAlchemy
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    # 'Post' references model name, hence the capitalization
    posts = db.relationship('post', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #'user.id' references table name which is automatically lowercase in SQLAlchemy
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author':"Abe Mankavil",
        'title':"Post #1",
        'content':"Hello World! First Flask Blog Post",
        "post_date":"4/20/22"
    },
    {
        'author':"Thomas Jones",
        'title':"Post #2",
        'content':"Hello World! Second Flask Blog Post",
        "post_date":"5/1/22"
    }
]


@app.route("/")
@app.route("/home")
def Home():
    return render_template('home.html', post=posts)


@app.route("/about")
def About():
    return render_template('about.html', title="About")


@app.route("/register", methods=['GET', 'POST'])
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('Home'))
    #print(form.errors) ===> use to snuff out errors in forms
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('Home'))
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    #default port 5000 on MACOSX in use for airplay
    app.run(debug=True, port=8001)

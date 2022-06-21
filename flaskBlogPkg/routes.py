from flask import Flask, render_template, url_for, flash, redirect
from flaskBlogPkg import app
from flaskBlogPkg.forms import *
from flaskBlogPkg.models import user, post

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

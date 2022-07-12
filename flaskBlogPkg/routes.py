import os
from flask import Flask, render_template, url_for, flash, redirect, request
from flaskBlogPkg import app, db, bcrypt
from flaskBlogPkg.forms import *
from flaskBlogPkg.models import user, post
from flask_login import login_user, current_user, logout_user, login_required
import secrets


@app.route("/")
@app.route("/home")
def Home():
    posts = post.query.all()
    return render_template('home.html', post=posts)


@app.route("/about")
def About():
    return render_template('about.html', title="About")


@app.route("/register", methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # noinspection PyArgumentList
        User = user(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(User)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You\'re now able to login!', 'success')
        return redirect(url_for('Login'))
    #print(form.errors) ===> use to snuff out errors in forms
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = LoginForm()
    if form.validate_on_submit():
        User_Email = user.query.filter_by(email=form.username.data).first()
        User = user.query.filter_by(username=form.username.data).first()
        if User_Email:
            User = User_Email
        if User and bcrypt.check_password_hash(User.password, form.password.data):
            login_user(User, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('Home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def LogOut():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('Home'))


def save_pic(form_pic):
    rand_hex = secrets.token_hex(8)
    # underscore is way of discarding unused variable that wd be produced by splittext function
    _, file_ext = os.path.splitext(form_pic.filename)
    pic_fn = rand_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
    form_pic.save(picture_path)
    prev_pic = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if current_user.image_file != 'default.png':
        os.remove(prev_pic)
    return pic_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def Account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_pic(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def New_Post():
    form = PostForm()
    if form.validate_on_submit():
        Post = post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(Post)
        db.session.commit()
        flash('Post has been created', 'success')
        return redirect((url_for('Home')))
    return render_template('create_post.html', title='New Post', form=form)
    

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def IndividualPost(post_id):
    pass
    Post = post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=Post)


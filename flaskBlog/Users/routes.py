from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskBlog import db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from flaskBlog.Users.forms import *
from flaskBlog.models import user, post
from flaskBlog.Users.utils import save_pic, send_reset_email

users = Blueprint('Users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('Main.Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # noinspection PyArgumentList
        User = user(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(User)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You\'re now able to login!', 'success')
        return redirect(url_for('Users.Login'))
    #print(form.errors) ===> use to snuff out errors in forms
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('Main.Home'))
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
            return redirect(next_page) if next_page else redirect(url_for('Main.Home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def LogOut():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('Main.Home'))


@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('Users.Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def User_Posts(username):
    user_id = user.query.filter_by(username=username).first_or_404().id
    page = request.args.get('page', 1, type=int)
    posts = post.query.filter_by(user_id=user_id).order_by(post.date_posted.desc()) \
        .paginate(per_page=2, page=page)
    return render_template('user_posts.html', post=posts, user=username)


@users.route("/reset_password", methods=['GET', 'POST'])
def Reset_Request():
    if current_user.is_authenticated:
        return redirect(url_for('Main.Home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        User = user.query.filter_by(email=form.email.data).first()
        send_reset_email(User)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('Users.Login'))
    
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def Reset_Token(token):
    if current_user.is_authenticated:
        return redirect(url_for('Main.Home'))
    User = user.verify_reset_token(token)
    if not User:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('Users.Reset_Request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.password = hashed_password
        db.session.commit()
        flash(f'Account info for {User.username} has been updated!', 'success')
        return redirect(url_for('Users.Login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

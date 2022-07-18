import os
import secrets
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskBlogPkg import app, db, bcrypt, mail
from flaskBlogPkg.forms import *
from flaskBlogPkg.models import user, post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def Home():
    #posts = post.query.all()
    #posts = post.query.order_by(post.id.desc())
    page = request.args.get('page', 1, type=int)
    posts = post.query.order_by(post.date_posted.desc()).paginate(per_page=10, page=page)
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
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def IndividualPost(post_id):
    Post = post.query.get_or_404(post_id)
    return render_template('post.html', title=Post.title, post=Post)


@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def Edit_Post(post_id):
    Post = post.query.get_or_404(post_id)
    if Post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        Post.title = form.title.data
        Post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('IndividualPost', post_id=Post.id))
    elif request.method == 'GET':
        form.title.data = Post.title
        form.content.data = Post.content
    
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def Delete_Post(post_id):
    Post = post.query.get_or_404(post_id)
    if Post.author != current_user:
        abort(403)
    db.session.delete(Post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('Home'))


@app.route("/user/<string:username>")
def User_Posts(username):
    user_id = user.query.filter_by(username=username).first_or_404().id
    page = request.args.get('page', 1, type=int)
    posts = post.query.filter_by(user_id=user_id).order_by(post.date_posted.desc()) \
        .paginate(per_page=2, page=page)
    return render_template('user_posts.html', post=posts, user=username)


def send_reset_email(User):
    token = User.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[User.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('Reset_Token', token=token, _external=True)}

If you did not make this request then simply ignore this email
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def Reset_Request():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        User = user.query.filter_by(email=form.email.data).first()
        send_reset_email(User)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('Login'))
    
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def Reset_Token(token):
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    User = user.verify_reset_token(token)
    if not User:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('Reset_Request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.password = hashed_password
        db.session.commit()
        flash(f'Account info for {User.username} has been updated!', 'success')
        return redirect(url_for('Login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

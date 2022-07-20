import os
import secrets
from flask_mail import Message
from flask import url_for, flash
from flaskBlog import app, mail
from flask_login import current_user
from flaskBlog.models import user, post


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


def send_reset_email(User):
    token = User.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[User.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('Users.Reset_Token', token=token, _external=True)}

If you did not make this request then simply ignore this email
'''
    mail.send(msg)

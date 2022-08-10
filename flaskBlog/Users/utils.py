import os
import secrets
from flask_mail import Message
from flask import url_for
from flaskBlog import mail
from flask_login import current_user
from decouple import config
import boto3 as boto


# def save_pic(form_pic):
#     rand_hex = secrets.token_hex(8)
#     # underscore is way of discarding unused variable that wd be produced by splittext function
#     _, file_ext = os.path.splitext(form_pic.filename)
#     pic_fn = rand_hex + file_ext
#     picture_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fn)
#     form_pic.save(picture_path)
#     prev_pic = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
#     if current_user.image_file != 'default.png':
#         os.remove(prev_pic)
#     return pic_fn

def save_pic(form_pic):
    rand_hex = secrets.token_hex(8)
    # underscore is way of discarding unused variable that wd be produced by splittext function
    _, file_ext = os.path.splitext(form_pic.filename)
    contentType = file_ext.lower()
    if contentType == '.jpg':
        contentType = 'jpeg'
    file_bytes = form_pic.stream.read()
    pic_fn = rand_hex + file_ext
    s3 = boto.client('s3', aws_access_key_id=config('S3_ACCESS_ID'),
                     aws_secret_access_key=config('S3_SECRET_KEY'))
    picture_path = os.path.join('static/profile_pics', pic_fn)
    s3.put_object(ACL='public-read', Body=file_bytes, Bucket=config('S3_BUCKET_NAME'), Key=picture_path,
                  ContentType='image/' + contentType)
    prev_pic = os.path.join('static/profile_pics', current_user.image_file)
    if current_user.image_file != 'default.png':
        s3.delete_object(Bucket=config('S3_BUCKET_NAME'), Key=prev_pic)
    return pic_fn


def send_reset_email(User):
    token = User.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[User.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('Users.Reset_Token', token=token, _external=True)}

If you did not make this request then simply ignore this email
'''
    mail.send(msg)

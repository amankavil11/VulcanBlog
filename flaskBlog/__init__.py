from flask import Flask
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#template_folder **kwargs is used to change default "template" folder name, in this case to HTML templates
app = Flask(__name__, template_folder="HTML templates")

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)
login_man.login_view = 'Users.Login'
login_man.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = config('EMAIL_PASS')
mail = Mail(app)

from flaskBlog.Users.routes import users
from flaskBlog.Posts.routes import posts
from flaskBlog.Main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)



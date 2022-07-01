from flask import Flask
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#template_folder **kwargs is used to change default "template" folder name, in this case to HTML templates
app = Flask(__name__, template_folder="HTML templates")

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)
login_man.login_view = 'Login'
login_man.login_message_category = 'info'

from flaskBlogPkg import routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#template_folder **kwargs is used to change default "template" folder name, in this case to HTML templates
app = Flask(__name__, template_folder="HTML templates")

app.config['SECRET_KEY'] = '34665436c8c5f81e7aadc5b9b015089c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///site.db'
db = SQLAlchemy(app)

from flaskBlogPkg import routes

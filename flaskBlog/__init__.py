from flask import Flask
from flaskBlog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_man = LoginManager()
login_man.login_view = 'Users.Login'
login_man.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    #template_folder **kwargs is used to change default "template" folder name, in this case to HTML templates
    app = Flask(__name__, template_folder="HTML templates")
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_man.init_app(app)
    mail.init_app(app)
    
    from flaskBlog.Users.routes import users
    from flaskBlog.Posts.routes import posts
    from flaskBlog.Main.routes import main
    from flaskBlog.Errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app

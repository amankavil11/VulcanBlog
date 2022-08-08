from decouple import config


class Config:
    SECRET_KEY = config('SECRET_KEY')
    
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('EMAIL_ADDRESS')
    MAIL_PASSWORD = config('EMAIL_PASS')
    
    

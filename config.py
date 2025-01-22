from dotenv import dotenv_values

class Config:
    config = dotenv_values('.env')

    SECRET_KEY = config['SECRET_KEY']
    JWT_TOKEN_LOCATION = ['headers']
    SERVER_NAME = "127.0.0.1:5000"
    DEBUG = True

    DATABASE_USERNAME = config['DATABASE_USERNAME']
    DATABASE_PASSWORD = config['DATABASE_PASSWORD']
    DATABASE_HOST = config['DATABASE_HOST']
    DATABASE_PORT = config['DATABASE_PORT']
    DATABASE_NAME = config['DATABASE_NAME']

    TEMPLATE_FOLDER = "templates/"
    STATIC_FOLDER = "static/"

    MAIL_SERVER = config.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(config.get('MAIL_PORT', 587))
    MAIL_USE_TLS = config.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = config['MAIL_USERNAME']
    MAIL_PASSWORD = config['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = config['MAIL_DEFAULT_SENDER']
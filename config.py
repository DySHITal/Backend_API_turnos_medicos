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

class TestingConfig:
    config = dotenv_values('.env')

    SECRET_KEY = config['SECRET_KEY']
    JWT_TOKEN_LOCATION = ['headers']
    SERVER_NAME = "127.0.0.1:5000"
    TESTING = True

    DATABASE_USERNAME = config['TEST_DATABASE_USERNAME']
    DATABASE_PASSWORD = config['TEST_DATABASE_PASSWORD']
    DATABASE_HOST = config['TEST_DATABASE_HOST']
    DATABASE_PORT = config['TEST_DATABASE_PORT']
    DATABASE_NAME = config['TEST_DATABASE_NAME']

    TEMPLATE_FOLDER = "templates/"
    STATIC_FOLDER = "static/"
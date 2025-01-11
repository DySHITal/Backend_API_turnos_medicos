from flask import Flask
from config import Config
from flask_cors import CORS
# from .routes.auth_bp import auth_bp
# from .routes.user_bp import user_bp
# from .routes.chat_bp import chat_bp
# from .routes.canales_bp import canal_bp
from .database import DatabaseConnection

def init_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    CORS(app,origins='http://127.0.0.1:5500', supports_credentials=True)
    app.config.from_object(Config)
    DatabaseConnection.set_config(app.config)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(user_bp)
    # app.register_blueprint(chat_bp)
    # app.register_blueprint(canal_bp)
    return app
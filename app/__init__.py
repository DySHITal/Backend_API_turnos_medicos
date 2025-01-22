from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS
from .routes.auth_bp import auth_bp
from .routes.paciente_bp import paciente_bp
from .routes.profesional_bp import profesional_bp
from flask_mail import Mail
from flask_apscheduler import APScheduler
from .database import DatabaseConnection

mail = Mail()
scheduler = APScheduler()

def init_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    # CORS(app,origins='http://127.0.0.1:5500', supports_credentials=True)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    DatabaseConnection.set_config(app.config)
    JWTManager(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(profesional_bp)
    return app
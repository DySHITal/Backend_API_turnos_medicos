from flask import Blueprint
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['POST'])(AuthController.login)
auth_bp.route('/logout', methods=['GET'])(AuthController.logout)
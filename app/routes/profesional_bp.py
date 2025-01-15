from flask import Blueprint
from ..controllers.profesional_controller import ProfesionalController

profesional_bp = Blueprint('profesional_bp', __name__)

profesional_bp.route('/cancelar_turno/<int:id_turno>', methods=['DELETE'])(ProfesionalController.cancelarTurno)
profesional_bp.route('/datos_profesional/<int:id_profesional>', methods=['GET'])(ProfesionalController.getInfo)
profesional_bp.route('/turnos_profesional/<int:id_profesional>', methods=['GET'])(ProfesionalController.getTurnos)
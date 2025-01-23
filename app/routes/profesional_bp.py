from flask import Blueprint
from ..controllers.profesional_controller import ProfesionalController

profesional_bp = Blueprint('profesional_bp', __name__)

profesional_bp.route('/cancelar_turno_profesional/<int:id_turno>', methods=['POST'])(ProfesionalController.cancelarTurno)
profesional_bp.route('/datos_profesional', methods=['GET'])(ProfesionalController.getInfo)
profesional_bp.route('/turnos_profesional', methods=['GET'])(ProfesionalController.getTurnos)
profesional_bp.route('/get_profesionales', methods=['GET'])(ProfesionalController.getProfesionales)
profesional_bp.route('/asistir/<int:id_turno>', methods=['GET'])(ProfesionalController.asistirTurno)
profesional_bp.route('/disponibilidad/<int:id_profesional>', methods=['GET'])(ProfesionalController.getDisponibilidad)
from flask import Blueprint
from ..controllers.paciente_controller import PacienteController

paciente_bp = Blueprint('paciente_bp', __name__)

paciente_bp.route('/register', methods=['GET','POST'])(PacienteController.register)
paciente_bp.route('/crear_turno', methods=['POST'])(PacienteController.crearTurno)
paciente_bp.route('/cancelar_turno/<int:id_turno>', methods=['DELETE'])(PacienteController.cancelarTurno)
paciente_bp.route('/datos_paciente/<int:id_paciente>', methods=['GET'])(PacienteController.getInfo)
paciente_bp.route('/turnos_paciente/<int:id_paciente>', methods=['GET'])(PacienteController.getTurnos)
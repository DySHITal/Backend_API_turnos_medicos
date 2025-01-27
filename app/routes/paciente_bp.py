from flask import Blueprint
from ..controllers.paciente_controller import PacienteController

paciente_bp = Blueprint('paciente_bp', __name__)

paciente_bp.route('/register', methods=['POST'])(PacienteController.register)
paciente_bp.route('/crear_turno', methods=['POST'])(PacienteController.crearTurno)
paciente_bp.route('/cancelar_turno/<int:id_turno>', methods=['POST'])(PacienteController.cancelarTurno)
paciente_bp.route('/datos_paciente', methods=['GET'])(PacienteController.getInfo)
paciente_bp.route('/turnos_paciente', methods=['GET'])(PacienteController.getTurnos)
paciente_bp.route('/modificar_paciente', methods=['PUT'])(PacienteController.modificarPaciente)
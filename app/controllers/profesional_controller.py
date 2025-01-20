from ..models.profesional_model import Profesional
from ..models.paciente_model import Paciente
from flask import request, session, jsonify
import os
from ..utils.auth_decorador import requiere_autenticacion
class ProfesionalController:
    
    @staticmethod
    @requiere_autenticacion
    def getInfo(id_usuario):
        usuario = Profesional.get_info(id_usuario)
        if usuario is None:
            return {'msg': 'Usuario no encontrado'}, 404
        else:
            return usuario, 200

    @staticmethod
    @requiere_autenticacion
    def cancelarTurno(id_turno, id_usuario):
        data = request.json
        razon_cancelacion = data.get('Razon', 'Cancelado por el profesional')
        try:
            # Verificar si el turno existe y pertenece al paciente
            turno = Profesional.obtener_turno_por_id(id_turno)
            if not turno:
                return {'msg': 'El turno no existe'}, 404

            # Cambiar el estado del turno a "Cancelado por Profesional"
            Profesional.cancelar_turno(id_turno, id_usuario, razon_cancelacion)

            return jsonify({'msg': 'Turno cancelado exitosamente'}), 200
        except Exception as e:
            return jsonify({'msg': 'Error al cancelar el turno', 'error': str(e)}), 400
        
    @staticmethod
    @requiere_autenticacion
    def getTurnos(id_usuario):
        turnos = Profesional.turnos_reservados(id_usuario)
        return jsonify(turnos), 200
    
    @classmethod
    def getProfesionales(cls):
        profesionales = Profesional.get_profesionales()
        return [profesional for profesional in profesionales], 200

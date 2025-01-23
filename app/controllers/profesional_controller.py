from ..models.profesional_model import Profesional
from ..models.disponibilidad_model import Disponibilidad
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
            turno = Profesional.obtener_turno_por_id(id_turno)
            if not turno:
                return {'msg': 'El turno no existe'}, 404

            Profesional.cancelar_turno(id_turno, id_usuario, razon_cancelacion)

            return jsonify({'msg': 'Turno cancelado exitosamente'}), 200
        except Exception as e:
            return jsonify({'msg': 'Error al cancelar el turno', 'error': str(e)}), 400
        
    @staticmethod
    @requiere_autenticacion
    def getTurnos(id_usuario):
        turnos = Profesional.turnos_reservados(id_usuario)
        return turnos, 200
    
    @classmethod
    def getProfesionales(cls):
        profesionales = Profesional.get_profesionales()
        return [profesional for profesional in profesionales], 200
    
    @staticmethod
    @requiere_autenticacion
    def asistirTurno(id_turno, id_usuario=None):
        check = request.args.get('check', '').lower() == 'true'
        try:
            estado = 'Asistió' if check else 'No Asistió'
            Profesional.actualizar_estado_turno(id_turno, estado)
            return {'msg': f"Turno actualizado exitosamente a '{estado}'"}, 200
        except Exception as e:
            return {'error': f"Error al actualizar el turno: {str(e)}"}, 404

    @staticmethod
    @requiere_autenticacion
    def getDisponibilidad(id_profesional, id_usuario=None):
        try:
            disponibilidad = Disponibilidad.get_disponibilidad(id_profesional)
            return disponibilidad, 200
        except Exception as e:
            return {'error': f"Error al obtener la disponibilidad: {str(e)}"}, 404
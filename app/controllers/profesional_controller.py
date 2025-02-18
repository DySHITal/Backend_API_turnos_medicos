from ..models.profesional_model import Profesional
from ..models.disponibilidad_model import Disponibilidad
from flask import request, session, jsonify
from ..utils.auth_decorador import requiere_autenticacion
from datetime import datetime, timedelta

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
        turno_fecha = data.get('fecha')
        turno_hora = data.get('hora')
        razon_cancelacion = data.get('Razon', 'Cancelado por el profesional')
        try:
            turno = Profesional.obtener_turno_por_id(id_turno)
            if not turno:
                return {'msg': 'El turno no existe'}, 404

            fecha_hora_turno = datetime.strptime(f"{turno_fecha} {turno_hora}", "%Y-%m-%d %H:%M")
            ahora = datetime.now()

            if fecha_hora_turno <= ahora + timedelta(hours=24):
                return {'msg': 'No puedes cancelar turnos antes de 24 horas de anticipación'}, 400
            
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
        
    @staticmethod
    def getOsProfesional(id_profesional):
        try:
            os_profesional = Profesional.get_os_profesional(id_profesional)
            return os_profesional, 200
        except Exception as e:
            return {'error': f"Error al obtener las obras sociales del profesional: {str(e)}"}, 404
        
    @staticmethod
    @requiere_autenticacion
    def modificarProfesional(id_usuario):
        data = request.json
        try:
            profesional = Profesional(
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                correo=data.get('correo'),
                especialidad=data.get('especialidad'),
                numero_matricula=data.get('numero_matricula')
            )
            obras_sociales = data.get('obras_sociales')
            id_obras_sociales = Profesional.get_id_os(obras_sociales)

            if profesional is not None and obras_sociales is not None:
                Profesional.modificar_profesional(id_usuario, profesional, id_obras_sociales)
                return jsonify({'msg': 'Profesional modificado exitosamente'}), 200
            else:
                return jsonify({'msg': 'Datos incompletos'}), 400
        except Exception as e:
            return jsonify({'msg': 'Error al modificar el profesional', 'error': str(e)}), 400
        
    @staticmethod
    @requiere_autenticacion
    def modificarDisponibilidad(id_usuario):
        data = request.json
        try:
            disponibilidades = data.get('disponibilidades')
            if not disponibilidades or not isinstance(disponibilidades, list):
                return jsonify({'msg': 'Datos incompletos o formato inválido'}), 400

            # Llamar al modelo para actualizar las disponibilidades
            Disponibilidad.modificar_disponibilidad(id_usuario, disponibilidades)
            return jsonify({'msg': 'Disponibilidad modificada exitosamente'}), 200

        except Exception as e:
            return jsonify({'msg': 'Error al modificar la disponibilidad', 'error': str(e)}), 400

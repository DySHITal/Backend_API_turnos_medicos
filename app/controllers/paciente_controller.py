from ..models.paciente_model import Paciente
from flask import request, session, jsonify
import os
import jwt
from dotenv import load_dotenv
from ..utils.auth_decorador import requiere_autenticacion
from datetime import datetime, timedelta

load_dotenv()
JWT_SECRET_KEY = os.getenv("SECRET_KEY")

class PacienteController:
    
    @staticmethod
    @requiere_autenticacion
    def getInfo(id_usuario):
        usuario = Paciente.get_info(id_usuario)
        if usuario is None:
            return {'msg': 'Usuario no encontrado'}, 404
        else:
            return usuario, 200

    @classmethod
    def register(cls):                  
        data = request.json
        usuario = Paciente(
            nombre = data.get('nombre'),
            apellido = data.get('apellido'),
            correo = data.get('correo'),
            dni = data.get('dni'),
            obra_social = data.get('obra_social'),
            contrasena = data.get('contrasena')
        )
        if not usuario.dni or not usuario.dni.isdigit() or len(usuario.dni) != 8:
            return {'msg': 'El DNI debe tener 8 dígitos y contener solo números'}, 400
        if not usuario.contrasena or len(usuario.contrasena) < 8:
            return {'msg': 'La contraseña debe tener al menos 8 caracteres'}, 400
        if Paciente.is_registered(usuario) or Paciente.existe_dni(usuario.dni):
            return {'msg':'Usuario ya registrado o DNI en uso'}, 401
            
        try:
            Paciente.register_user(usuario)
            return jsonify({'msg': 'Usuario Registrado exitosamente'}), 200
        except Exception as e:
            return jsonify({'msg': 'Todos los campos deben estar completados'}), 400
        
    @staticmethod
    @requiere_autenticacion
    def crearTurno(id_usuario):
        try:
            data = request.json
            turno = {
                "fecha": data.get("Fecha"),
                "hora": data.get("Hora"),
                "estado": data.get("Estado"),
                "id_paciente": id_usuario,
                "id_profesional": data.get("ID_Profesional"),
            }
            if Paciente.turnos_reservados(turno["fecha"], turno["hora"], turno["id_profesional"]):
                return {'msg': 'El profesional ya tiene un turno reservado en esa hora'}, 409
            
            fecha_hora_turno = datetime.strptime(f"{turno['fecha']} {turno['hora']}", "%Y-%m-%d %H:%M:%S")
            ahora = datetime.now()

            if fecha_hora_turno <= ahora + timedelta(hours=24):
                return {'msg': 'No puedes reservar turnos antes de 24 horas de anticipación'}, 400

            Paciente.crear_turno(turno)
            return jsonify({'msg': 'Turno creado exitosamente'}), 201

        except Exception as e:
            return jsonify({'msg': f'Error desconocido: {str(e)}'}), 500

    @staticmethod
    @requiere_autenticacion
    def cancelarTurno(id_turno, id_usuario):
        data = request.json
        razon_cancelacion = data.get('Razon', 'Cancelado por el paciente')
        try:
            turno = Paciente.obtener_turno_por_id(id_turno)
            if not turno:
                return {'msg': 'El turno no existe'}, 404
            if turno['id_paciente'] != id_usuario:
                return {'msg': 'El turno no pertenece al paciente'}, 403

            Paciente.cancelar_turno(id_turno, turno['id_paciente'], razon_cancelacion)

            return {'msg': 'Turno cancelado exitosamente'}, 200
        except Exception as e:
            return {'msg': 'Error al cancelar el turno', 'error': str(e)}, 400
        
    @staticmethod
    @requiere_autenticacion
    def getTurnos(id_usuario):
        turnos = Paciente.get_turnos_paciente(id_usuario)
        return turnos, 200

    @staticmethod
    @requiere_autenticacion
    def modificarPaciente(id_usuario):
        data = request.json
        try:
            paciente = Paciente(
                nombre = data.get('nombre'),
                apellido = data.get('apellido'),
                correo = data.get('correo'),
                dni = data.get('dni'),
                obra_social = data.get('obra_social')
            )
            if paciente is not None:
                Paciente.modificar_paciente(id_usuario, paciente)
                return jsonify({'msg': 'Paciente modificado exitosamente'}), 200
        except Exception as e:
            return jsonify({'msg': 'Error al modificar el paciente', 'error': str(e)}), 400
            
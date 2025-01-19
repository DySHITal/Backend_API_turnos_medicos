from ..models.paciente_model import Paciente
from flask import request, session, jsonify
import os
import jwt
from dotenv import load_dotenv
from ..utils.auth_decorador import requiere_autenticacion

load_dotenv()
JWT_SECRET_KEY = os.getenv("SECRET_KEY")

class PacienteController:
    
    @classmethod
    def getInfo(cls, id_profesional):
        usuario = Paciente.get_info(id_profesional)
        if usuario is None:
            return {'msg': 'Usuario no encontrado'}, 404
        else:
            return usuario.serialize(), 200

    @classmethod
    def register(cls):                  
        data = request.json
        print(f"Datos recibidos para el registro: {data}")
        usuario = Paciente(
            nombre = data.get('nombre'),
            apellido = data.get('apellido'),
            correo = data.get('correo'),
            dni = data.get('dni'),
            obra_social = data.get('obra_social'),
            contrasena = data.get('contrasena')
        )
        if Paciente.is_registered(usuario):
            return {'msg':'Usuario ya registrado'}, 401
            
        try:
            Paciente.register_user(usuario)
            return jsonify({'msg': 'Usuario Registrado exitosamente'}), 200
        except Exception as e:
            return jsonify({'msg': 'Todos los campos deben estar completados'}), 400
        
    # Cargar variables de entorno desde .env

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
            print("Turno: ", turno)

            # Validar duplicidad de turno
            if Paciente.turnos_reservados(turno["fecha"], turno["hora"], turno["id_profesional"]):
                return {'msg': 'El profesional ya tiene un turno reservado en esa hora'}, 409

            # Crear el turno
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
            # Verificar si el turno existe y pertenece al paciente
            turno = Paciente.obtener_turno_por_id(id_turno)
            if not turno:
                return {'msg': 'El turno no existe'}, 404
            if turno['id_paciente'] != id_usuario:
                return {'msg': 'El turno no pertenece al paciente'}, 403

            # Cambiar el estado del turno a "Cancelado por Paciente"
            Paciente.cancelar_turno(id_turno, turno['id_paciente'], razon_cancelacion)

            return {'msg': 'Turno cancelado exitosamente'}, 200
        except Exception as e:
            return {'msg': 'Error al cancelar el turno', 'error': str(e)}, 400
        
    @staticmethod
    @requiere_autenticacion
    def getTurnos(id_paciente, id_usuario = None):
        turnos = Paciente.get_turnos_paciente(id_paciente)
        return jsonify(turnos), 200

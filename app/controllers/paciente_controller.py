from ..models.paciente_model import Paciente
from flask import request, session, jsonify
import os
import jwt
from dotenv import load_dotenv

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

    @classmethod
    def crearTurno(cls):
        # Verificar autenticación JWT
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({'msg': 'Token de autenticación no proporcionado'}), 401

        try:
            # Extraer y decodificar el token
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'msg': 'Token expirado, inicia sesión nuevamente'}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({'msg': 'Token inválido', 'error': str(e)}), 401
            id_usuario = payload.get("sub")  # Ajuste para usar el ID en "sub"

            if not id_usuario:
                return jsonify({'msg': 'Token no válido, usuario no identificado'}), 401

            # Procesar solicitud para crear el turno
            data = request.json
            turno = {
                "fecha": data.get("Fecha"),
                "hora": data.get("Hora"),
                "estado": data.get("Estado"),
                "id_paciente": id_usuario,  # Usa el ID extraído del token
                "id_profesional": data.get("ID_Profesional"),
            }

            # Validar duplicidad de turno
            if Paciente.turnos_reservados(turno["fecha"], turno["hora"], turno["id_profesional"]):
                return {'msg': 'El profesional ya tiene un turno reservado en esa hora'}, 409

            # Crear el turno
            Paciente.crear_turno(turno)
            return jsonify({'msg': 'Turno creado exitosamente'}), 201

        except jwt.ExpiredSignatureError:
            return jsonify({'msg': 'Token expirado, inicia sesión nuevamente'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'msg': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'msg': f'Error desconocido: {str(e)}'}), 500
        
    @classmethod
    def cancelarTurno(cls, id_paciente):
        data = request.json
        id_turno = data.get('ID_Turno') 
        razon_cancelacion = data.get('Razon', 'Cancelado por el paciente')

        try:
            # Verificar si el turno existe y pertenece al paciente
            turno = Paciente.obtener_turno_por_id(id_turno)
            if not turno:
                return {'msg': 'El turno no existe'}, 404
            if turno['id_paciente'] != id_paciente:
                return {'msg': 'El turno no pertenece al paciente'}, 403

            # Cambiar el estado del turno a "Cancelado por Paciente"
            Paciente.cancelar_turno(id_turno, id_paciente, razon_cancelacion)

            return jsonify({'msg': 'Turno cancelado exitosamente'}), 200
        except Exception as e:
            return jsonify({'msg': 'Error al cancelar el turno', 'error': str(e)}), 400
        
    @classmethod
    def getTurnos(cls, id_paciente):
        turnos = Paciente.getTurnos(id_paciente)
        return jsonify(turnos), 200

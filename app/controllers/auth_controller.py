from ..models.paciente_model import Paciente
from flask import request, session, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from ..models.profesional_model import Profesional

class AuthController:

    @classmethod
    def login(cls):
        bcrypt = Bcrypt()
        data = request.json
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        # Buscar en la tabla Paciente primero
        paciente = Paciente.get_by_email(correo)
        if paciente:
            if bcrypt.check_password_hash(paciente.contrasena, contrasena):
                session['correo'] = correo 
                access_token = create_access_token(identity=str(paciente.id_paciente)) 
                return jsonify({'msg': 'Sesion iniciada', 'access_token': access_token}), 200
            else:
                return {'msg': 'Usuario o contraseña incorrectos'}, 401

        # Si no es paciente, entonces buscar en la tabla Profesional
        profesional = Profesional.get_by_email(correo)
        if profesional:
            # Para profesionales, no manejamos contraseñas con hashing, sino que directamente la validación de correos
            if profesional.contrasena == contrasena:
                access_token = create_access_token(identity=str(profesional.id_profesional)) 
                return jsonify({'msg': 'Sesion iniciada', 'access_token': access_token}), 200
            else:
                return {'msg': 'Usuario o contraseña incorrectos'}, 401

        return {'msg': 'Usuario o contraseña incorrectos'}, 401

    @classmethod
    def logout(cls):
        session.pop('correo', None)
        return {'msg':'Sesion cerrada'}, 200
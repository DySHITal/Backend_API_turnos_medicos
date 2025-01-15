from ..models.paciente_model import Paciente
from flask import request, session, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

class AuthController:

    @classmethod
    def login(cls):
        bcrypt = Bcrypt()
        data = request.json
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        usuario = Paciente.get_by_email(correo)

        if usuario is None:
            return {'msg': 'Usuario o contraseña incorrectos'}, 401

        if bcrypt.check_password_hash(usuario.contrasena, contrasena):
            session['correo'] = correo 
            access_token = create_access_token(identity=str(usuario.id_paciente)) 
            return jsonify({'msg': 'Sesion iniciada', 'access_token': access_token}), 200
        else:
            return {'msg': 'Usuario o contraseña incorrectos'}, 401

    @classmethod
    def logout(cls):
        session.pop('alias', None)
        return {'msg':'Sesion cerrada'}, 200

    

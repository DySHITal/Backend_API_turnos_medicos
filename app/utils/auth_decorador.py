from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()
JWT_SECRET_KEY = os.getenv("SECRET_KEY")

def requiere_autenticacion(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({'msg': 'Token de autenticación no proporcionado'}), 401

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            id_usuario = int(payload.get("sub"))

            if not id_usuario:
                return jsonify({'msg': 'Token no válido, usuario no identificado'}), 401

            return f(*args, id_usuario=id_usuario, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': 'Token expirado, inicia sesión nuevamente'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'msg': 'Token inválido', 'error': str(e)}), 401
        except Exception as e:
            return jsonify({'msg': f'Error desconocido: {str(e)}'}), 500
    return wrapper



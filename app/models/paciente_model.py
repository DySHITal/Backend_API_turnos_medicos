from ..database import DatabaseConnection
from flask_bcrypt import Bcrypt

class Paciente:
    '''Modelo para la clase paciente'''

    def __init__(self, **kwargs):
        self.id_paciente = kwargs.get('id_paciente')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.correo = kwargs.get('correo')
        self.contrasena = kwargs.get('contrasena')

    def serialize(self):
        '''Serialize object representation
        Returns:
            dict: Object representation '''
        return {
            'id_paciente': self.id_paciente,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'contrasena': self.contrasena
        }

    @classmethod
    def is_registered(cls, paciente):
        try:
            query = '''SELECT id_paciente FROM turnosDB.paciente WHERE correo = %(correo)s'''
            params = paciente.__dict__
            result = DatabaseConnection.fetch_one(query, params=params)
            if result is not None:
                DatabaseConnection.close_connection()
                return True
            DatabaseConnection.close_connection()
            return False
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_by_email(cls, correo):
        try:
            query = '''SELECT id_paciente, nombre, apellido, correo, contrasena
                        FROM turnosDB.paciente WHERE correo = %s'''
            result = DatabaseConnection.fetch_one(query, (correo,))
            if result:
                DatabaseConnection.close_connection()
                return cls(
                    id_paciente=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    contrasena=result[4]  # Asegúrate de que se retorna la contraseña con el hash
                )
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
    
    @classmethod
    def register_user(cls, paciente):
        bcrypt = Bcrypt()
        try:
            hashed_password = bcrypt.generate_password_hash(paciente.contrasena).decode('utf-8')
            query="""INSERT INTO turnosDB.paciente(nombre, apellido, correo, contrasena)
            VALUES(%(nombre)s, %(apellido)s, %(correo)s, %(contrasena)s);"""
            params = paciente.__dict__
            params['contrasena'] = hashed_password
            DatabaseConnection.execute_query(query, params=params)
            DatabaseConnection.close_connection()
        except Exception as e:
            raise Exception(f"Error durante el registro del usuario: {e}")

    @classmethod
    def get_id_paciente(cls, email):
        try:
            query = 'SELECT id_paciente FROM paciente WHERE email = %s'
            result = DatabaseConnection.fetch_one(query, (email,))
            if result is not None:
                DatabaseConnection.close_connection()
                id_paciente = result[0]
                print(id_paciente)
                return id_paciente
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_info(cls, id_paciente):
        try:
            query = 'SELECT nombre, apellido, correo FROM paciente WHERE id_paciente = %s'
            result = DatabaseConnection.fetch_one(query, (id_paciente,))
            if result is not None:
                DatabaseConnection.close_connection()
                info = result
                return info
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def turnos_reservados(cls, fecha, hora, id_profesional):
        try:
            query = '''SELECT COUNT(*) FROM turnosDB.turno WHERE fecha = %s AND hora = %s AND id_profesional = %s'''
            params = (fecha, hora, id_profesional)
            result = DatabaseConnection.fetch_one(query, params=params)
            if result is not None:
                DatabaseConnection.close_connection()
                cantidad = result[0]
                return cantidad > 0
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def crear_turno(cls, turno):
        try:
            query = '''INSERT INTO turnosDB.turno(fecha, hora, estado, id_paciente, id_profesional) VALUES (%(fecha)s, %(hora)s, %(estado)s, %(id_paciente)s, %(id_profesional)s)'''
            params = turno
            DatabaseConnection.execute_query(query, params=params)
            DatabaseConnection.close_connection()
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def obtener_turno_por_id(cls, id_turno):
        """Obtiene la información de un turno por su ID."""
        try:
            query = '''SELECT id_turno, id_paciente, id_profesional, fecha, hora, estado
            FROM turnosDB.turno
            WHERE id_turno = %s
            '''
            result = DatabaseConnection.fetch_one(query, (id_turno,))
            if result:
                return {
                    'id_turno': result[0],
                    'id_paciente': result[1],
                    'id_profesional': result[2],
                    'fecha': result[3],
                    'hora': result[4],
                    'estado': result[5]
                }
            return None
        except Exception as e:
            raise Exception(e)


    @classmethod
    def cancelar_turno(cls, id_turno, id_paciente, razon_cancelacion):
        """Cancela un turno actualizando su estado y registrando la cancelación."""
        try:
            # Actualizar estado del turno
            update_turno_query = '''
            UPDATE turnosDB.turno
            SET estado = 'Cancelado por Paciente'
            WHERE id_turno = %s
            '''
            DatabaseConnection.execute_query(update_turno_query, (id_turno,))

            # Registrar la cancelación
            registrar_cancelacion_query = '''
            INSERT INTO turnosDB.cancelaciones (id_turno, id_realizado_por, fecha_cancelacion, razon)
            VALUES (%s, %s, NOW(), %s)
            '''
            params = (id_turno, id_paciente, razon_cancelacion)
            DatabaseConnection.execute_query(registrar_cancelacion_query, params)
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_turnos_paciente(cls, id_paciente):
        try:
            query = '''
            SELECT t.id_turno, t.fecha, t.hora, t.estado, p.nombre, p.apellido
            FROM turnosDB.turno t
            JOIN turnosDB.profesionales p ON t.id_profesional = p.id_profesional
            WHERE t.id_paciente = %s
            '''
            result = DatabaseConnection.fetch_all(query, (id_paciente,))
            if result:
                return result
            return []
        except Exception as e:
            raise Exception(e)
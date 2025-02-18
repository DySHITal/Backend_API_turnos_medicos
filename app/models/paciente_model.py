from ..database import DatabaseConnection
from flask_bcrypt import Bcrypt
from datetime import datetime

class Paciente:
    '''Modelo para la clase paciente'''

    def __init__(self, **kwargs):
        self.id_paciente = kwargs.get('id_paciente')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.correo = kwargs.get('correo')
        self.dni = kwargs.get('dni')
        self.obra_social = kwargs.get('obra_social')
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
            'dni': self.dni,
            'obra_social': self.obra_social,
            'contrasena': self.contrasena
        }

    @classmethod
    def is_registered(cls, paciente):
        '''Controla si el paciente está registrado'''
        try:
            query = '''SELECT id_paciente FROM paciente WHERE correo = %(correo)s'''
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
        '''Obtiene un paciente por correo'''
        try:
            query = '''SELECT id_paciente, nombre, apellido, correo, contrasena
                        FROM paciente WHERE correo = %s'''
            result = DatabaseConnection.fetch_one(query, (correo,))
            if result:
                DatabaseConnection.close_connection()
                return cls(
                    id_paciente=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    contrasena=result[4]
                )
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
    
    @classmethod
    def register_user(cls, paciente):
        '''Registra un nuevo paciente'''
        bcrypt = Bcrypt()
        try:
            hashed_password = bcrypt.generate_password_hash(paciente.contrasena).decode('utf-8')
            query="""INSERT INTO paciente(nombre, apellido, correo, dni, obra_social, contrasena)
            VALUES(%(nombre)s, %(apellido)s, %(correo)s, %(dni)s, %(obra_social)s, %(contrasena)s);"""
            params = paciente.__dict__
            params['contrasena'] = hashed_password
            DatabaseConnection.execute_query(query, params=params)
            DatabaseConnection.close_connection()
        except Exception as e:
            raise Exception(f"Error durante el registro del usuario: {e}")

    @classmethod
    def get_id_paciente(cls, email):
        '''Obtiene el id_paciente asociado con un correo'''
        try:
            query = 'SELECT id_paciente FROM paciente WHERE correo = %s'
            result = DatabaseConnection.fetch_one(query, (email,))
            if result is not None:
                DatabaseConnection.close_connection()
                id_paciente = result[0]
                return id_paciente
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_info(cls, id_usuario):
        '''Obtiene la información del paciente asociado con un id_paciente'''
        try:
            query = 'SELECT nombre, apellido, correo, dni, obra_social FROM paciente WHERE id_paciente = %s'
            result = DatabaseConnection.fetch_one(query, (id_usuario,))
            
            if result is not None:
                DatabaseConnection.close_connection()
                paciente = Paciente(
                    nombre=result[0],
                    apellido=result[1],
                    correo=result[2],
                    dni=result[3],
                    obra_social=result[4]
                )
                return paciente.serialize()
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(f"Error al obtener la información del paciente: {e}")
        
    @classmethod
    def turnos_reservados(cls, fecha, hora, id_profesional):
        '''Controla que el turno que se quiere crear no exista previamente 
        y tenga una diferencia mínima de 30 minutos con otro turno del mismo profesional'''
        try:
            query = '''
                SELECT estado 
                FROM turno 
                WHERE fecha = %s 
                AND id_profesional = %s 
                AND estado = 'Reservado'
                AND ABS(TIMESTAMPDIFF(MINUTE, CONCAT(fecha, ' ', hora), CONCAT(%s, ' ', %s))) < 30
            '''
            params = (fecha, id_profesional, fecha, hora)
            result = DatabaseConnection.fetch_one(query, params=params)
            DatabaseConnection.close_connection()            
            return result is not None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def crear_turno(cls, turno):
        """Crea un nuevo turno."""
        try:
            query = '''INSERT INTO turno(fecha, hora, estado, id_paciente, id_profesional) VALUES (%(fecha)s, %(hora)s, %(estado)s, %(id_paciente)s, %(id_profesional)s)'''
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
            FROM turno
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
            update_turno_query = '''
            UPDATE turno
            SET estado = 'Cancelado por Paciente'
            WHERE id_turno = %s
            '''
            DatabaseConnection.execute_query(update_turno_query, (id_turno,))

            registrar_cancelacion_query = '''
            INSERT INTO cancelacion (id_turno, id_paciente_cancelacion, fecha_cancelacion, razon)
            VALUES (%s, %s, NOW(), %s)
            '''
            params = (id_turno, id_paciente, razon_cancelacion)
            DatabaseConnection.execute_query(registrar_cancelacion_query, params)
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_turnos_paciente(cls, id_paciente):
        """Obtiene los turnos reservados por un paciente."""
        try:
            query = '''
            SELECT t.id_turno, t.fecha, t.Hora, t.estado, p.nombre, p.apellido
            FROM turno t
            JOIN profesional p ON t.id_profesional = p.id_profesional
            WHERE t.id_paciente = %s AND t.estado = "Reservado"
            '''
            result = DatabaseConnection.fetch_all(query, (id_paciente,))
            
            if result:
                formatted_result = []
                for turno in result:
                    turno_dict = {
                        'id_turno': turno[0],
                        'fecha': turno[1].strftime("%Y-%M-%D") if isinstance(turno[1], datetime) else str(turno[1]),
                        'hora': turno[2].strftime('%H:%M:%S') if isinstance(turno[2], datetime) else str(turno[2]),
                        'estado': turno[3],
                        'nombre': turno[4],
                        'apellido': turno[5]
                    }
                    formatted_result.append(turno_dict)
                return formatted_result
            
            return []
        except Exception as e:
            raise Exception(e)

    @classmethod
    def existe_dni(cls, dni):
        '''Verifica si un paciente ya existe con un dni determinado'''
        try:
            query = 'SELECT COUNT(*) FROM paciente WHERE dni = %s'
            result = DatabaseConnection.fetch_one(query, (dni,))
            if result is not None:
                DatabaseConnection.close_connection()
                cantidad = result[0]
                return cantidad > 0
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def modificar_paciente(cls, id_paciente, paciente):
        '''Modifica la información de un paciente'''
        try:
            query = '''
            UPDATE paciente
            SET nombre = %s, apellido = %s, correo = %s, dni = %s, obra_social = %s
            WHERE id_paciente = %s
            '''
            params = (
                paciente.nombre,
                paciente.apellido,
                paciente.correo,
                paciente.dni,
                paciente.obra_social,
                id_paciente
            )
            DatabaseConnection.execute_query(query, params=params)
            DatabaseConnection.close_connection()
        except Exception as e:
            raise Exception(f"Error al modificar el paciente: {e}")
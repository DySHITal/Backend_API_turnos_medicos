from ..database import DatabaseConnection

class Profesional:
    '''Modelo para la clase profesional'''

    def __init__(self, **kwargs):
        self.id_profesional = kwargs.get('id_profesional')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.especialidad = kwargs.get('especialidad')
        self.matricula = kwargs.get('numero_matricula')
        self.contrasena = kwargs.get('contrasena')

    def serialize(self):
        '''Serialize object representation
        Returns:
            dict: Object representation '''
        return {
            'id_profesional': self.id_profesional,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'especialidad': self.especialidad,
            'numero_matricula': self.matricula,
            'contrasena': self.contrasena
        }

    @classmethod
    def is_registered(cls, profesional):
        try:
            query = '''SELECT id_profesional FROM turnosDB.profesional WHERE email = %(email)s AND contrasena = %(contrasena)s'''
            params = profesional.__dict__
            result = DatabaseConnection.fetch_one(query, params=params)
            if result is not None:
                DatabaseConnection.close_connection()
                return True
            DatabaseConnection.close_connection()
            return False
        except Exception as e:
            raise Exception(e)

    @classmethod
    def get_id_profesional(cls, email):
        try:
            query = 'SELECT id_profesional FROM profesional WHERE email = %s'
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
    def get_info(cls, id_profesional):
        try:
            query = 'SELECT nombre, apellido, especialidad, numero_matricula FROM profesional WHERE id_profesional = %s'
            result = DatabaseConnection.fetch_one(query, (id_profesional,))
            if result is not None:
                DatabaseConnection.close_connection()
                return result
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_by_email(cls, correo):
        try:
            query = '''SELECT id_profesional, nombre, apellido, correo, contrasena
                        FROM turnosDB.profesional WHERE correo = %s'''
            result = DatabaseConnection.fetch_one(query, (correo,))
            if result:
                DatabaseConnection.close_connection()
                return cls(
                    id_profesional=result[0],
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
    def turnos_reservados(cls, id_profesional):
        try:
            query = '''
            SELECT p.nombre, p.apellido, t.fecha, TIME_FORMAT(t.Hora, "%H:%I:%S") AS Hora
            FROM turnosDB.turno t
            JOIN turnosDB.paciente p ON t.id_paciente = p.id_paciente
            WHERE t.estado = 'Reservado' AND t.id_profesional = %s
            '''
            result = DatabaseConnection.fetch_all(query, (id_profesional,))
            if result:
                turnos_reservados = []
                for turno in result:
                    turno_data = {
                        'nombre': turno[0],
                        'apellido': turno[1],
                        'fecha': turno[2],
                        'hora': turno[3]
                    }
                    turnos_reservados.append(turno_data)
                return turnos_reservados
            DatabaseConnection.close_connection()
            return []
        except Exception as e:
            raise Exception(e)



    @classmethod
    def cancelar_turno(cls, id_turno, id_profesional, razon_cancelacion):
        """Cancela un turno actualizando su estado y registrando la cancelación."""
        try:
            # Actualizar estado del turno
            update_turno_query = '''
            UPDATE turnosDB.turno
            SET estado = 'Cancelado por Profesional'
            WHERE id_turno = %s
            '''
            DatabaseConnection.execute_query(update_turno_query, (id_turno,))

            # Registrar la cancelación
            registrar_cancelacion_query = '''
            INSERT INTO turnosDB.cancelacion (id_turno, id_realizado_por, fecha_cancelacion, razon)
            VALUES (%s, %s, NOW(), %s)
            '''
            params = (id_turno, id_profesional, razon_cancelacion)
            DatabaseConnection.execute_query(registrar_cancelacion_query, params)
        except Exception as e:
            raise Exception(e)
    
    @staticmethod
    def get_profesionales():
        try:
            query = '''
            SELECT id_profesional, nombre, apellido, especialidad
            FROM turnosDB.profesional
            '''
            result = DatabaseConnection.fetch_all(query)
            if result:
                profesionales = []
                for profesional in result:
                    profesional_instance = Profesional(
                        id_profesional= profesional[0],
                        nombre= profesional[1],
                        apellido= profesional[2],
                        especialidad= profesional[3]
                    )
                    profesionales.append(profesional_instance.serialize())
                    
                DatabaseConnection.close_connection()
                return profesionales
            DatabaseConnection.close_connection()
            return []
        except Exception as e:
            raise Exception(e)

from ..database import DatabaseConnection
from datetime import datetime

class Profesional:
    '''Modelo para la clase profesional'''

    def __init__(self, **kwargs):
        self.id_profesional = kwargs.get('id_profesional')
        self.nombre = kwargs.get('nombre')
        self.apellido = kwargs.get('apellido')
        self.correo = kwargs.get('correo')
        self.especialidad = kwargs.get('especialidad')
        self.numero_matricula = kwargs.get('numero_matricula')
        self.contrasena = kwargs.get('contrasena')

    def serialize(self):
        '''Serialize object representation
        Returns:
            dict: Object representation '''
        return {
            'id_profesional': self.id_profesional,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'especialidad': self.especialidad,
            'numero_matricula': self.numero_matricula,
            'contrasena': self.contrasena
        }

    @classmethod
    def is_registered(cls, profesional):
        '''Controla si el profesional está registrado'''
        try:
            query = '''SELECT id_profesional FROM profesional WHERE email = %(email)s AND contrasena = %(contrasena)s'''
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
        '''Obtiene el id profesional a través del email'''
        try:
            query = 'SELECT id_profesional FROM profesional WHERE correo = %s'
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
        '''Obtiene la información del profesional a través del id_profesional'''
        try:
            query = 'SELECT id_profesional, nombre, apellido, correo, especialidad, numero_matricula FROM profesional WHERE id_profesional = %s'
            result = DatabaseConnection.fetch_one(query, (id_profesional,))
            if result is not None:
                DatabaseConnection.close_connection()
                profesional = Profesional(
                    id_profesional=result[0],
                    nombre=result[1],
                    apellido=result[2],
                    correo=result[3],
                    especialidad=result[4],
                    numero_matricula=result[5]
                )
                return profesional.serialize()
            DatabaseConnection.close_connection()
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_by_email(cls, correo):
        '''Obtiene la información del profesional a través del email'''
        try:
            query = '''SELECT id_profesional, nombre, apellido, correo, contrasena
                        FROM profesional WHERE correo = %s'''
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
        '''Obtiene los turnos reservados del profesional a través del id_profesional'''
        try:
            query = '''
            SELECT p.nombre, p.apellido, t.estado, t.fecha, t.Hora, t.id_turno
            FROM turno t
            JOIN paciente p ON t.id_paciente = p.id_paciente
            WHERE t.id_profesional = %s
            '''
            result = DatabaseConnection.fetch_all(query, (id_profesional,))
            if result:
                turnos_reservados = []
                for turno in result:
                    turno_data = {
                        'nombre': turno[0],
                        'apellido': turno[1],
                        'estado': turno[2],
                        'fecha': turno[3],
                        'hora': turno[4].strftime('%H:%M:%S') if isinstance(turno[4], datetime) else str(turno[4]),
                        'id_turno': turno[5]
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
            update_turno_query = '''
            UPDATE turno
            SET estado = 'Cancelado por Profesional'
            WHERE id_turno = %s
            '''
            DatabaseConnection.execute_query(update_turno_query, (id_turno,))

            registrar_cancelacion_query = '''
            INSERT INTO cancelacion (id_turno, id_profesional_cancelacion, fecha_cancelacion, razon)
            VALUES (%s, %s, NOW(), %s)
            '''
            params = (id_turno, id_profesional, razon_cancelacion)
            DatabaseConnection.execute_query(registrar_cancelacion_query, params)
        except Exception as e:
            raise Exception(e)

    
    @staticmethod
    def get_profesionales():
        """Obtiene la lista de todos los profesionales."""
        try:
            query = '''
            SELECT id_profesional, nombre, apellido, correo, especialidad, numero_matricula
            FROM profesional
            '''
            result = DatabaseConnection.fetch_all(query)
            if result:
                profesionales = []
                for profesional in result:
                    profesional_instance = Profesional(
                        id_profesional= profesional[0],
                        nombre= profesional[1],
                        apellido= profesional[2],
                        correo=profesional[3],
                        especialidad= profesional[4],
                        numero_matricula=profesional[5]
                    )
                    profesionales.append(profesional_instance.serialize())
                    
                DatabaseConnection.close_connection()
                return profesionales
            DatabaseConnection.close_connection()
            return []
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
    def actualizar_estado_turno(cls, id_turno, estado):
        """Actualiza el estado de un turno en la base de datos."""
        query = '''
        UPDATE turno
        SET estado = %s
        WHERE id_turno = %s
        '''
        try:
            cursor = DatabaseConnection.execute_query(query, (estado, id_turno))
            if cursor.rowcount == 0:
                raise Exception(f"El turno con ID {id_turno} no existe.")
        except Exception as e:
            raise Exception(f"Error al actualizar el estado del turno: {str(e)}")
        
    @classmethod
    def get_os_profesional(cls, id_profesional):
        """Obtiene la obra social del profesional."""
        try:
            query = '''
            SELECT os.Nombre AS Obra_Social
            FROM Obra_Social os
            JOIN Profesional_ObraSocial pos ON os.ID_ObraSocial = pos.ID_ObraSocial
            JOIN Profesional p ON pos.ID_Profesional = p.ID_Profesional
            WHERE p.ID_Profesional = %s;
            '''
            result = DatabaseConnection.fetch_all(query, (id_profesional,))
            DatabaseConnection.close_connection()
            return result if result else None
        except Exception as e:
            raise Exception(f"Error al obtener las obras sociales del profesional: {str(e)}")


    @classmethod
    def get_id_os(cls, obras_sociales):
        """Obtiene los IDs de las obras sociales a partir de los nombres."""
        try:
            placeholders = ', '.join(['%s'] * len(obras_sociales))
            query = f'''
            SELECT ID_ObraSocial
            FROM Obra_Social
            WHERE Nombre IN ({placeholders});
            '''
            params = tuple(obras_sociales)
            result = DatabaseConnection.fetch_all(query, params)
            DatabaseConnection.close_connection()
            return [row[0] for row in result] if result else None
        except Exception as e:
            raise Exception(f"Error al obtener los IDs de las obras sociales: {str(e)}")

    @classmethod
    def modificar_profesional(cls, id_usuario, profesional, obras_sociales):
        """Actualiza los datos del profesional en la base de datos."""
        try:
            query_profesional = '''
            UPDATE Profesional
            SET nombre = %s, apellido = %s, correo = %s, especialidad = %s, numero_matricula = %s
            WHERE id_profesional = %s;
            '''
            params_profesional = (
                profesional.nombre,
                profesional.apellido,
                profesional.correo,
                profesional.especialidad,
                profesional.numero_matricula,
                id_usuario
            )
            DatabaseConnection.execute_query(query_profesional, params_profesional)
            DatabaseConnection.close_connection()
            query_delete = '''
            DELETE FROM Profesional_ObraSocial
            WHERE id_profesional = %s;
            '''
            DatabaseConnection.execute_query(query_delete, (id_usuario,))
            DatabaseConnection.close_connection()
            query_insert = '''
            INSERT INTO Profesional_ObraSocial (id_profesional, id_obrasocial)
            VALUES (%s, %s);
            '''
            for id_obrasocial in obras_sociales:
                DatabaseConnection.execute_query(query_insert, (id_usuario, id_obrasocial))
            DatabaseConnection.close_connection()

        except Exception as e:
            raise Exception(f"Error al modificar el profesional: {str(e)}")
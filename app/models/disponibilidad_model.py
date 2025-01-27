from ..database import DatabaseConnection
from datetime import datetime, timedelta

class Disponibilidad:
    '''Modelo para la clase disponibilidad'''

    def __init__(self, **kwargs):
        self.id_horario = kwargs.get('id_horario')
        self.dias_semana = kwargs.get('dias_semana')
        self.hora_inicio = kwargs.get('hora_inicio')
        self.hora_fin = kwargs.get('hora_fin')

    def serialize(self):
        '''Serialize object representation
        Returns:
            dict: Object representation '''
        return {
            'id_horario': self.id_horario,
            'dias_semana': self.dias_semana,
            'hora_inicio': self.hora_inicio,
            'hora_fin': self.hora_fin
        }
    
    @classmethod
    def get_disponibilidad(cls, id_profesional):
        '''Obtiene la disponibilidad de un profesional'''
        try:
            query = '''
            SELECT Dias_Semana, Hora_Inicio, Hora_Fin
            FROM turnosDB.disponibilidad
            WHERE id_profesional = %s
            '''
            result = DatabaseConnection.fetch_all(query, (id_profesional,))

            if result:
                disponibilidad_list = []
                for row in result:
                    dias_semana_set = row[0]
                    dias_semana = ', '.join(dias_semana_set) 
                    hora_inicio_td = row[1]
                    hora_fin_td = row[2]
                    
                    if isinstance(hora_inicio_td, timedelta):
                        hora_inicio = str(hora_inicio_td).split('.')[0]
                    else:
                        hora_inicio = hora_inicio_td
    
                    if isinstance(hora_fin_td, timedelta):
                        hora_fin = str(hora_fin_td).split('.')[0]
                    else:
                        hora_fin = hora_fin_td
                    
                    disponibilidad = Disponibilidad(
                        dias_semana=dias_semana,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin
                    )
                    disponibilidad_list.append(disponibilidad.serialize())
                
                DatabaseConnection.close_connection()
                return disponibilidad_list
            
            DatabaseConnection.close_connection()
            return []
        except Exception as e:
            raise Exception(f"Error al obtener la disponibilidad del profesional: {str(e)}")
        
    @classmethod
    def eliminar_disponibilidades(cls, id_profesional):
        '''Elimina todas las disponibilidades de un profesional'''
        try:
            query = 'DELETE FROM turnosDB.disponibilidad WHERE ID_Profesional = %s'
            DatabaseConnection.execute_query(query, (id_profesional,))
        except Exception as e:
            raise Exception(f"Error al eliminar las disponibilidades: {str(e)}")


    @classmethod
    def insertar_disponibilidades(cls, id_profesional, disponibilidades):
        '''Inserta nuevas disponibilidades para un profesional'''
        try:
            query = '''
            INSERT INTO turnosDB.disponibilidad (Dias_Semana, Hora_Inicio, Hora_Fin, ID_Profesional)
            VALUES (%s, %s, %s, %s)
            '''
            for disponibilidad in disponibilidades:
                DatabaseConnection.execute_query(
                    query,
                    (
                        disponibilidad['dias_semana'],
                        disponibilidad['hora_inicio'],
                        disponibilidad['hora_fin'],
                        id_profesional
                    )
                )
        except Exception as e:
            raise Exception(f"Error al insertar las disponibilidades: {str(e)}")


    @classmethod
    def modificar_disponibilidad(cls, id_profesional, disponibilidades):
        '''Modifica las disponibilidades de un profesional'''
        try:
            cls.eliminar_disponibilidades(id_profesional)
            cls.insertar_disponibilidades(id_profesional, disponibilidades)
        except Exception as e:
            raise Exception(f"Error al modificar las disponibilidades: {str(e)}")
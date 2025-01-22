from datetime import datetime, timedelta
from ..database import DatabaseConnection

class Recordatorio:
    @staticmethod
    def get_turnos_reservados(ahora, limite):
        """
        Obtiene los turnos reservados dentro de un rango de tiempo.
        """
        query = """
        SELECT p.nombre, p.apellido, pro.nombre, pro.apellido, t.fecha, t.hora, p.correo, pro.correo
        FROM turno t
        JOIN paciente p ON t.id_paciente = p.id_paciente
        JOIN profesional pro ON t.id_profesional = pro.id_profesional
        WHERE t.estado = 'Reservado' AND CONCAT(t.fecha, ' ', t.hora) BETWEEN %s AND %s
        """
        params = (ahora, limite)
        result = DatabaseConnection.fetch_all(query, params)
        DatabaseConnection.close_connection()
        return result

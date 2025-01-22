from flask_mail import Message
from datetime import datetime, timedelta
from . import mail
from ..notificaciones.recordatorio import Recordatorio

def send_reminder_emails():
    """
    Envía recordatorios para los turnos dentro de las próximas 24 horas.
    """
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    limite = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")

    # Obtener turnos reservados
    turnos = Recordatorio.get_turnos_reservados(ahora, limite)

    for turno in turnos:
        paciente_nombre = turno[0]
        paciente_apellido = turno[1]
        profesional_nombre = turno[2]
        profesional_apellido = turno[3]
        fecha = turno[4]
        hora = turno[5]
        paciente_correo = turno[6]
        profesional_correo = turno[7]

        fecha_hora = f"{fecha} {hora}"

        try:
            # Crear y enviar correo
            msg = Message(
                subject="Recordatorio de Turno",
                recipients=[paciente_correo, profesional_correo],
                body=(
                    f"Recordatorio: Tienes un turno programado para el {fecha_hora}.\n\n"
                    f"Paciente: {paciente_nombre} {paciente_apellido}\n"
                    f"Profesional: {profesional_nombre} {profesional_apellido}"
                )
            )
            mail.send(msg)
            print(f"Recordatorio enviado a {paciente_correo} y {profesional_correo}")
        except Exception as e:
            print(f"Error al enviar recordatorio: {e}")
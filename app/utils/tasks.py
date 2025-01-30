from notificaciones import enviar_recordatorio
from models.paciente_model import Paciente
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def enviar_recordatorios_turnos():
    """Envía recordatorios a los pacientes con turnos en 24 horas"""
    turnos = Paciente.get_turnos_proximos()
    
    for turno in turnos:
        id_turno, fecha, hora, pcorreo, pnombre, procorreo, pronombre = turno
        asunto = "Recordatorio de turno médico"
        cuerpo = f"Hola {pnombre},\n\nTe recordamos que tienes un turno programado para el {fecha} a las {hora}.\n\nSaludos,\nCentro Médico"
        
        try:
            enviar_recordatorio(pcorreo, asunto, cuerpo)
            enviar_recordatorio(procorreo, asunto, cuerpo)
            print(f"Recordatorio enviado a {pcorreo} para el turno {id_turno}")
            print(f"Recordatorio enviado a {procorreo} para el turno {id_turno}")
        except Exception as e:
            print(f"Error al enviar recordatorio a {pcorreo}: {e}")
            print(f"Error al enviar recordatorio a {procorreo}: {e}")

# Configurar APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(enviar_recordatorios_turnos, trigger=CronTrigger(hour=8, minute=0))  # Ejecuta todos los días a las 8 AM
scheduler.start()

print("Scheduler iniciado. Enviará recordatorios cada día a las 8 AM.")

# Mantener el script en ejecución si se ejecuta de manera independiente
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler detenido.")
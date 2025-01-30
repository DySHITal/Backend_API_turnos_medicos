from flask_mail import Message
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app import mail

def enviar_recordatorio(destinatario, asunto, cuerpo):
    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo
    mail.send(msg)

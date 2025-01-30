from flask_mail import Message
from __init__ import mail

def enviar_recordatorio(destinatario, asunto, cuerpo):
    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo
    mail.send(msg)

import os
import sys
from celery import Celery # розподіляє задачі.

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    print(x+y)
    return  x + y

def send_mail(recipient, subject, text):
    import smtplib, ssl

    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "irajhdhj@gmail.com"
    receiver_email = recipient
    password = os.environ.get('EMAIL_PASSWORD')
    message = text
    #msg = EmailMessage()

    context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    with smtplib.SMTP(host=smtp_server, port=port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


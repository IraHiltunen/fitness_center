import sys
from celery import Celery

app = Celery('tasks', broker='pyamdp://guest@localhost//')

@app.task
def add(x, y):
    print(x+y)
    return  x + y

def send_mail(recepient, subject, text):
    import smtplib, ssl

    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email ="ira.jhdhj@gmail.com"
    receive_email =recepient
    password = os.environ('email_password')
    message =text
    
    context = ssl.cr
    with smtplib.SMTP
        server.ehlo()
        server.start
        server.ehlo
        server.login
        server.sendmail
        
if __name__== 'main
    send_mail(sys.ar
from flask import request, session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import smtplib

from InsertData import AddAmount


def SandMail(mail,Payment):
    """отправка письма"""
    msg = MIMEMultipart()
    text="Thank u for shopping on "+str(Payment)
    password = "*"
    msg['From'] = "PacifistRaging@gmail.com"
    msg['To'] = mail
    msg['Subject'] = "Shopping"
    msg.attach(MIMEText(text, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()



def ClearTable():
    """очитска корзины"""
    if 'data' in session:
        AddAmount(session['data'])
        session.pop('data')

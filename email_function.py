from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
import os

def body(email_receiver):
    
    email_sender = 'h.proj.456712@gmail.com'
    email_password = 'uozuxyewcpauviak'
    
    subject = 'Twitter Report'
    msg = EmailMessage()

    with open('report.pdf', 'rb') as f:
        pdf_data = f.read()

    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='report.pdf')
    body_text = 'Here is an email that you asked for, containing an attachment of the report.'
    msg_body = MIMEText(body_text)
    msg.attach(msg_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as f:
        f.login(email_sender, email_password)
        f.sendmail(email_sender, email_receiver, msg.as_string())

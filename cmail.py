import smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('sravyasravya729@gmail.com','brvz iqow dicw uypl')
    msg=EmailMessage()
    msg['From']='sravyasravya729@gmail.com'
    msg['TO']=to
    msg['Subject']=subject
    msg.set_content(body)
    server.send_message(msg)
    server.quit()
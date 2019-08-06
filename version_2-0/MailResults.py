import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time

receivers_dict={
        'name':['Name', 'name@mailto.com']
                }

def send_via_email(receiver, path):
    sender='sender.mail@mail.com'
    date=list(time.localtime()[0:3])[::-1]
    passwd='password'
    port=465
    context=ssl.create_default_context()
    msg=MIMEMultipart()
    msg['From']=sender
    msg['To']=receiver[1]
    msg['Subject']='Your measurement results'
    message='''Dear {:s}
    
Here are your measurement results from {:02d}-{:02d}-{:d}. 

Results are attached to this message.'''.format(receiver[0],*date)

    msg.attach(MIMEText(message,'plain'))
    
    with open(path, "rb") as fil:
        part = MIMEApplication(fil.read(), Name='results')
        part['Content-Disposition']='attachment; filename=measurements.csv'
        msg.attach(part)

    
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender, passwd)
        server.sendmail(sender, receiver, msg.as_string())
        

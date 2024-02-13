from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import ssl
import os
import re

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv('APP_PASSWORD')
email_receiver = 'antony.dudnikov@parl.gc.ca'

def send_email(text, title):
    text = re.sub("```html", f"Today Statistics Canada released: {title}", text)
    # em = EmailMessage()
    # em['From'] = EMAIL
    # em['To'] = email_receiver
    # em['Subject'] = f"Summary: {title}"
    # em.set_content(text)

    #html gpt output
    message = MIMEMultipart('alternative')
    message['Subject'] = f"Summary: {title}"
    message['From'] = EMAIL
    message["To"] = email_receiver
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(text, 'html')
    #message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.sendmail(EMAIL, email_receiver, message.as_string())
    pass
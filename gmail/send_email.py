from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import smtplib, ssl, base64, google.auth
from dotenv import load_dotenv
import os
from email.message import EmailMessage

load_dotenv()

port = 465
PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL = os.getenv('EMAIL')
#C:\Users\anton\AppData\Local\Google\Cloud SDK
context = ssl.create_default_context()

def send_email():
    
    creds, _ = google.auth.default()
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message.set_content("This is an automated email from webscrapeHoC")

    message['To'] = EMAIL
    message["From"] = EMAIL
    message['Subject'] = "Automated email webscrapeHoC"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {'raw': encoded_message}

    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    return send_message


    # with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context, ) as server:
    #     server.login(EMAIL,PASSWORD)
    #     server.sendmail(from_addr=EMAIL, to_addrs= EMAIL, msg=message)

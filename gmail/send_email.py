from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
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




def send_email(text, title):
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    #creds, _ = google.auth.default()
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message = MIMEText(text)

    message['To'] = EMAIL
    message["From"] = EMAIL
    message['Subject'] = f"Summary: {title}"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {'raw': encoded_message}

    send_message = (service.users().messages().send(userId="me", body=create_message).execute()
    )
    return send_message


    # with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context, ) as server:
    #     server.login(EMAIL,PASSWORD)
    #     server.sendmail(from_addr=EMAIL, to_addrs= EMAIL, msg=message)

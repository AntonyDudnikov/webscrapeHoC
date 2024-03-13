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

advisor_details = {
    'Connor':{
        'email':"connor.macdonald@parl.gc.ca",
        'release_titles': []
    },
    'Sean':{
        'email': "sean.phelan@parl.gc.ca",
        'release_titles':[] 
    },
    'Mark':{
        'email': 'mark.emes@parl.gc.ca',
        'release_titles':[]
    },
    'Yuan': {
        'email': 'yuanyi.zhu@parl.gc.ca',
        'release_titles':[] 
    },
    'Elan':{
        'email':'elan.harper@parl.gc.ca',
        'release_titles':[]
    },
    'Darren': {
        'email':'darren.hall@parl.gc.ca',
        'release_titles':[]
    },
    'David':{
        'email':'david.murray@parl.gc.ca',
        'release_titles':[]
    },
    'Emma':{
        'email':'emma.hopper@parl.gc.ca',
        'release_titles':[]
    }
}

def send_email(text, title, institution):
    text = re.sub("```html", f"Today {institution} released: {title}", text)
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

def advisor_send(titles, advisors):
    """
    Automatic email sender that sends the advisors their corresponding related
    files inclusions into the database.

    Method:
        2. create a lsit for each advisor of corresponding titles
        3. create email content
        4. send email
    """
    for x in range(len(titles)):
        for y in range(2):
            match advisors[y][x]:
                case 'C. MacDonald':
                    advisor_details['Connor']['release_titles'].append(titles[x])
                case 'D. Hall':
                    advisor_details['Darren']['release_titles'].append(titles[x])
                case 'D. Murray':
                    advisor_details['David']['release_titles'].append(titles[x])
                case 'E. Harper':
                    advisor_details['Elan']['release_titles'].append(titles[x])
                case 'E. Hopper':
                    advisor_details['Emma']['release_titles'].append(titles[x])
                case 'M. Emes':
                    advisor_details['Mark']['release_titles'].append(titles[x])
                case 'S. Phelan':
                    advisor_details['Sean']['release_titles'].append(titles[x])
                case 'Y. Zhu':
                    advisor_details['Yuan']['release_titles'].append(titles[x])


if __name__ == "__main__":
    advisor_send(titles=["banana","orange"], advisors=[['E. Harper', 'M. Emes'],['S. Phelan', 'D. Murray']])

                


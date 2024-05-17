from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.text import MIMEText
from dotenv import load_dotenv
import dotenv
import pandas as pd
import datetime
import smtplib
import random
import ssl
import os
import re

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv('APP_PASSWORD')
email_receiver = 'antony.dudnikov@parl.gc.ca'

poilievre_quotes = ["Society is not a zero-sum game. One person's gain does not have to come at the expense of another's loss.", 
                    "Success is not about how much money you make, but about how many lives you touch positively.",
                    "Change is the law of life. Those who only look to the past or present are certain to miss the future.",
                    "A true leader is not afraid to take risks and make tough decisions.",
                    "Don't be afraid of failure. It is through failures that we learn and grow.",
                    "Strong individuals build strong communities.",
                    "Education is the most powerful weapon we can use to change the world.",
                    "The measure of a society is how it treats its most vulnerable members.",
                    "Great opportunities are often disguised as challenging situations.",
                    "Persistence and hard work are the foundation of success.",
                    "Focus on your strengths, not your weaknesses. Capitalize on what you're good at.",
                    "Leadership is not about power, but about influencing others to create positive change.",
                    "The pursuit of knowledge should be a lifelong journey.",
                    "The root cause of terrorism is terrorists.",
                    "Any politician promising not to raise your taxes is like a vampire promising to become a vegetarian.",
                    "The tax on capital gains in Canada is twice as high as in communist China and we wonder why our ideas are being held back.",
                    "We believe that the real child-care experts are mom and dad. That's why we brought in the universal child care benefit way back in 2006.",
                    "It's clear Justin Trudeau has something to hide.",
                    "My dreams of NHL glory were never fulfilled so I had to settle for politics instead.",
                    "wacko policy... wacko prime minister"]

full_email_recipients = {'David' : "david.murray@parl.gc.ca", "Jwane": "jwane.izzetpanah@parl.gc.ca"}

advisor_details = {
    'Connor':{
        'formal': 'C. MacDonald',
        'email':"connor.macdonald@parl.gc.ca"
    },
    'Sean':{
        'formal': 'S. Phelan',
        'email': "sean.phelan@parl.gc.ca"
    },
    'Mark':{
        'formal': 'M. Emes',
        'email': 'mark.emes@parl.gc.ca'
    },
    'Yuan': {
        'formal':'Y. Zhu',
        'email': 'yuanyi.zhu@parl.gc.ca'
    },
    'Elan':{
        'formal': 'E. Harper',
        'email':'elan.harper@parl.gc.ca'
    },
    'Darren': {
        'formal':'D. Hall',
        'email':'darren.hall@parl.gc.ca'
    },
    'David':{
        'formal':'D. Murray',
        'email':'david.murray@parl.gc.ca'
    },
    'Emma':{
        'formal': 'E. Hopper',
        'email':'emma.hopper@parl.gc.ca'
    }
}

def _extract_summary(html)->str:
    try:
        pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    except TypeError:
        return "Error extracting summary, visit the app to read more about this release. "
    

def _email_creation(todays_df, advisor):
    #get all releases that relate to the advisor
    current_advisor_df = todays_df[(todays_df['file_advisor_1'] == advisor_details[advisor]['formal']) | (todays_df['file_advisor_2'] == advisor_details[advisor]['formal'])].reset_index()
    if len(current_advisor_df) > 0: #check if empty
        email_content = f"""<p>GOOD MORNING {advisor}!</p><p>Today these reports, articles and news releases related to your files were included into the database:</p><h3>Releases related to your files</h3><ul>
        """
        for x in range(len(current_advisor_df)): #add releases and hyperlink
            email_content += f"<li>{current_advisor_df['institution'][x]} - <a href={current_advisor_df['url'][x]}>{current_advisor_df['title'][x]}</a></li>"
        email_content += '</ul><h3>Summaries of releases</h3><ul>'
        for x in range(len(current_advisor_df)): #add release summaries
            email_content += f"""<li><span style="text-decoration: underline;">{current_advisor_df['title'][x]}</span><ul><li>{_extract_summary(current_advisor_df['summary'][x])}</li></ul></li>"""
        email_content += f"""</ul><p>Please refer to the database application to read more about these releases.</p><p>Here is your Pierre quote of the day: "{random.choice(poilievre_quotes)}"<br><p>Have a great day!</p>"""
        message = MIMEMultipart('alternative')
        message['Subject'] = f"Summary: Recent inclusions to database related to your file"
        message['From'] = EMAIL
        #change to receiver 
        message["To"] = advisor_details[advisor]['email']
        part2 = MIMEText(email_content, 'html')
        message.attach(part2)
        context = ssl.create_default_context()
        #send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.sendmail(EMAIL, advisor_details[advisor]['email'], message.as_string())
        pass
        print(f"EMAIL SENT TO {advisor}")
    else:
        print(f"NOTHING TO SEND TO {advisor}")

#my personal email send that 
def send_email(text, title, institution, quotes):
    text = re.sub("```html", f"Today {institution} released: {title}", text)
    text += f"""<h3> Quotes</h3><p>{quotes}</p>"""
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

def advisor_send(files):
    """
    Automatic email sender that sends the advisors their corresponding related
    files inclusions into the database.

    Method:
        2. create a lsit for each advisor of corresponding titles
        3. create email content
        4. send email
    """
    #get today's releases from dataframe
    todays_df = files[files["date_retrieved"] == datetime.date.today().strftime("%d/%m/%Y")]
    if len(todays_df) == 0:
        todays_df = files[files["date_retrieved"] == datetime.date.today().strftime("%Y-%m-%d")]

    if len(todays_df) > 0:
        #loop through advisors
        for key in advisor_details:
            if key != "David":
                _email_creation(todays_df, key)

        #DAVID specific email send
        for key in full_email_recipients:

            email_content = f"""<p>Good Morning {key}!</p><p>Today these reports, articles and news releases were included into the database:</p><h3>Releases</h3><ul>
            """
            for x in range(len(todays_df)): #add releases and hyperlink
                email_content += f"<li>{todays_df['institution'][x]} - <strong><a href={todays_df['url'][x]}>{todays_df['title'][x]}</a></strong></li>"
            email_content += '</ul><h3>Summaries of releases</h3><ul>'
            for x in range(len(todays_df)): #add release summaries
                email_content += f"""<li><strong>{todays_df['title'][x]}</strong><ul><li>{_extract_summary(todays_df['summary'][x])}</li></ul></li>"""
            email_content += f"""</ul> <p>Please refer to the database application to read more about these releases.</p> <p>Here is your Pierre quote of the day: "{random.choice(poilievre_quotes)}"<br></p> <p>Have a great day!</p>"""
            message = MIMEMultipart('alternative')
            message['Subject'] = f"Summary: Recent inclusions to database"
            message['From'] = EMAIL
            #change to receiver 
            #message["To"] = "antony.dudnikov@parl.gc.ca"
            message["To"] = full_email_recipients[key]
            part2 = MIMEText(email_content, 'html')
            message.attach(part2)
            context = ssl.create_default_context()
            #send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
                smtp.login(EMAIL, PASSWORD)
                smtp.sendmail(EMAIL, full_email_recipients[key], message.as_string())
                #smtp.sendmail(EMAIL, "antony.dudnikov@parl.gc.ca", message.as_string())
            print(f"FULL EMAIL SENT TO {key}")
    else:
        print("Nothing to send!")
           



if __name__ == "__main__":
    all_files_copy = pd.read_csv("storage/final_loaded.csv")
    advisor_send(all_files_copy)


    

                


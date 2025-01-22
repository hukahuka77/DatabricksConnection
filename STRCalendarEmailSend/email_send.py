import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path
from dotenv import load_dotenv # pip install python-dotenv
from .get_calendar import get_calendar

# EMAIL_SERVER = "smtp-mail.outlook.com"
# EMAIL_SERVER = "smtp.gmail.com"

def send_email(subject, receiver_email, name):
    # For hostinger
    EMAIL_SERVER = "smtp.titan.email"
    PORT = 587

    #Load the environment variables
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars = current_dir / ".env"
    load_dotenv(envars)

    #read enviornment variables
    sender_email = os.getenv('EMAIL_SENDER')
    password_email = os.getenv('EMAIL_PASSWORD')
    bcc_email = os.getenv('EMAIL_BCC')

    #Initialize the email message
    msg = EmailMessage()
    msg ["Subject"] = subject
    msg["From"] = formataddr(("Alkaz Homes", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = bcc_email
    styles = """
    <style>
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th, td {
        border: 1px solid #ddd; /* Adds a border to table headers and cells */
        padding: 8px; /* Adds padding inside the cells */
        text-align: left;
      }
      th {
        background-color: #f2f2f2; /* Adds a background color to the header */
      }
    </style>
    """
    #getting and preparing events calendar
    events = get_calendar()
    events_html = '<table><tr><th>Name</th><th>Start Date</th><th>End Date</th><th>Length</th></tr>'
    for event in events:
        events_html += f"<tr><td>{event[4]}</td><td>{event[0]} 3:00 PM</td><td>{event[1]} 10:00 AM</td><td>{event[5]} Day(s)</td></tr>"
    events_html += '</table>'

    msg.add_alternative(
        f"""\
    <html>
      <head>
        {styles}
      </head>
      <body>
        <p>Hi {name},</p>
        <p>Here is the booking schedule at 3044 W Sierra Vista Dr. as of today, {event[7]}:<p>
        {events_html}
        <p style="font-family: Arial, sans-serif; font-size: 16px; color: #333; line-height: 1.5;">
        Link to calendar view: 
        <a href="https://alkazhomes.com/pages/sierra.html" 
            style="text-decoration: none; color: #1a73e8; font-weight: bold;">
            Calendar
        </a>
        </p>
        <p>Best Regards,</p>
        <p></p>
        <strong><p>Andrew Long-Kettenhofen</p>
        <p>Alkaz Homes </p>
        <p>(925) 413-6561</p></strong>
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.send_message(msg)

import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr  
from pathlib import Path
from dotenv import load_dotenv # pip install python-dotenv
from .get_calendar import get_calendar

# EMAIL_SERVER = "smtp-mail.outlook.com"
# EMAIL_SERVER = "smtp.gmail.com"

def send_email(subject, receiver_email, name):
    # For hostinger
    server_email = os.environ.get('EMAIL_SERVER')
    port = 587


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
    # Define the email styles
    styles = """
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #F0F0E6; /* Off-white from logo sky */
        margin: 0;
        padding: 20px;
      }
      .container {
        max-width: 650px;
        margin: 0 auto;
        background-color: #ffffff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      }
      .header {
        background-color: #e4e9d5; /* nice green */
        color: #000000;
        padding: 25px;
        text-align: center;
      }
      .header h1 {
        margin: 0;
        font-size: 24px;
      }
      .content {
        padding: 30px;
        color: #2A2B2A; /* Dark brown from logo text */
        line-height: 1.6;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
      }
      th, td {
        border: 1px solid #dddddd;
        padding: 12px;
        text-align: left;
      }
      th {
        background-color: #e4e9d5; /* nice green */
        font-weight: bold;
        color: #2A2B2A;
      }
      tr:nth-child(even) {
        background-color: #f9f9f9;
      }
      .cta-button {
        display: inline-block;
        background-color: #e65617; /* user-specified orange */
        color: #ffffff !important;
        padding: 12px 25px;
        margin-top: 15px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
      }
      .footer {
        padding: 20px 30px;
        font-size: 14px;
        color: #2A2B2A;
      }
      .footer p {
        margin: 5px 0;
      }
    </style>
    """

    # Get calendar data
    events = get_calendar()
    
    # Check if events list is empty to avoid errors
    if not events:
        logging.warning("No events found in the calendar. Email will be sent without a schedule.")
        events_html = "<p>No upcoming bookings found.</p>"
        current_date = "today"
    else:
        # Build the HTML table for events
        events_html = '<table><tr><th>Name</th><th>Start Date</th><th>End Date</th><th>Length</th></tr>'
        for event in events:
            # event format: (start_date, end_date, description, uid, name, length, other, current_date)
            events_html += f"<tr><td>{event[4]}</td><td>{event[0]} 3:00 PM</td><td>{event[1]} 10:00 AM</td><td>{event[5]} Day(s)</td></tr>"
        events_html += '</table>'
        current_date = events[0][7] # Get date from the last field of the first event

    # Add the HTML body to the email
    msg.add_alternative(
        f"""\
    <html>
      <head>
        {styles}
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Alkaz Homes Booking Schedule</h1>
          </div>
          <div class="content">
            <p>Hi {name},</p>
            <p>Here is the booking schedule for 3044 W Sierra Vista Dr. as of {current_date}:</p>
            {events_html}
            <p>For a live view of the calendar, please click the button below:</p>
            <a href="https://alkazhomes.com/pages/sierra.html" class="cta-button">
              View Live Calendar
            </a>
          </div>
          <div class="footer">
            <p>Best Regards,</p>
            <p><strong>Andrew Long-Kettenhofen</strong><br>
               Alkaz Homes<br>
               (925) 413-6561</p>
          </div>
        </div>
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(server_email, port) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.send_message(msg)

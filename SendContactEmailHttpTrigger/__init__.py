import azure.functions as func
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
from dotenv import load_dotenv # pip install python-dotenv
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Email sending function triggered.")
    print("Email sending function triggered.")

    # Parse request for email input
    email = req.params.get("email")
    name = req.params.get("name")
    subject = req.params.get("subject")
    message = req.params.get("message")

    if not email or not name:
        print("Please provide both 'email' and 'name' parameters in the query string.")
        return func.HttpResponse(
            "Please provide both 'email' and 'name' parameters in the query string.",
            status_code=400
        )

    
    # Email content
    subject = f"Your message has been received: {subject}" 
    body = f"Hello {name},\n\nThank you for submitting your message. It has been received. Below is the recorded message:\n\n{message}\n\nI will get back to you shortly!\n\nBest Regards,\nAndrew Long-Kettenhofen"
    
    #Load the environment variables
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars = current_dir / ".env"
    load_dotenv(envars)

    # Configure email settings
    sender_email = os.getenv('EMAIL_SENDER')
    sender_name = "Andrew Long-Kettenhofen"
    password_email = os.environ.get('EMAIL_PASSWORD')
    EMAIL_SERVER = "smtp.titan.email"
    PORT = 587

    formatted_sender = f'"{sender_name}" <{sender_email}>'

    try:
        # Set up the MIME email
        message = MIMEMultipart()
        message["From"] = formatted_sender
        message["To"] = email
        message["Subject"] = subject
        message["BCC"] = "andrew.kettenhofen@gmail.com"
        message.attach(MIMEText(body, "plain"))
        print("Email message created.")
        # Send email using SMTP
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()  # Secure the connection
            print("Connection secured.")
            server.login(sender_email, password_email)
            server.send_message(message)

        logging.info(f"Email sent successfully to {email}")
        print(f"Email sent successfully to {email}")
        return func.HttpResponse(f"Email sent successfully to {email}", status_code=200)

    except Exception as e:
        logging.error(f"Error sending email: {e}")
        print(f"Error sending email: {e}")
        return func.HttpResponse(
            f"Failed to send email. Error: {str(e)}",
            status_code=500
        )
    
if __name__ == "__main__":
    # Test the function
    req = func.HttpRequest(
        method='POST',
        url='/api/test',
        headers={},
        params={'email': 'andrew.whitelock@yahoo.com', 'name': 'Whatchacallit', 'subject': 'heres teh subjcet', 'message': 'I wanna send you a message because this is a test and you really should get this message.'},  # Simulate query parameters
        body=json.dumps({}).encode('utf-8')  # Simulate request body
    )
     
    main(req)
    # for key, value in os.environ.items():
    #  print(f"{key}: {value}")
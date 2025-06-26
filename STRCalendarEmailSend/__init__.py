import os
import logging
import azure.functions as func
from .email_send import send_email
import json
from pathlib import Path
from dotenv import load_dotenv # pip install python-dotenv


def main(myTimer: func.TimerRequest) -> None:
    logging.info('Trigger executed. Starting job')
    
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars = current_dir / ".env"
    load_dotenv(envars)

    # Load emails from environment variables
    emails_list_str = os.getenv('EMAILS_LIST')
    if not emails_list_str:
        logging.error('Failed to retrieve EMAILS_LIST from environment variables.')
        return

    try:
        emails_list = json.loads(emails_list_str)
    except json.JSONDecodeError:
        logging.error('EMAILS_LIST environment variable is not a valid JSON string.')
        return

    # Send emails
    for name, email in emails_list.items():
        try:
            send_email("3044 W Sierra Vista Calendar", email, name)
            logging.info(f'Email Sent to {email}')
        except Exception as e:
            logging.error(f'Failed to send email to {email}. Error: {e}')

    # Check timer status
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function executed.')

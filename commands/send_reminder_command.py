from integrations.email_util import send_expenses_reminder_email
from dotenv import load_dotenv
import os
from utils.logger_factory import LoggerFactory

load_dotenv()

SUBJECT = os.getenv('SUBJECT')
SENDER = os.getenv('SENDER')
RECIPIENTS = os.getenv('RECIPIENTS')
PASSWORD = os.getenv('PASSWORD')

logger = LoggerFactory.get_logger("EXPENSES REMINDER", log_level="INFO")


def send_reminder_command():
    try:
        send_expenses_reminder_email(SUBJECT, SENDER, [RECIPIENTS], PASSWORD)
        logger.error(f"Reminder sent successfully")
    except (BrokenPipeError, IOError) as error:
        logger.error(f"Expenses Reminder - {type(error).__name__}: {error}")


if __name__ == '__main__':
    send_reminder_command()

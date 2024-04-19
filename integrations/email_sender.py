import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os

load_dotenv()
SENDER = os.getenv('SENDER')
RECIPIENTS = os.getenv('RECIPIENTS')
PASSWORD = os.getenv('PASSWORD')


def send_template_email(subject, template, attachment_path=None):
    message = MIMEMultipart()
    message['From'] = SENDER
    message['To'] = ', '.join([RECIPIENTS])
    message['Subject'] = subject

    # Add the HTML content to the message
    message.attach(MIMEText(template, 'html'))

    # Add attachment
    if attachment_path:
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEApplication(attachment_file.read(), Name=attachment_path)
            attachment['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
            message.attach(attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, ) as smtp_server:
        smtp_server.login(SENDER, PASSWORD)
        smtp_server.sendmail(SENDER, RECIPIENTS, message.as_string())


def generate_html_template(template_path, content):
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    template_dir = os.path.join(parent_dir, "templates")

    env = Environment(loader=FileSystemLoader(template_dir))

    # Carga la plantilla
    template = env.get_template(template_path)

    # Renderiza la plantilla con los datos proporcionados
    rendered_template = template.render(content=content)
    return rendered_template


def send_task_template(content):
    html_template = generate_html_template('task_reminder.html', content)
    send_template_email("Pending Tasks", html_template)

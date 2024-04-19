import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from jinja2 import Template
from flask import Flask, render_template


def send_email(subject, sender, recipients, password, content, date, username, attachment_path=None):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    # Add the template and replace the markers
    with open('template.html', 'r') as f:
        html_template = f.read()

    html_content = html_template.format(username=username, date=date, content=content)

    # Add the HTML content to the message
    message.attach(MIMEText(html_content, 'html'))

    # Add attachment
    if attachment_path:
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEApplication(attachment_file.read(), Name=attachment_path)
            attachment['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
            message.attach(attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, ) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, message.as_string())


def send_expenses_reminder_email(subject, sender, recipients, password, attachment_path=None):
    message = MIMEMultipart()
    message['From'] = formataddr(("SimplyDevTools", sender))
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    # Add the template and replace the markers
    with open('./templates/daily_reminder.html', 'r') as f:
        html_template = f.read()

    # Add the HTML content to the message
    message.attach(MIMEText(html_template, 'html'))

    # Add attachment
    if attachment_path:
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEApplication(attachment_file.read(), Name=attachment_path)
            attachment['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
            message.attach(attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, ) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, message.as_string())


def send_task_reminder_email(subject, sender, recipients, password, injected_html, ):
    message = MIMEMultipart()
    message['From'] = formataddr(("SimplyDevTools", sender))
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    app = Flask(__name__, template_folder='templates')
    tasks = [
        {"title": "qwe", "status": "new"},
        {"title": "rter", "status": "new"},
        {"title": "dsdvxcvsds", "status": "new"}
    ]

    rendered = render_template("task_reminder.html", tasks=tasks)

    # Add the HTML content to the message
    message.attach(MIMEText(rendered, 'html'))


    with smtplib.SMTP_SSL('smtp.gmail.com', 465, ) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, message.as_string())

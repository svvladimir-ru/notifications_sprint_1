import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from services.notification import settings


def send_mail(to, subject, content):
    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            message = EmailMessage()
            message["From"] = settings.SMTP_USER
            message["To"] = ",".join([to])
            message["Subject"] = subject

            env = Environment(loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))
            template = env.get_template('mail.html')

            output = template.render(**{
                'username': content.get('username'),
                'link': content.get('link'),
                'title': content.get('title'),
                'description':  content.get('description'),
                'unsubscribe': content.get('unsubscribe')
            })

            message.add_alternative(output, subtype="html")
            server.sendmail(settings.SMTP_USER, [to], message.as_string())
            server.close()

    except Exception:
        return False, "exception"
    else:
        return True, "ok"
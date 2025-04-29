from django.core.mail import send_mail
from django.conf import settings


class EmailConfig():
    def __init__(self, email_to=[], subject="", body="", html=""):
        self.email_to = email_to
        self.subject = subject
        self.body = body
        self.html = html

def send_email(ec):
    try:
        email_from = settings.EMAIL_FROM_DEFAULT
    except:
        email_from = "noresponse@fundec.org"
    send_mail(ec.subject, ec.body, email_from, ec.email_to, html_message=ec.html)

def send_warning_level_email(email_to, subject, html):
    ec = EmailConfig(email_to, subject, "", html)
    send_email(ec)



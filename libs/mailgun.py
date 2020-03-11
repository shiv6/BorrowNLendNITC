import os
from requests import Response, post


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Mailgun:
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    FROM_TITLE = 'stores REST API'
    FROM_EMAIL = 'postmaster@sandboxe4d9734075ab496a999328f2ea91a9ea.mailgun.org'

    @classmethod
    def send_email(cls, email, subject, text, html):
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException('mailgun_failed_load_api_key')

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException('mailgun_failed_load_domain')
        
        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                'from': f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                'to': email,
                'subject': subject,
                'text': text,
                'html': html,
            }
        )

        if response.status_code != 200:
            raise MailGunException('mailgun_error_send_email')
        return response
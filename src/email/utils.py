import requests
import os

def send_transac_email(recipient, content, subject):
    mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
    mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
    
    return requests.post(
        mailgun_domain,
        auth=("api", mailgun_api_key),
        data={"from": "Girok <admin@girok.org>",
            "to": [recipient],
            "subject": subject,
            "html": content
        }
    )
    
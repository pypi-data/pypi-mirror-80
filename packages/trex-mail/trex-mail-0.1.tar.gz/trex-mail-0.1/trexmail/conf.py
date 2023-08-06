import os

SENDGRID_API_KEY                                    = os.environ['SENDGRID_API_KEY']


MAILJET_API_KEY                                     = os.environ['MAILJET_API_KEY']
MAILJET_SECRET_KEY                                  = os.environ['MAILJET_SECRET_KEY']

FLASK_MAIL_USERNAME                                 = os.environ['FLASK_MAIL_USERNAME']
FLASK_MAIL_PASSWORD                                 = os.environ['FLASK_MAIL_PASSWORD']
FLASK_MAIL_SERVER                                   = os.environ['FLASK_MAIL_SERVER']
FLASK_MAIL_SERVER_PORT                              = os.environ['FLASK_MAIL_SERVER_PORT']
FLASK_MAIL_USE_SSL                                  = os.environ['FLASK_MAIL_USE_SSL']

DEFAULT_SENDER                                      = os.environ['DEFAULT_SENDER']
DEFAULT_RECIPIENT_EMAIL                             = os.environ['DEFAULT_RECIPIENT_EMAIL']
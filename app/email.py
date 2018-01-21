import os
from flask import current_app
from flask import render_template
from flask_mail import Message

from app import mail
from app.decorators import AsyncEmail as asynchronous


@asynchronous.send_email
def asynchronous_sending(message):
    with current_app.app_context():
        mail.send(message)


def send_email(email, full_name, username, password):
    subject = 'Registration on enceladus <user@example.com>'
    mail_username = os.environ.get('MAIL_USERNAME')
    message = Message(subject, sender=mail_username, recipients=[email])
    message.html = render_template('email/message.html', full_name=full_name,
                                   username=username, password=password)
    asynchronous_sending(message)

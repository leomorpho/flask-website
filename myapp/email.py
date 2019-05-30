from flask_mail import Message
from flask import render_template
from myapp import mail, app


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    app_name = app.config['APP_NAME']
    subject = "[%s] Reset your password" % (app.config['APP_NAME'])
    send_email(subject,
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template(
                   'email/reset_password.txt', user=user,
                   token=token, app_name=app_name),
               html_body=render_template(
                   'email/reset_password.html', user=user,
                   token=token, app_name=app_name))

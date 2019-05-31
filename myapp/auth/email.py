from flask import render_template, current_app
from myapp.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    app_name = current_app.config['APP_NAME']
    subject = "[%s] Reset your password" % (current_app.config['APP_NAME'])
    send_email(subject,
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template(
                   'email/reset_password.txt', user=user,
                   token=token, app_name=app_name),
               html_body=render_template(
                   'email/reset_password.html', user=user,
                   token=token, app_name=app_name))

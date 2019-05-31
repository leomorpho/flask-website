from flask_mail import Message
from flask import render_template
from threading import Thread
from myapp import mail, app


def send_async_email(app, msg):
    # The application context that is created with the 'with
    # app.app_context()' call makes the application instance
    # accessible via the current_app variable from Flask.
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # Send messages asyncronously to not hog up the app.
    # Notice that the app instance is sent as an argument. Flask
    # uses contexts to avoid having to pass argmts across functions.
    # There are 2 types of context: the application and the request
    # context. In most cases, the contexts are automatically managed
    # by the framework, but they may require to be set manually
    # for custom threads.
    # The reason that many extensions need to know the context (i.e.
    # the application instance) is because they have their config
    # stored in the app.config object.
    # In this case here, flask-mail need to access config settings
    # for the email server stored in app.config.
    Thread(target=send_async_email, args=(app, msg)).start()

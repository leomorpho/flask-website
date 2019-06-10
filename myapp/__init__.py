from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
import pusher
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
# admin = Admin()
# login_view is used by LoginManager for pages that require
# that user be logged-in.
login.login_view = 'auth.login'

pusher = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_APP_KEY'),
    secret=os.getenv('PUSHER_APP_SECRET'),
    cluster=os.getenv('PUSHER_APP_CLUSTER'),
    ssl=True)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Flask-Bootstrap optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
#     admin.init_app(app)

    # Register Blueprints
    from myapp.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from myapp.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from myapp.main import bp as main_bp
    app.register_blueprint(main_bp)

    from myapp.store import bp as store_bp
    app.register_blueprint(store_bp, url_prefix='/store')

    from myapp.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # If not in debug mode, log all errors
    if not app.debug and not app.testing:
        # Emailing
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Olivier\'s Breads Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/website.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: \
                    %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("%s startup" % (app.config['APP_NAME']))

    return app


# from myapp must be at the bottom of __init__ to avoid circular imports!!!
from myapp import models

import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
# .env file cannot be used for python FLASK_APP and FLASK_DEBUG
# environment variables, because they are needed very early in the
# application bootstrap process, before the app instance and its
# configuration object exist.
# Furthermore, do not add env to version control because it includes
# secret keys and other info that should stay confidential
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    APP_NAME = ['Olivier\'s Breads']
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['leonard.audibert@gmail.com']
    POSTS_PER_PAGE = 15

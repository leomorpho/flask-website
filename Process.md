# Development Process of a Flask Website

## Start Here
1. Make a virtual environment in a new project `python3 -m venv venv`
2. Activate virtual environment `source venv/bin/activate` or with my shell alias `venv`
3. Install flask `pip install flask`
4. Make a `myapp` directory inside project directory.
5. In the _myapp_ package, create a _\__init\__.py_ file.

~~~sh
# Make a new project directory
$ mkdir project

# Make virtual environment in project directory
$ cd project
$ python3 -m venv venv

# Activate virtual environment
$ venv

# Create a new app
(venv) $ nvim my_app.py
~~~

~~~py
# my_app.py
from myapp import app
~~~

~~~sh
# Make a new package
(venv) $ mkdir myapp

# Add the new package to the app
(venv) $ cd myapp
(venv) $ nvim __init__.py
~~~

~~~py
# __init__.py
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Avoid circular import by placing this at bottom (Flask peculiarity)
from myapp import routes
~~~

~~~sh
(venv) $ pip install python-dotenv
(venv) $ echo 'FLASK_APP=myapp.py' >> .flaskenv
~~~
---

## Web Forms
~~~sh
(venv) $ pip install flask-wtf
~~~

Form validators that have the form (no pun intended) `validate_X` validate the `X` property of the form.
e.g.: `validate_username` is automatically called for a `username` property of a form.

---
## Database
### Database Intro
~~~sh
(venv) $ pip install flask-sqlalchemy
(venv) $ pip install flask-migrate

# Create migration repository
# FLASK_APP must be set for the flask command to work
(venv) $ flask db init
 Creating directory /home/miguel/microblog/migrations ... done
 Creating directory /home/miguel/microblog/migrations/versions ... done
 Generating /home/miguel/microblog/migrations/alembic.ini ... done
 Generating /home/miguel/microblog/migrations/env.py ... done
 Generating /home/miguel/microblog/migrations/README ... done
 Generating /home/miguel/microblog/migrations/script.py.mako ... done
 Please edit configuration/connection/logging settings in
 '/home/miguel/microblog/migrations/alembic.ini' before proceeding.

 # If it is the 1st migration, a database will be created
 (venv) $ flask db migrate -m "A description of the changes made to the db"
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.autogenerate.compare] Detected added table 'user'
 INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
 INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
 Generating /home/miguel/microblog/migrations/versions/e517276bb1c2_users_table.py ... done

 # Generate migration script. Note that it makes no changes to the db.
 # In case you want to revert to a previous migration script, use 'downgrade' option.
 (venv) $ flask db upgrade
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.runtime.migration] Running upgrade  -> e517276bb1c2, users table

~~~
Note that Flask-SQLAlchemy uses snake-case for table names. For a `User` model, the corresponding table will be called `user`. For `AddressAndPhone` it will be `address_and_phone`. The `__tablename__` attribute can be added to name the tables yourself.

By now \__init\__.py should look somewhat like the following:
~~~py
# __init__.py in myapp package
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
~~~

The representation of a **many-to-many relationship** requires the use of an **auxiliary table** called an association table.

---

## Python Email
Register the mailing stuff in the config:
~~~py
class Config(object):
    # ...
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
~~~

In `__init__.py` register mail:
~~~py
import logging
from logging.handlers import SMTPHandler

# ...

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
~~~

Start a debugging SMTP server. This server will accept emails, print them to the terminal, but it will not send them.
~~~sh
(venv) $ python -m smtpd -n -c DebuggingServer localhost:8025
~~~

Leave the SMTP server running, then stop your flask app, set

~~~sh
export MAIL_SERVER=localhost
export MAIL_PORT=8025
export MAIL_DEBUG=0
~~~

A second approach is to set a real email server. Below is a configuration for a gmail account's web server:
~~~sh
export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=<your-gmail-username>
export MAIL_PASSWORD=<your-gmail-password>
~~~
Gmail security features may prevent the application from sending emails through it unless you explicitly allow "less secure apps" to access your gmail account.

[More info about gmail settings here](https://support.google.com/accounts/answer/6010255?hl=en)

---

## App factories

Create an app with a config file when blueprints are imported. Multiple instances can thus be created.
This idea is to setup an application in a function like this:
~~~py
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from yourapplication.model import db
    db.init_app(app)

    from yourapplication.views.admin import admin
    from yourapplication.views.frontend import frontend
    app.register_blueprint(admin)
    app.register_blueprint(frontend)

    return app
~~~
To get access to the app with the config, use `current_app`.

---

## Git

~~~sh
# Create a new commit that represents exactly the same state of the project as f414f31,
# but just adds that on to the history, so you don't lose any history.
git reset --hard f414f31
git reset --soft HEAD@{1}
git commit -m "Reverting to the state of the project at f414f31"
~~~


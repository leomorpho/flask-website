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

---
## Database

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

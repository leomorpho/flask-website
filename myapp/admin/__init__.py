from flask import Blueprint

# Don't call it 'admin' since it clashes with flask-admin
# default bp
bp = Blueprint('admin_panel', __name__)

from myapp.store import routes

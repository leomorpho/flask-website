from flask import Blueprint

bp = Blueprint('store', __name__)

from myapp.store import routes

from flask import Blueprint

bp = Blueprint('errors', __name__)

# Keep import at bottom to avoid circular imports
from myapp.errors import handlers

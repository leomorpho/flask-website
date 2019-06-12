from flask import Blueprint
from myapp.models import Permission

# Don't call it 'admin' since it clashes with flask-admin
# default bp
bp = Blueprint('admin_panel', __name__)

# context processors make variables globally available to
# all templates used by this blueprint
@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

from myapp.admin import routes, forms

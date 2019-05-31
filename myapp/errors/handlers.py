from flask import render_template
from myapp import db
from myapp.errors import bp

# While the simple @app.errorhandler() will work the same as
# the following, the idea is to make the blueprint as
# independent of the application as possible so that it
# is more portable.
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

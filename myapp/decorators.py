from functools import wraps
from flask import abort
from flask_login import current_user
import datetime
from myapp.models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


def time_this(function_to_time):
    def decorator(*args, **kwargs):
        before = datetime.datetime.now()
        x = function_to_time(*args, **kwargs)
        after = datetime.datetime.now()
        print("Elapsed time = {}").format(after-before)
        return x
    return decorator

# from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask import current_app, render_template, flash, redirect, \
        url_for
from myapp import db, admin
from myapp.models import User, Post, Product

# admin = Admin(current_app, name='Dashboard')

# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Post, db.session))
# admin.add_view(ModelView(Product, db.session))

# @bp.route('/')
# def admin():
#
#     return render_template('admin/index.html')


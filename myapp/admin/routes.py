from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import current_app
from myapp import db
from myapp.models import User, Post, Product

admin = Admin(current_app, name='Dashboard')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Product, db.session))
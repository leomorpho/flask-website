from myapp import create_app, db
from myapp.models import User, Post, Product, ProductCategory,\
        Role

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Product': Product,
            'ProductCategory': ProductCategory, 'Role': Role}

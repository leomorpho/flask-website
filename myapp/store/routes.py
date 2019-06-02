from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from myapp.models import Product
from myapp.store import bp
from myapp.store.forms import CreateNewProductForm


@bp.route('/')
def store():
    # get all products and present them
    products = Product.query.all()
    return render_template('store/index.html',
                           title='Store', products=products)


@bp.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    form = CreateNewProductForm()

# @bp.route('/store/<product_name>')
# def store(product_name):
#     product = Product.query.filter_by(name=product_name).first_or_404()
#     return render_template('index.html', title='Store')

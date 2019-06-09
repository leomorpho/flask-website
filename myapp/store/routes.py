from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from myapp.models import Product, ProductCategory
from myapp.store import bp
from myapp.store.forms import CreateNewProductForm, \
        EditProductForm
from myapp import db


@bp.route('/')
def store():
    # get all products and present them
    products = Product.query.all()
    return render_template('store/index.html',
                           title='Store', products=products)


@bp.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    categories = ProductCategory.query.order_by('name')
    form = CreateNewProductForm()
    form.category.choices = [(c.id, c.name) for c in categories]
#     if request.method == 'POST':
#         category = ProductCategory.query.filter_by(
#                 id=form.category.data).first()
#         return 'Name: {}, Category: {}'.format(form.name.data, category.name)
    if form.validate_on_submit():
        category = ProductCategory.query.filter_by(
                id=form.category.data).first()
        product = Product(
            name=form.name.data,
            description=form.description.data,
            # image=form.image.data,
            # Create a method to make a thumbnail from a full image?
            # thumbnail=
            # Not sure about how to add category to a new product
            category=category,
            weight=form.weight.data)
        db.session.add(product)
        db.session.commit()
        flash('Your product has been added!')
        return redirect(url_for('store.store'))
    return render_template('store/create_product.html',
                           form=form)


# @bp.route('/create_product', methods=['GET', 'POST'])
# @login_required
# def edit_product():
#     form = EditProductForm()
#     form.category.choices = [(c.id, c.name) for c in
#                              ProductCategory.query.order_by('name')]
#     if form.validate_on_submit():
#         category = ProductCategory.query.filter_by(
#             form.category.data)
#         product = Product(
#             name=form.name.data,
#             description=form.description.data,
#             # image=form.image.data,
#             # Create a method to make a thumbnail from a full image?
#             # thumbnail=
#             # Not sure about how to add category to a new product
#             category=category,
#             weight=form.weight.data)

# @bp.route('/store/<product_name>')
# def store(product_name):
#     product = Product.query.filter_by(name=product_name).first_or_404()
#     return render_template('index.html', title='Store')

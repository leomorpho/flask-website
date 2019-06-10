from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from myapp.models import Product, ProductCategory
from myapp.store import bp
from myapp.store.forms import ProductForm
from myapp import db


@bp.route('/')
def store():
    # get all products and present them
    products = Product.query.all()
    return render_template('store/index.html',
                           title='Store', products=products)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    Add a new product to the database
    """
    categories = ProductCategory.query.order_by('name')
    form = ProductForm()
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
    return render_template('store/crud_product.html',
                           form=form, title='Add Product')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Edit a product stored in database
    """
    product = Product.query.get_or_404(id)
    current_category = product.category
    categories = ProductCategory.query.all()
    # 1. Remove current product category from full list
    for c in categories:
        if c == current_category:
            categories.remove(c)
    # Sort list alphabetically

    categories.sort(key=lambda x: x.name)

    # 3. Prepend categories with the current category of the product
    categories.insert(0, current_category)

    form = ProductForm(obj=product)
    form.category.choices = [(c.id, c.name) for c in categories]
#     if request.method == 'POST':
#         category = ProductCategory.query.filter_by(
#                 id=form.category.data).first()
#         return 'Name: {}, Category: {}'.format(form.name.data, category.name)
    if form.validate_on_submit():
        category = ProductCategory.query.filter_by(
            id=form.category.data).first()
        product.name = form.name.data,
        product.description = form.description.data,
        # image=form.image.data,
        # Create a method to make a thumbnail from a full image?
        # thumbnail=
        # Not sure about how to add category to a new product
        product.category = category,
        product.weight = form.weight.data
        db.session.commit()
        flash('Your product has been updated!')
        return redirect(url_for('store.store'))
    form.name.data = product.name
    form.description.data = product.description
    form.category.data = product.category
    form.weight.data = product.weight
    return render_template('store/crud_product.html',
                           form=form, product=product,
                           title='Update Product')


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """
    Delete a product from the database
    """
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('You have successfully deleted this product')

    return redirect(url_for('store.store'))

    return render_template('crud_product.html', title='Delete Product')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired
from myapp.models import Product


class ProductForm(FlaskForm):
    """
    Form for admin to add or delete a product
    """
    #    product = FormField(ProductForm)
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    # image = check file upload for flask-form
    category = SelectField('Category', coerce=int)
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Product name already in use. \
                    Please use a different one.')


# class CreateNewProductForm(FlaskForm):
#     #    product = FormField(ProductForm)
#     name = StringField('Product Name', validators=[DataRequired()])
#     description = StringField('Product Description',
#                               validators=[DataRequired()])
#     # image = check file upload for flask-form
#     category = SelectField('Category', coerce=int)
#     weight = IntegerField('Weight (grams)', validators=[DataRequired()])
#     submit = SubmitField('Create Product')
#
#     def validate_name(self, name):
#         product = Product.query.filter_by(name=name.data).first()
#         if product is not None:
#             raise ValidationError('Product name already in use. \
#                     Please use a different one.')
#
#
# class EditProductForm(FlaskForm):
#     name = StringField('Product Name', validators=[DataRequired()])
#     description = StringField('Product Description',
#                               validators=[DataRequired()])
#     # image = check file upload for flask-form
#     category = SelectField('Category', coerce=int)
#     weight = IntegerField('Weight (grams)', validators=[DataRequired()])
#     submit = SubmitField('Update Product')
#
#     def __init__(self, original_specs, *args, **kwargs):
#         super(EditProductForm, self).__init__(*args, **kwargs)
#         # original product specs saved as instance variables
#         self.original_name = original_specs.name
#
#     def validate_name(self, name):
#         if name.data != self.original_name:
#             product = Product.query.filter_by(
#                 name=self.name.data).first()
#             if product is not None:
#                 raise ValidationError('Product name already in use. \
#                         Please use a different one.')

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, \
    IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired
from myapp.models import Product


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    # image = check file upload for flask-form
    category = SelectField('Category', coerce=int)
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Product name already in use. \
                    Please use a different one.')


class CreateNewProductForm(FlaskForm):
    #    product = FormField(ProductForm)
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    # image = check file upload for flask-form
    category = SelectField('Category', coerce=int)
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])
    submit = SubmitField('Create Product')

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Product name already in use. \
                    Please use a different one.')


class EditProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    # image = check file upload for flask-form
    category = SelectField('Category')
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])
    submit = SubmitField('Create Product')

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Product name already in use. \
                    Please use a different one.')
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different username.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different email address.')

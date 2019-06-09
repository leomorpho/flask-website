from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length


class CreateNewProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    # image = check file upload for flask-form
    # category = StringField('Category',
    #                       validators=[DataRequired()])
    weight = IntegerField('Weight (grams)', validators=[DataRequired()])
    submit = SubmitField('Create Product')

#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different username.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different email address.')

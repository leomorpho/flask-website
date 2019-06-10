from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired
from myapp.models import Role


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])

    def validate_name(self, name):
        role = Role.query.filter_by(name=name.data).first()
        if role is not None:
            raise ValidationError('Role name already in use. \
                    Please use a different one.')

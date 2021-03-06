# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Poll, Role

class PollForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class VotersAssignForm(FlaskForm):
    """
    Form for admin to assign polls and roles to employees
    """
    poll = QuerySelectField(query_factory=lambda: Poll.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

# class RegistrationForm(FlaskForm):
#     """
#     Form for users to create new account
#     """
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     username = StringField('Username', validators=[DataRequired()])
#     first_name = StringField('First Name', validators=[DataRequired()])
#     last_name = StringField('Last Name', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[
#                                         DataRequired(),
#                                         EqualTo('confirm_password')
#                                         ])
#     confirm_password = PasswordField('Confirm Password')
#     submit = SubmitField('Register')
#
#     def validate_email(self, field):
#         if Voters.query.filter_by(email=field.data).first():
#             raise ValidationError('Email is already in use.')
#
#     def validate_username(self, field):
#         if Voters.query.filter_by(username=field.data).first():
#             raise ValidationError('Username is already in use.')

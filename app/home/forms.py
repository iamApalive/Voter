from wtforms import BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from ..models import Vote

class VoteForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    checkbox = BooleanField(Vote, validators=[DataRequired(), ])
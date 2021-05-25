from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Universe


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class UniverseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate_title(self, title):
        universe = Universe.query.filter_by(title=title.data).first()
        if universe is not None:
            raise ValidationError('Universe already exists.')

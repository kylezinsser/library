from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from app.models import Actor, Art, Author, Book, Character, Series, Universe


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class ActorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', filters = [lambda x: x or None])
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', filters = [lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class ArtForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', filters = [lambda x: x or None])
    source = StringField('Source', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', filters = [lambda x: x or None])
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', filters = [lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    series_number = IntegerField('Series Number', validators=[Optional()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class CharacterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    suffix = StringField('Suffix', filters = [lambda x: x or None])
    description = TextAreaField('Description', filters = [lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class SeriesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class UniverseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

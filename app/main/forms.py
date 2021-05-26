from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import ValidationError, Required, DataRequired, Email, EqualTo, Optional
from app.models import Actor, Art, Author, Book, Character, Series, Universe
from app import db


def author_choices():      
    return db.session.query(Author).order_by('last_name', 'first_name')

def book_choices():      
    return db.session.query(Book).order_by('title')

def character_choices():      
    return db.session.query(Character).order_by('last_name', 'first_name')

def series_choices():      
    return db.session.query(Series).order_by('title')

def universe_choices():      
    return db.session.query(Universe).order_by('title')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class ActorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', filters=[lambda x: x or None])
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', filters=[lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class ArtForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', filters=[lambda x: x or None])
    source = StringField('Source', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', filters=[lambda x: x or None])
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', filters=[lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class BookForm(FlaskForm):
    universe = QuerySelectField('Universe', query_factory=universe_choices, get_label='title', allow_blank=True)
    series = QuerySelectField('Series', query_factory=series_choices, get_label='title', allow_blank=True)
    author = QuerySelectField('Author', query_factory=author_choices, get_label='full_name', allow_blank=True)
    coauthor = QuerySelectField('Co-Author', query_factory=author_choices, get_label='full_name', allow_blank=True)
    title = StringField('Title', validators=[DataRequired()])
    series_number = IntegerField('Series Number', validators=[Optional()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class CharacterForm(FlaskForm):
    universe = QuerySelectField('Universe', query_factory=universe_choices, get_label='title', allow_blank=True)
    series = QuerySelectField('Series', validators=[DataRequired()], query_factory=series_choices, get_label='title', allow_blank=True)
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    suffix = StringField('Suffix', filters=[lambda x: x or None])
    parent = QuerySelectField('Parent', query_factory=character_choices, get_label='full_name', allow_blank=True)
    description = TextAreaField('Description', filters=[lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class SeriesForm(FlaskForm):
    universe = QuerySelectField('Universe', query_factory=universe_choices, get_label='title', allow_blank=True)
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class UniverseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

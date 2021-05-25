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

    def validate(self):
        if not super(ActorForm, self).validate():
            return False
        
        actor = Actor.query.filter_by(first_name=self.first_name.data, middle_name=self.middle_name.data, 
                last_name=self.last_name.data, suffix=self.suffix.data).first()
        if actor is not None:
            msg = 'Duplicate actor already exists'
            self.first_name.errors.append(msg)
            self.last_name.errors.append(msg)
            return False
        return True


class ArtForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', filters = [lambda x: x or None])
    source = StringField('Source', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate(self):
        if not super(ArtForm, self).validate():
            return False
        
        art = Art.query.filter_by(title=self.title.data, source=self.source.data).first()
        if art is not None:
            msg = 'Duplicate art already exists'
            self.title.errors.append(msg)
            self.source.errors.append(msg)
            return False
        return True


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', filters = [lambda x: x or None])
    last_name = StringField('Last Name', validators=[DataRequired()])
    suffix = StringField('Suffix', filters = [lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate(self):
        if not super(AuthorForm, self).validate():
            return False
        
        author = Author.query.filter_by(first_name=self.first_name.data, middle_name=self.middle_name.data, 
                last_name=self.last_name.data, suffix=self.suffix.data).first()
        if author is not None:
            msg = 'Duplicate author already exists'
            self.first_name.errors.append(msg)
            self.last_name.errors.append(msg)
            return False
        return True


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    series_index = IntegerField('Series Index', validators=[Optional()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if book is not None:
            raise ValidationError('Book title already exists.')


class CharacterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', filters = [lambda x: x or None])
    suffix = StringField('Suffix', filters = [lambda x: x or None])
    description = TextAreaField('Description', filters = [lambda x: x or None])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate(self):
        if not super(CharacterForm, self).validate():
            return False
        
        character = Character.query.filter_by(first_name=self.first_name.data, last_name=self.last_name.data, 
                suffix=self.suffix.data).first()
        if character is not None:
            msg = 'Duplicate character already exists'
            self.first_name.errors.append(msg)
            self.last_name.errors.append(msg)
            return False
        return True


class SeriesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate_title(self, title):
        series = Series.query.filter_by(title=title.data).first()
        if series is not None:
            raise ValidationError('Series already exists.')


class UniverseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

    def validate_title(self, title):
        universe = Universe.query.filter_by(title=title.data).first()
        if universe is not None:
            raise ValidationError('Universe already exists.')

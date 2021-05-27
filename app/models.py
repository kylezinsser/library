from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.ext.hybrid import hybrid_property
from app import db, login

class BaseModel(db.Model):
    __abstract__ = True

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
            if isinstance(prop, ColumnProperty)]
    
# User model for logins

class User(UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, index=True, unique=True)
    email = db.Column(db.Text, index=True, unique=True)
    password_hash = db.Column(db.Text)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Tag association tables

actor_tags = db.Table('actor_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

art_tags = db.Table('art_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('art_id', db.Integer, db.ForeignKey('art.id'))
)

book_tags = db.Table('book_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

character_tags = db.Table('character_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
)

series_tags = db.Table('series_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('series_id', db.Integer, db.ForeignKey('series.id'))
)

universe_tags = db.Table('universe_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('universe_id', db.Integer, db.ForeignKey('universe.id'))
)


# Reference association tables

actor_refs = db.Table('actor_refs',
    db.Column('reference_id', db.Integer, db.ForeignKey('reference.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

art_refs = db.Table('art_refs',
    db.Column('reference_id', db.Integer, db.ForeignKey('reference.id')),
    db.Column('art_id', db.Integer, db.ForeignKey('art.id'))
)

character_refs = db.Table('character_refs',
    db.Column('reference_id', db.Integer, db.ForeignKey('reference.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
)


# Apperance association table

appearances = db.Table('appearances',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
)


# Association parent classes/functions

class TagBase(object):
    def add_tag(self, tag):
        if not self.is_tagged(tag):
            self.tags.append(tag)

    def remove_tag(self, tag):
        if self.is_tagged(tag):
            self.tags.remove(tag)

    def is_tagged(self, tag, association):
        return self.tags.filter(
            association.c.tag_id == tag.id).count() > 0


class RefBase(object):
    def add_ref(self, ref):
        if not self.is_referenced(ref):
            self.refs.append(ref)

    def remove_ref(self, ref):
        if self.is_referenced(ref):
            self.refs.remove(ref)

    def is_referenced(self, ref, association):
        return self.refs.filter(
            association.c.reference_id == ref.id).count() > 0


# Association models

class Tag(BaseModel):
    __table_args__ = (db.UniqueConstraint('name', 'tag_type_id'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    tag_type_id = db.Column(db.Integer, db.ForeignKey('tag_type.id'))

    def __repr__(self):
        return '{}'.format(self.name)


class TagType(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)


class Reference(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    private = db.Column(db.Boolean, default=False)


# Main object models

class Actor(BaseModel, TagBase, RefBase):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('first_name', 'last_name'),)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False, default='')
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text, nullable=False, default='')
    suffix = db.Column(db.Text)

    # Table associations
    tags = db.relationship('Tag', secondary=actor_tags, lazy='dynamic',
        backref=db.backref('actors', lazy=True))
    refs = db.relationship('Reference', secondary=actor_refs, lazy='dynamic',
        backref=db.backref('actors', lazy=True))

    # Property for select field labels
    @hybrid_property
    def full_name(self):
        first = self.first_name + ' ' + self.middle_name if self.middle_name else self.first_name
        last = self.last_name + ' ' + self.suffix if self.suffix else self.last_name
        return first + ' ' + last

    # Instance functions
    # TODO: middle_name printing None for nulls
    def __repr__(self):
        return '<Actor: {} {} {}; Tags:{};>'.format(self.first_name, self.middle_name, self.last_name, self.tags.all() or "n/a")

    def is_tagged(self, tag):
        return super().is_tagged(tag, actor_tags)

    def is_referenced(self, ref):
        return super().is_referenced(ref, actor_refs)


class Art(BaseModel, TagBase, RefBase):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('title', 'source'),)
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    source = db.Column(db.Text)

    # Table associations
    tags = db.relationship('Tag', secondary=art_tags, lazy='dynamic',
        backref=db.backref('art', lazy=True))
    refs = db.relationship('Reference', secondary=art_refs, lazy='dynamic',
        backref=db.backref('art', lazy=True))

    # Instance functions
    def __repr__(self):
        return '<Art: {} by {}>'.format(self.title, self.artist)

    def is_tagged(self, tag):
        return super().is_tagged(tag, art_tags)

    def is_referenced(self, ref):
        return super().is_referenced(ref, art_refs)


class Author(BaseModel):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('first_name', 'last_name'),)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False, default='')
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text, nullable=False, default='')
    suffix = db.Column(db.Text)

    # Property for select field labels
    @hybrid_property
    def full_name(self):
        first = self.first_name + ' ' + self.middle_name if self.middle_name else self.first_name
        last = self.last_name + ' ' + self.suffix if self.suffix else self.last_name
        return first + ' ' + last

    # Instance functions
    def __repr__(self):
        return '{}'.format(self.full_name)


class Book(BaseModel, TagBase):
    # Table definitions
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    coauthor_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.Text, unique=True)
    series_number = db.Column(db.Integer)

    # Table associations
    tags = db.relationship('Tag', secondary=book_tags, lazy='dynamic',
        backref=db.backref('books', lazy=True))
    characters = db.relationship('Character', secondary=appearances, lazy='dynamic',
        back_populates='books')
    universe = db.relationship('Universe', foreign_keys=universe_id, backref='books')
    series = db.relationship('Series', foreign_keys=series_id, backref='books')
    author = db.relationship('Author', foreign_keys=author_id, backref='books')
    coauthor = db.relationship('Author', foreign_keys=coauthor_id, backref='coauthored')

    # Instance functions
    def __repr__(self):
        return '{}'.format(self.title)

    def is_tagged(self, tag):
        return super().is_tagged(tag, book_tags)

    def add_character_appearance(self, character):
        if not self.has_character_appearance(character):
            self.characters.append(character)

    def remove_character_appearance(self, character):
        if self.has_character_appearance(character):
            self.characters.remove(character)

    def has_character_appearance(self, character):
        return self.characters.filter(
            appearances.c.character_id == character.id).count() > 0


class Character(BaseModel, TagBase, RefBase):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('series_id', 'first_name', 'last_name'),)
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    first_name = db.Column(db.Text, nullable=False, default='')
    last_name = db.Column(db.Text, nullable=False, default='')
    suffix = db.Column(db.Text)
    description = db.Column(db.Text)

    # Table associations
    tags = db.relationship('Tag', secondary=character_tags, lazy='dynamic',
        backref=db.backref('characters', lazy=True))
    refs = db.relationship('Reference', secondary=character_refs, lazy='dynamic',
        backref=db.backref('characters', lazy=True))
    books = db.relationship('Book', secondary=appearances, lazy='dynamic',
        back_populates='characters')
    universe = db.relationship('Universe', foreign_keys=universe_id, backref='characters')
    series = db.relationship('Series', foreign_keys=series_id, backref='characters')
    aliases = db.relationship('Character', backref=db.backref('parent', remote_side=[id]))

    # Property for select field labels
    @hybrid_property
    def full_name(self):
        last = self.last_name + ' ' + self.suffix if self.suffix else self.last_name
        return self.first_name + ' ' + last

    # Instance functions
    def __repr__(self):
        return '{}'.format(self.full_name)

    def is_tagged(self, tag):
        return super().is_tagged(tag, character_tags)

    def is_referenced(self, ref):
        return super().is_referenced(ref, character_refs)

    def add_book_appearance(self, book):
        if not self.has_book_appearance(book):
            self.books.append(book)

    def remove_book_appearance(self, book):
        if self.has_book_appearance(book):
            self.books.remove(book)

    def has_book_appearance(self, book):
        return self.books.filter(
            appearances.c.book_id == book.id).count() > 0


class Series(BaseModel, TagBase):
    # Table definitions
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    title = db.Column(db.Text, unique=True)

    # Table associations
    tags = db.relationship('Tag', secondary=series_tags, lazy='dynamic',
        backref=db.backref('series', lazy=True))
    universe = db.relationship('Universe', foreign_keys=universe_id, backref='series')

    # Instance functions
    def __repr__(self):
        return '{}'.format(self.title)

    def is_tagged(self, tag):
        return super().is_tagged(tag, series_tags)


class Universe(BaseModel, TagBase):
    # Table definitions
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)

    # Table associations
    tags = db.relationship('Tag', secondary=universe_tags, lazy='dynamic',
        backref=db.backref('universes', lazy=True))

    # Instance functions
    def __repr__(self):
        return '{}'.format(self.title)

    def is_tagged(self, tag):
        return super().is_tagged(tag, universe_tags)

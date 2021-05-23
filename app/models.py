from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


# User model for logins

class User(UserMixin, db.Model):
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

class Tag(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'tag_type_id'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    tag_type_id = db.Column(db.Integer, db.ForeignKey('tag_type.id'))

    def __repr__(self):
        return '{}'.format(self.name)


class TagType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)


class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    private = db.Column(db.Boolean, default=False)


# Main object models

class Actor(db.Model, TagBase, RefBase):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('first_name', 'middle_name', 'last_name', 'suffix'),)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    suffix = db.Column(db.Text)

    # Table associations
    tags = db.relationship('Tag', secondary=actor_tags, lazy='dynamic',
        backref=db.backref('actors', lazy=True))
    refs = db.relationship('Reference', secondary=actor_refs, lazy='dynamic',
        backref=db.backref('actors', lazy=True))

    # Instance functions
    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    # TODO: middle_name printing None for nulls
    def __repr__(self):
        return '<Actor: {} {} {}; Tags:{};>'.format(self.first_name, self.middle_name, self.last_name, self.tags.all() or "n/a")

    def is_tagged(self, tag):
        return super().is_tagged(tag, actor_tags)

    def is_referenced(self, ref):
        return super().is_referenced(ref, actor_refs)


class Art(db.Model, TagBase, RefBase):
    # Table definitions
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
    def __init__(self, artist, title, source):
        self.artist = artist
        self.title = title
        self.source = source

    def __repr__(self):
        return '<Art: {} by {}; Tags:{};>'.format(self.title, self.artist, self.tags.all() or "n/a")

    def is_tagged(self, tag):
        return super().is_tagged(tag, art_tags)

    def is_referenced(self, ref):
        return super().is_referenced(ref, art_refs)


class Author(db.Model):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('first_name', 'middle_name', 'last_name', 'suffix'),)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    suffix = db.Column(db.Text)

    # Instance functions
    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def __repr__(self):
        return '<Author: {} {} {};>'.format(self.first_name, self.middle_name, self.last_name)


class Book(db.Model, TagBase):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('universe_id', 'series_id', 'title'),)
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    coauthor_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.Text)
    series_index = db.Column(db.Integer)

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
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Book: {} by author_id {}; Tags:{};>'.format(self.title, self.author_id, self.tags.all() or "n/a")

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


class Character(db.Model, TagBase, RefBase):
    # Table definitions
    __table_args__ = (db.UniqueConstraint('series_id', 'first_name', 'last_name', 'suffix', 'parent_id'),)
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
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

    # Instance functions
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<Character: {} {}; Tags:{};>'.format(self.first_name, self.last_name, self.tags.all() or "n/a")

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


class Series(db.Model, TagBase):
    # Table definitions
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    title = db.Column(db.Text, unique=True)

    # Table associations
    tags = db.relationship('Tag', secondary=series_tags, lazy='dynamic',
        backref=db.backref('series', lazy=True))
    universe = db.relationship('Universe', foreign_keys=universe_id, backref='series')

    # Instance functions
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Series: {}; Tags:{};>'.format(self.title, self.tags.all() or "n/a")

    def is_tagged(self, tag):
        return super().is_tagged(tag, series_tags)


class Universe(db.Model, TagBase):
    # Table definitions
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)

    # Table associations
    tags = db.relationship('Tag', secondary=universe_tags, lazy='dynamic',
        backref=db.backref('universes', lazy=True))

    # Instance functions
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Universe: {}; Tags: {};>'.format(self.title, self.tags.all() or "n/a")

    def is_tagged(self, tag):
        return super().is_tagged(tag, universe_tags)

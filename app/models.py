from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


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


class Universe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    title = db.Column(db.Text)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    coauthor_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.Text)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    description = db.Column(db.Text)


class CharacterAlias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    alias = db.Column(db.Text)


class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    # Is this relationship too obtuse? Could cover instances where a character that "belongs" to one 
    # series appears in another under a different name e.g. Taelien/Keras, Hoid/Wit, etc
    alias_id = db.Column(db.Integer, db.ForeignKey('alias.id'))


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    source = db.Column(db.Text)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    tag_type_id = db.Column(db.Integer, db.ForeignKey('tag_type.id'), default=0)


class TagType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class ActorTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class ArtTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class BookTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class SeriesTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class UniverseTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universe.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class CharacterTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text)
    private = db.Column(db.Boolean, default=False)


class ActorRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))


class ArtRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))
    

class CharacterRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))

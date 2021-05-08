from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class CharacterAlias(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


class ActorTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))


class ArtTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))


class BookTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


class CharacterTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))


class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(1024))


class ActorRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))
    

# actor refers to a specific person that can be distinct from the reference
# e.g. young actor and older actor may have particular images that lend to different types of characters
# aren't the art refs and the art itself indistinguishable though? AKA do we need both tables?
# What does one have that another doesn't? Art table could have author, tags, ??
class ArtRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))
    

class CharacterRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))

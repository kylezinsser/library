from app import create_app, db
from app.models import User, Actor, Tag, Book, Character, Author, Universe


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Actor': Actor, 'Tag': Tag, 'Book': Book, 'Character': Character, 
            'Author': Author, 'Universe': Universe}
from app import create_app, db
from app.models import User, Actor, Tag, Book, Author, Universe


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Actor': Actor, 'Tag': Tag, 'Book': Book, 'Author': Author, 'Universe': Universe}
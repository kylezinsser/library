from flask import current_app, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import db, s3
from app.main.forms import EmptyForm, ActorForm, ArtForm, AuthorForm, BookForm, CharacterForm, SeriesForm, UniverseForm, UploadForm
from app.models import User, Actor, Art, Author, Book, Character, Series, Universe
from app.main import bp
from sqlalchemy import exc
import os


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@bp.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/search')
def search():
    return render_template('search.html')


@bp.route('/explore')
def explore():
    return render_template('explore.html')


@bp.route('/submit')
def submit():
    return render_template('submit.html')


# Actor Endpoints

@bp.route('/actors/add', methods=['GET', 'POST'])
def add_actor():
    return add_resource(Actor, ActorForm, 'resource.html', url_for('main.submit'), url_for('main.get_actors'))

@bp.route('/actors/<int:id>/edit', methods=['GET', 'POST'])
def edit_actor(id):
    return edit_resource(Actor, ActorForm, id, 'resource.html', url_for('main.get_actors'), url_for('main.get_actors'))

@bp.route('/actors')
def get_actors():
    columns = ['first_name', 'middle_name', 'last_name', 'suffix']
    return get_resources(Actor, 'resource.html', url_for('main.explore'), 'main.get_actor', 'main.edit_actor', columns)

@bp.route('/actors/<int:id>')
def get_actor(id):
    columns = ['first_name', 'middle_name', 'last_name', 'suffix']
    return get_resource(Actor, id, 'resource.html', url_for('main.get_actors'), 'main.get_actor', 'main.edit_actor', columns)

@bp.route('/actors/<int:id>', methods=['DELETE'])
def delete_actor(id):
    return delete_resource(Actor, id)


# Art Endpoints

@bp.route('/art/add', methods=['GET', 'POST'])
def add_art():
    return add_resource(Art, ArtForm, 'resource.html', url_for('main.submit'), url_for('main.get_art'))

@bp.route('/art/<int:id>/edit', methods=['GET', 'POST'])
def edit_art(id):
    return edit_resource(Art, ArtForm, id, 'resource.html', url_for('main.get_art'), url_for('main.get_art'))

@bp.route('/art')
def get_art():
    columns = ['artist', 'title', 'description', 'source']
    return get_resources(Art, 'resource.html', url_for('main.explore'), 'main.get_art_id', 'main.edit_art', columns)

@bp.route('/art/<int:id>')
def get_art_id(id):
    columns = ['artist', 'title', 'description', 'source']
    return get_resource(Art, id, 'resource.html', url_for('main.get_art'), 'main.get_art_id', 'main.edit_art', columns)

@bp.route('/art/<int:id>', methods=['DELETE'])
def delete_art(id):
    return delete_resource(Art, id)


# Author Endpoints

@bp.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    return add_resource(Author, AuthorForm, 'resource.html', url_for('main.submit'), url_for('main.get_authors'))

@bp.route('/authors/<int:id>/edit', methods=['GET', 'POST'])
def edit_author(id):
    return edit_resource(Author, AuthorForm, id, 'resource.html', url_for('main.get_authors'), url_for('main.get_authors'))

@bp.route('/authors')
def get_authors():
    columns = ['first_name', 'middle_name', 'last_name', 'suffix']
    return get_resources(Author, 'resource.html', url_for('main.explore'), 'main.get_author', 'main.edit_author', columns)

@bp.route('/authors/<int:id>')
def get_author(id):
    columns = ['first_name', 'middle_name', 'last_name', 'suffix']
    return get_resource(Author, id, 'resource.html', url_for('main.get_authors'), 'main.get_author', 'main.edit_author', columns)

@bp.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    return delete_resource(Author, id)


# Book Endpoints

@bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    return add_resource(Book, BookForm, 'resource.html', url_for('main.submit'), url_for('main.get_books'))

@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    return edit_resource(Book, BookForm, id, 'resource.html', url_for('main.get_books'), url_for('main.get_books'))

@bp.route('/books')
def get_books():
    columns = ['universe', 'series', 'author', 'title', 'series_number']
    return get_resources(Book, 'resource.html', url_for('main.explore'), 'main.get_book', 'main.edit_book', columns)

@bp.route('/books/<int:id>')
def get_book(id):
    columns = ['universe', 'series', 'author', 'title', 'series_number']
    return get_resource(Book, id, 'resource.html', url_for('main.get_books'), 'main.get_book', 'main.edit_book', columns)

@bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    return delete_resource(Book, id)


# Character Endpoints

@bp.route('/characters/add', methods=['GET', 'POST'])
def add_character():
    return add_resource(Character, CharacterForm, 'resource.html', url_for('main.submit'), url_for('main.get_characters'))

@bp.route('/characters/<int:id>/edit', methods=['GET', 'POST'])
def edit_character(id):
    return edit_resource(Character, CharacterForm, id, 'resource.html', url_for('main.get_characters'), url_for('main.get_characters'))

@bp.route('/characters')
def get_characters():
    columns = ['universe', 'series', 'first_name', 'last_name', 'suffix', 'description']
    return get_resources(Character, 'resource.html', url_for('main.explore'), 'main.get_character', 'main.edit_character', columns)

@bp.route('/characters/<int:id>')
def get_character(id):
    columns = ['universe', 'series', 'first_name', 'last_name', 'suffix', 'description']
    return get_resource(Character, id, 'resource.html', url_for('main.get_characters'), 'main.get_character', 'main.edit_character', columns)

@bp.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    return delete_resource(Character, id)


# Series Endpoints

@bp.route('/series/add', methods=['GET', 'POST'])
def add_series():
    return add_resource(Series, SeriesForm, 'resource.html', url_for('main.submit'), url_for('main.get_series'))

@bp.route('/series/<int:id>/edit', methods=['GET', 'POST'])
def edit_series(id):
    return edit_resource(Series, SeriesForm, id, 'resource.html', url_for('main.get_series'), url_for('main.get_series'))

@bp.route('/series')
def get_series():
    columns = ['universe', 'title']
    return get_resources(Series, 'resource.html', url_for('main.explore'), 'main.get_series_id', 'main.edit_series', columns)

@bp.route('/series/<int:id>')
def get_series_id(id):
    columns = ['universe', 'title']
    return get_resource(Series, id, 'resource.html', url_for('main.get_series'), 'main.get_series_id', 'main.edit_series', columns)

@bp.route('/series/<int:id>', methods=['DELETE'])
def delete_series(id):
    return delete_resource(Series, id)


# Universe Endpoints

@bp.route('/universes/add', methods=['GET', 'POST'])
def add_universe():
    return add_resource(Universe, UniverseForm, 'resource.html', url_for('main.submit'), url_for('main.get_universes'))

@bp.route('/universes/<int:id>/edit', methods=['GET', 'POST'])
def edit_universe(id):
    return edit_resource(Universe, UniverseForm, id, 'resource.html', url_for('main.get_universes'), url_for('main.get_universes'))

@bp.route('/universes')
def get_universes():
    columns = ['title']
    return get_resources(Universe, 'resource.html', url_for('main.explore'), 'main.get_universe', 'main.edit_universe', columns)

@bp.route('/universes/<int:id>')
def get_universe(id):
    columns = ['title']
    return get_resource(Universe, id, 'resource.html', url_for('main.get_universes'), 'main.get_universe', 'main.edit_universe', columns)

@bp.route('/universes/<int:id>', methods=['DELETE'])
def delete_universe(id):
    return delete_resource(Universe, id)


# CRUD functions for basic resource management

def add_resource(ResourceClass, FormClass, default_template, redirect_url, back_url):
    form = FormClass()
    if form.validate_on_submit():
        resource = ResourceClass()
        form.populate_obj(resource)
        
        try:
            db.session.add(resource)
            db.session.commit()
            flash('Congratulations, you added a {}!'.format(ResourceClass.__name__))
        except exc.IntegrityError:
            db.session.rollback()
            flash('Duplicate {} entry detected'.format(ResourceClass.__name__), 'error')
            return render_template('errors/500.html'), 500
        except:
            db.session.rollback()
            flash('Unknown error occured', 'error')
            return render_template('errors/500.html'), 500

        return redirect(redirect_url)

    return render_template(default_template, title='Add to {} Collection'.format(ResourceClass.__name__), form=form, back_url=back_url)

def edit_resource(ResourceClass, FormClass, id, default_template, redirect_url, back_url):
    resource = ResourceClass.query.get(id)
    if resource:
        form = FormClass(obj=resource)
        if form.validate_on_submit():
            try:
                form.populate_obj(resource)
                db.session.commit()
                flash('{} record update success'.format(ResourceClass.__name__))
            except exc.IntegrityError:
                db.session.rollback()
                flash('Duplicate {} entry detected'.format(ResourceClass.__name__), 'error')
                return render_template('errors/500.html'), 500
            except:
                db.session.rollback()
                flash('Unknown error occured', 'error')
                return render_template('errors/500.html'), 500

            return redirect(redirect_url)

    return render_template(default_template, title='Edit Resource', form=form, back_url=back_url)

def get_resources(ResourceClass, default_template, back_url, get_uri, edit_uri, columns):
    resources = ResourceClass.query.all()
    return render_template(default_template, results=resources, back_url=back_url, get_uri=get_uri, edit_uri=edit_uri, columns=columns)

def get_resource(ResourceClass, id, default_template, back_url, get_uri, edit_uri, columns):
    resource = ResourceClass.query.get(id)

    if resource:
        return render_template(default_template, results=[resource], back_url=back_url, get_uri=get_uri, edit_uri=edit_uri, columns=columns)
    else:        
        return render_template('errors/404.html'), 404
    

def delete_resource(ResourceClass, id):
    try:
        result = ResourceClass.query.filter_by(id=id).delete()
        db.session.commit()

        if result:
            flash('Successfully deleted {} record'.format(ResourceClass.__name__))
            return jsonify(success=True)
        else:
            flash('Error deleting {} id: {}'.format(ResourceClass.__name__, id), 'error')
            return jsonify(success=False)
    except:
        db.session.rollback()
        flash('Error deleting {} id: {}'.format(ResourceClass.__name__, id), 'error')
        return jsonify(success=False)


# CRUD functions for S3

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        print("ATTEMPTING FILE UPLOAD")
        output = send_to_s3(form.file.data)
        flash(output)
        print("ATTEMPTING FILE DELETE")
        deleteput = delete_from_s3('Reyna.png')
        print(deleteput)
        return redirect(url_for('main.upload_file'))

    return render_template('upload.html', form=form)

def send_to_s3(file):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            current_app.config["S3_BUCKET"],
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(current_app.config["S3_LOCATION"], file.filename)

def delete_from_s3(key):
    try:
        result = s3.delete_object(Bucket=current_app.config["S3_BUCKET"], Key=key)
        print(result)
        return result
    except Exception as e:
        print("Something Happened: ", e)
        return e


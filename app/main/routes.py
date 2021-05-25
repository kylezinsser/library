from flask import current_app, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.main.forms import EmptyForm, UniverseForm
from app.models import User, Universe
from app.main import bp
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


# Universe Endpoints

@bp.route('/universes/add', methods=['GET', 'POST'])
def add_universe():
    return add_resource(Universe, UniverseForm, 'resource.html', url_for('main.submit'), url_for('main.get_universes'))

@bp.route('/universes/<int:id>/edit', methods=['GET', 'POST'])
def edit_universe(id):
    return edit_resource(Universe, UniverseForm, id, 'resource.html', url_for('main.get_universes'), url_for('main.get_universes'))

@bp.route('/universes')
def get_universes():
    return get_resources(Universe, 'resource.html', url_for('main.explore'), 'main.get_universe', 'main.edit_universe')

@bp.route('/universes/<int:id>')
def get_universe(id):
    return get_resource(Universe, id, 'resource.html', url_for('main.get_universes'), 'main.get_universe', 'main.edit_universe')

@bp.route('/universes/<int:id>', methods=['DELETE'])
def delete_universe(id):
    return delete_resource(Universe, id)


# CRUD functions for basic resource management

def add_resource(ResourceClass, FormClass, default_template, redirect_url, back_url):
    form = FormClass()
    if form.validate_on_submit():
        resource = ResourceClass()
        form.populate_obj(resource)
        
        db.session.add(resource)
        db.session.commit()

        flash('Congratulations, you added a {}!'.format(ResourceClass.__name__))
        return redirect(redirect_url)

    return render_template(default_template, title='Add to Collection', form=form, back_url=back_url)

def edit_resource(ResourceClass, FormClass, id, default_template, redirect_url, back_url):
    resource = ResourceClass.query.get(id)
    if resource:
        form = FormClass(obj=resource)
        if form.validate_on_submit():
            form.populate_obj(resource)
            db.session.commit()
            flash('{} record update success'.format(ResourceClass.__name__))
            return redirect(redirect_url)

    return render_template(default_template, title='Edit Resource', form=form, back_url=back_url)

def get_resources(ResourceClass, default_template, back_url, get_uri, edit_uri):
    resources = ResourceClass.query.all()

    return render_template(default_template, results=resources, back_url=back_url, get_uri=get_uri, edit_uri=edit_uri)

def get_resource(ResourceClass, id, default_template, back_url, get_uri, edit_uri):
    resource = ResourceClass.query.get(id)

    return render_template(default_template, results=[resource], back_url=back_url, get_uri=get_uri, edit_uri=edit_uri)

def delete_resource(ResourceClass, id):
    result = ResourceClass.query.filter_by(id=id).delete()
    db.session.commit()

    if result:
        flash('Successfully deleted {} record'.format(ResourceClass.__name__))
        return jsonify(success=True)
    else:
        flash('Error deleting {} id: {}'.format(ResourceClass.__name__, id))
        return jsonify(success=False)

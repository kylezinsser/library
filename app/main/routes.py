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

@bp.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)


@bp.route('/search')
def search():
    return render_template('search.html')


@bp.route('/explore')
def explore():
    return render_template('explore.html')


@bp.route('/submit')
def submit():
    return render_template('submit.html')


@bp.route('/universes/add', methods=['GET', 'POST'])
def add_universe():
    form = UniverseForm()
    if form.validate_on_submit():
        universe = Universe(title=form.title.data)
        
        db.session.add(universe)
        db.session.commit()

        flash('Congratulations, you added a universe!')
        return redirect(url_for('main.submit'))

    return render_template('universes.html', title='Add to Collection', form=form)

@bp.route('/universes/<int:id>/edit', methods=['GET', 'POST'])
def edit_universe(id):
    universe = Universe.query.get(id)
    if universe:
        form = UniverseForm(obj=universe)
        if form.delete.data:
            return redirect(url_for('main.delete_universe', id=id))
        if form.validate_on_submit():
            universe.title = form.title.data
            db.session.commit()
            flash('Edit successful')
            return redirect(url_for('main.get_universes'))

    return render_template('universes.html', title='Edit Resource', form=form)

@bp.route('/universes')
def get_universes():
    universes = Universe.query.all()

    return render_template('universes.html', results=universes)

@bp.route('/universes/<int:id>')
def get_universe(id):
    universe = Universe.query.get(id)

    return render_template('universes.html', results=[universe])

@bp.route('/universes/<int:id>', methods=['DELETE'])
def delete_universe(id):
    result = Universe.query.filter_by(id=id).delete()
    db.session.commit()

    if result:
        flash('Deletion successful')
        return jsonify(success=True)
    else:
        flash('Error deleting universe id: ' + id)
        return jsonify(success=False)

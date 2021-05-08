from flask import current_app, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.main.forms import EmptyForm
from app.models import User
from app.main import bp


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


@bp.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

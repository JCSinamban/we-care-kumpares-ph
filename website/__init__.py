from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from logging import exception
import mimetypes
from xmlrpc.client import boolean

from logging import exception
import mimetypes
from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import uuid as uuid
from os.path import join, dirname, realpath

db = SQLAlchemy()
#DB_NAME = "feedback.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfghjkl'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
#    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
#    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#    UPLOAD_FOLDER = 'static/uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Admin, Products, Services

    from . import models

    with app.app_context():
        db.create_all()  

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':

            fullname = request.form.get('fullname')
            username = request.form.get('username')
            email = request.form.get('email')
            contnum = request.form.get('contnum')
            password = request.form.get('password')
            confpass = request.form.get('confpass')
            profile_pic = request.files['profile_pic']
    #        img = request.files['img']

            user = Admin.query.filter_by(email=email).first()
            admin = Admin.query.get(request.form.get('id'))
            filename = secure_filename(profile_pic.filename)
            mimetype = profile_pic.mimetype
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if user:
                flash('Email already exists.', category='error') 
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(fullname) < 2:
                flash('Full name must be greater than 1 characters.', category='error')
            elif password != confpass:
                flash('Passwords don\'t match', category='error')
            elif len(password) < 7:
                flash('Password must be at least 7 characters.', category='error')
    #        elif profile_pic and allowed_file(profile_pic.filename):
    #            filename = secure_filename(profile_pic.filename)
    #            profile_pic.save('UPLOADS_FOLDER', filename)   
            else:
                admin = Admin(email=email, username=username, fullname=fullname, password=generate_password_hash(password, method='sha256'), contnum=contnum, confpass=confpass, profile_pic=profile_pic.read(), filename=filename, mimetype=mimetype)
                db.session.add(admin)
                db.session.commit()
                login_user(admin, remember=True)
                #flash('Account created!', category='success')
                return redirect(url_for('auth.settings'))

        return render_template("add.html", user=current_user)

    @app.route('/display/<filename>')
    def display_image(filename):
        #print('display_image filename: ' + filename)
        return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return app

"""
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Create Database')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()
"""


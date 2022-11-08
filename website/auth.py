from logging import exception
import mimetypes
from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import uuid as uuid
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/..')

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #data = request.form
    #print(data)

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = Admin.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                #flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", boolean=True, user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
    


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
UPLOAD_FOLDER = 'static/uploads/'

@auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':

        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        contnum = request.form.get('contnum')
        password = request.form.get('password')
        confpass = request.form.get('confpass')
        img = request.files['img']

        user = Admin.query.filter_by(email=email).first()
        admin = Admin.query.get(request.form.get('id'))
        filename = secure_filename(img.filename)
        mimetype = img.mimetype

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
#        elif img and allowed_file(img.filename):
#            filename = secure_filename(img.filename)
#            img.save(os.path.join('UPLOAD_FOLDER', filename))

        else:
            new_admin = Admin(email=email, username=username, fullname=fullname, password=generate_password_hash(password, method='sha256'), contnum=contnum, confpass=confpass, img=img.read(), filename=filename, mimetype=mimetype)
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            #flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    
    all_admin = Admin.query.all()

    return render_template("settings.html", admin = all_admin, user=current_user)

@auth.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    admin = Admin.query.filter_by(id=id).first()

    if request.method == 'POST':

        admin.fullname = request.form.get('fullname')
        admin.username = request.form.get('username')
        admin.email = request.form.get('email')
        admin.contnum = request.form.get('contnum')
        admin.password = request.form.get('password')
        admin.confpass = request.form.get('confpass')

        try:
            db.session.commit()
            return redirect(url_for('auth.settings'))
        except:
            return "There was a problem"
    else:

#        img = request.files['img']
#        filename = secure_filename(img.filename)
#        mimetype = img.mimetype

#        admin = Admin(email=email, username=username, fullname=fullname, password=generate_password_hash(password, method='sha256'), contnum=contnum, confpass=confpass, img=img.read(), filename=filename, mimetype=mimetype)
#        admin = Admin(email=email, username=username, fullname=fullname, password=generate_password_hash(password, method='sha256'), contnum=contnum, confpass=confpass)
#        db.session.add(admin)
#        db.session.commit()
#        return redirect(url_for('views.home'))
 
        return render_template("updateAdmin.html", admin = admin)
 

 
@auth.route('/remove/<int:id>', methods=['GET','POST'])
def remove(id):
    admin = Admin.query.filter_by(id=id).first()
    if request.method == 'POST':
        if admin:
            db.session.delete(admin)
            db.session.commit()
            return redirect(url_for('auth.settings'))

    return render_template("deleteAdmin.html", admin = admin)

@auth.route('/insert', methods=['GET','POST'])
def insert():
    return render_template("editFeedback.html")

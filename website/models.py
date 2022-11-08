from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime 
from datetime import date

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    contnum = db.Column(db.String(15))
    confpass = db.Column(db.String(150))
#    img = db.Column(db.String(150))
    mimetype = db.Column(db.String(150))
    filename = db.Column(db.String(150))
    profile_pic = db.Column(db.String(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custname = db.Column(db.String(150))
    custcontact = db.Column(db.String(150))
    custemail = db.Column(db.String(150))
    custstatus = db.Column(db.String(150))
    branch = db.Column(db.String(150))
    prodpurchase = db.Column(db.String(150))
    fb_variety = db.Column(db.String(150))
    fb_presentation = db.Column(db.String(150))
    fb_quality = db.Column(db.String(150))
    prodcomment = db.Column(db.String(1000))
    prodtranscomment = db.Column(db.String(1000))
    prodremark = db.Column(db.String(150))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custname = db.Column(db.String(150))
    custcontact = db.Column(db.String(150))
    custemail = db.Column(db.String(150))
    custstatus = db.Column(db.String(150))
    branch = db.Column(db.String(150))
    prodpurchase = db.Column(db.String(150))
    fb_empserv = db.Column(db.String(150))
    fb_speed = db.Column(db.String(150))
    fb_clean = db.Column(db.String(150))
    servcomment = db.Column(db.String(1000))
    servtranscomment = db.Column(db.String(1000))
    servremark = db.Column(db.String(150))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Prodserv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custname = db.Column(db.String(150))
    custcontact = db.Column(db.String(150))
    custemail = db.Column(db.String(150))
    custstatus = db.Column(db.String(150))
    branch = db.Column(db.String(150))
    prodpurchase = db.Column(db.String(150))
    fb_variety = db.Column(db.String(150))
    fb_presentation = db.Column(db.String(150))
    fb_quality = db.Column(db.String(150))

    fb_empserv = db.Column(db.String(150))
    fb_speed = db.Column(db.String(150))
    fb_clean = db.Column(db.String(150))

    prodcomment = db.Column(db.String(1000))
    prodtranscomment = db.Column(db.String(1000))
    prodremark = db.Column(db.String(150))

    servcomment = db.Column(db.String(1000))
    servtranscomment = db.Column(db.String(1000))
    servremark = db.Column(db.String(150))
    date_added = db.Column(db.String)

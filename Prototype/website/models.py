from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Flag(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     data = db.Column(db.String(255))
     #date = db.Column(db.DateTime(timezone=True), default=func.now())
     #solver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(150), unique=True)
     password = db.Column(db.String(150))
     username = db.Column(db.String(150))
     #flags = db.relationship('Flag', backref=db.backref('users'))

class Solves(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     solver = db.Column(db.Integer, db.ForeignKey('user.id'))
     solved = db.Column(db.Integer, db.ForeignKey('flag.id'))
     timestamp = db.Column(db.String(150))
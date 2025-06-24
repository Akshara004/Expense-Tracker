from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    #  One-to-many relationship with Expense
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=datetime.now)
    description = db.Column(db.String(200))
    # ForeignKey to link with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

from flask_sqlalchemy import Model
from __init__ import db


class User(Model):
    __tablename__ = "user"
    ROLE_ADMIN = 0
    ROLE_USER = 1
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), index=True)
    username = db.Column(db.Unicode(20), index=True)
    password_hash = db.Column(db.Unicode(120))
    role = db.Column(db.Integer, default=ROLE_USER)
    postings = db.relationship("Posting", backref="user")


class Posting(Model):
    __tablename__ = "posting"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64), index=True)
    description = db.Column(1200)
    price = db.Column(db.Integer, default=100)
    user_id = db.ForeignKey("user.id", index=True)



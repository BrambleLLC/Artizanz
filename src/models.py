from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey
from sqlalchemy.orm import relationship


class User(Model):
    __tablename__ = "user"
    ROLE_ADMIN = 0
    ROLE_USER = 1
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64), index=True)
    username = Column(Unicode(20), index=True)
    password_hash = Column(Unicode(120))
    role = Column(Integer, default=ROLE_USER)
    postings = relationship("Posting", backref="user")


class Posting(Model):
    __tablename__ = "posting"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(64), index=True)
    description = Column(1200)
    price = Column(Integer, default=100)
    user_id = ForeignKey("user.id", index=True)



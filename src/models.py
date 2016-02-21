from mongokit import Document
from __init__ import connection
import datetime
from passlib.hash import bcrypt


@connection.register
class User(Document):
    structure = {
        "username": unicode,
        "password_hash": unicode,
        "email": unicode,
        "address1": unicode,
        "address2": unicode,
        "city": unicode,
        "state": unicode,
        "country": unicode,
        "zipcode": unicode,
        "phone_number": unicode,
        "registration_date": datetime.datetime,
        "postings": list,
        "bids": list
    }
    gridfs = {
        "files": ["profile_picture"]
    }
    required_fields = ["username", "password_hash", "email", "address1", "city", "state", "country", "zipcode",
                       "phone_number", "registration_date"]
    default_values = {"registration_date": datetime.datetime.utcnow()}

    def set_password(self, password):
        self["password_hash"] = unicode(bcrypt.encrypt(password))

    def verify_password(self, check_password):
        return bcrypt.verify(check_password, self["password_hash"])


@connection.register
class Posting(Document):
    structure = {
        "posting_id": unicode,
        "title": unicode,
        "description": unicode,
        "price_dollars": int,
        "price_cents": int,
        "start_time": datetime.datetime,
        "end_time": datetime.datetime,
        "bids": list,
        "tags": list
    }
    required_fields = ["title", "description", "price_dollars", "price_cents", "start_time", "end_time"]
    default_values = {"start_time": datetime.datetime.utcnow()}


@connection.register
class Bid(Document):
    structure = {
        "bid_id": int,
        "bid_amount_dollars": int,
        "bid_amount_cents": int,
        "user_id": unicode
    }
    required_fields = ["bid_id", "bid_amount_dollars", "bid_amount_cents", "user_id"]


@connection.register
class Tag(Document):
    structure = {
        "tag_id": unicode,
        "postings": list
    }
    required_fields = ["tag_id"]

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
        "bids": list,
        "description": unicode,
        "photo_path": unicode
    }
    required_fields = ["username", "password_hash", "email", "address1", "city", "state", "country", "zipcode",
                       "phone_number", "registration_date"]
    default_values = {"registration_date": datetime.datetime.utcnow()}

    def set_password(self, password):
        self["password_hash"] = unicode(bcrypt.encrypt(password, rounds=13))

    def verify_password(self, check_password):
        return bcrypt.verify(check_password, self["password_hash"])


@connection.register
class Artwork(Document):
    structure = {
        "vendor_name": unicode,
        "vendor_name_lower": unicode,
        "artist_name": unicode,
        "artist_name_lower": unicode,
        "title": unicode,
        "title_lower": unicode,
        "width": float,
        "height": float,
        "description": unicode,
        "bid_price": int,
        "buy_price": int,
        "start_time": datetime.datetime,
        "end_time": datetime.datetime,
        "bids": list,
        "mediums": list,
        "bought": bool,
        "photo_path": unicode
    }
    required_fields = ["vendor_name", "vendor_name_lower", "artist_name", "artist_name_lower", "title", "title_lower", "bid_price", "start_time", "end_time", "mediums"]
    default_values = {"start_time": datetime.datetime.utcnow(), "bought": False}

    def populate_lowers(self):
        self["vendor_name_lower"] = self["vendor_name"].lower()
        self["artist_name_lower"] = self["artist_name_lower"].lower()
        self["title_lower"] = self["title"].lower()


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

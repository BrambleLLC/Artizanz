from __init__ import db

thread_table = db.Table("threads",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("thread_id", db.Integer, db.ForeignKey("message_thread.id")))

tag_table = db.Table("tags",
                     db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
                     db.Column("posting_id", db.Integer, db.ForeignKey("posting.id")))


class User(db.Model):
    __tablename__ = "user"
    ROLE_ADMIN = 0
    ROLE_USER = 1
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), index=True)
    email = db.Column(db.Unicode(64), index=True)
    password_hash = db.Column(db.Unicode(120))
    address_1 = db.Column(db.Unicode(120))
    address_2 = db.Column(db.Unicode(120))
    city = db.Column(db.Unicode(30))
    state = db.Column(db.Unicode(30))
    country = db.Column(db.Unicode(30))
    zipcode = db.Column(db.Unicode(12))
    phone_number = db.Column(db.Unicode(10))
    role = db.Column(db.Integer, default=ROLE_USER)
    postings = db.relationship("Posting", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    bids = db.relationship("Bid", backref="user", lazy="dynamic", cascade="all, delete-orphan")


class Posting(db.Model):
    __tablename__ = "posting"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64), index=True)
    description = db.Column(db.UnicodeText(1600))
    price = db.Column(db.Integer, default=100)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, index=True)
    user_id = db.ForeignKey("user.id", index=True)
    bids = db.relationship("Bid", backref="posting", lazy="dynamic", cascade="all, delete-orphan")
    tags = db.relationship("Tag", secondary=tag_table, backref="postings", lazy="dynamic")


class Bid(db.Model):
    __tablename__ = "bid"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=20, scale=2))
    user_id = db.ForeignKey("user.id", index=True)
    posting_id = db.ForeignKey("posting.id", index=True)


class PrivateMessageThread(db.Model):
    __tablename__ = "message_thread"
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship("PrivateMessage", backref="thread", lazy="dynamic", cascade="all, delete-orphan")
    users = db.relationship("User", secondary=thread_table, backref="private_message_threads", lazy="dynamic")


class PrivateMessage(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)
    sent_datetime = db.Column(db.DateTime)


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

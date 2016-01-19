from src import app
from flask import session, escape
from datetime import datetime, timedelta
import hmac
from hashlib import sha256
import base64
from functools import wraps


expire_timedelta = timedelta(days=60)


def generate_session_id(username, dt):
    unix_timestamp = dt.strftime("%s")
    session_prefix = username + ":" + unix_timestamp
    session_hmac = base64.b64encode(hmac.new(app.secret_key, session_prefix, digestmod=sha256).digest())
    session_id = session_prefix + ":" + session_hmac
    return session_id


def create_session(username):
    session["username"] = escape(username)
    session["session-id"] = generate_session_id(username, datetime.utcnow())


def verify_session():
    username = session["username"]
    session_id = session["session-id"]
    tokens = session_id.split(":")
    if username != tokens[0]:
        return False
    creation_datetime = datetime.utcfromtimestamp(int(tokens[1]))
    now = datetime.utcnow()
    if now - creation_datetime > timedelta:
        return False
    return generate_session_id(username, creation_datetime) == session_id


def destroy_session():
    session.pop("username", None)
    session.pop("session-id", None)

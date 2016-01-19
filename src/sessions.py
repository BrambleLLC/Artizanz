from src import app
from flask import session, escape
from datetime import datetime, timedelta
import time
import hmac
from hashlib import sha256
import base64


expire_timedelta = timedelta(days=60)


def generate_session_id(username, dt):
    unix_timestamp = int(time.mktime(dt.timetuple()))
    session_prefix = username + ":" + str(unix_timestamp)
    session_hmac = base64.b64encode(hmac.new(app.secret_key, session_prefix, digestmod=sha256).digest())
    session_id = session_prefix + ":" + session_hmac
    return session_id


def create_session(username):
    session["username"] = escape(username)
    session["session-id"] = generate_session_id(username, datetime.utcnow())


def verify_session():
    username = session.get("username")
    session_id = session.get("session-id")
    if not username or not session_id:
        return False
    tokens = session_id.split(":")
    if username != tokens[0]:
        return False
    creation_datetime = datetime.fromtimestamp(int(tokens[1]))
    now = datetime.utcnow()
    if now - creation_datetime > expire_timedelta:
        return False
    return generate_session_id(username, creation_datetime) == session_id


def destroy_session():
    session.pop("username", None)
    session.pop("session-id", None)
    delete_session_next()


def set_session_next(next_path):
    session["next"] = next_path


def get_session_next():
    if session.get("next"):
        return session["next"]
    else:
        return "/"


def delete_session_next():
    session.pop("next", None)

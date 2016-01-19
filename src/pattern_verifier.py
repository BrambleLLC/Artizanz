import re


def matches_username(username):
    return True if re.match(r"^[a-zA-Z0-9_\.\-]{6,20}$", username) else False


def matches_password(password):
    return True if re.match(r"^[a-zA-Z0-9~!@#\$\^&\*\.,\?]$", password) else False


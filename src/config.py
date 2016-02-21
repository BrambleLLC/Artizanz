import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = 'change me when deployed'
PERMANENT_SESSION_LIFETIME = timedelta(days=120)

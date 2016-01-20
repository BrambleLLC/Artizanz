import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'mysql://arthur:bingbang@artizanz.stevex86.com/db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///webapp.db'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
SECRET_KEY = 'change me when deployed'
PERMANENT_SESSION_LIFETIME = timedelta(days=120)

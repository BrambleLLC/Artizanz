from flask import Flask
from mongokit import Connection
import config


app = Flask(__name__)
app.config.from_object(config)
connection = Connection(host="artizanz.com", port=27017)
collection = connection["artizanz"].art

from models import *
from views import *

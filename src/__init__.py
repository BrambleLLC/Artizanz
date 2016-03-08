from flask import Flask
from mongokit import Connection
import config
import os

app = Flask(__name__)
app.config.from_object(config)
connection = Connection(host="artizanz.com", port=27017)
art = connection["artizanz"].art
users = connection["artizanz"].users
bids = connection["artizanz"].bids
tags = connection["artizanz"].tags

if not os.path.exists("src/" + app.config["ARTWORK_FOLDER"]):
    os.makedirs("src/" + app.config["ARTWORK_FOLDER"])
if not os.path.exists("src/" + app.config["PROPIC_FOLDER"]):
    os.makedirs("src/" + app.config["PROPIC_FOLDER"])

from models import *
from views import *

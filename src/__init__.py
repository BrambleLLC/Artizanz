from flask import Flask
from mongokit import Connection
import config
import os
from decimal import *

getcontext().prec = 2
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


def CurrencyFilter(value):
    return str(Decimal(value) / Decimal(100))

app.jinja_env.filters["CurrencyFilter"] = CurrencyFilter()

from models import *
from views import *

from src import art
from urllib import urlopen
from PIL import Image
import datetime
from cStringIO import StringIO
import base64

for i in range(1, 31):
    artwork = art.Artwork()
    artwork["title"] = u"Test Post #{}".format(i)
    artwork["mediums"] = ["pixels"]
    artwork["width"] = float(20)
    artwork["height"] = float(20)
    artwork["bid_price_dollars"] = 100
    artwork["bid_price_cents"] = 80
    artwork["buy_price_dollars"] = 20
    artwork["buy_price_cents"] = 50
    artwork["description"] = u"Test description"
    artwork["end_time"] = datetime.datetime.now()
    artwork["photo_path"] = u"face.gif"
    artwork.save()

    print i

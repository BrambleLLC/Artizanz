from src import collection
from urllib import urlopen
from PIL import Image
import datetime
from cStringIO import StringIO
import base64

a = StringIO(urlopen("http://api.theweek.com/sites/default/files/styles/large/public/1.12_9-luckovich-creators.jpg").read())
image = Image.open(a).convert("RGB")
b = StringIO()
image.save(b, format="JPEG", quality=90)
image_data = b.getvalue()
data_url = "data:image/jpg;base64," + base64.b64encode(image_data)

for i in range(1, 31):
    artwork = collection.Artwork()
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
    artwork.save()
    artwork.fs.artwork_picture = data_url
    artwork.save()
    print i

from flask import request, render_template, redirect, url_for, session, json, send_file, send_from_directory
from src import app
from forms import SignUpForm, LoginForm, RecoveryForm, AdvancedSearchForm, SellAnArtworkForm
from functools import wraps
from sessions import verify_session, create_session, destroy_session, set_session_next, get_session_next, \
                     delete_session_next
from flask.ext.paginate import Pagination
from PIL import Image
from cStringIO import StringIO
from __init__ import users, art
import base64
import re
import datetime
from werkzeug import secure_filename
import os
import binascii
from decimal import Decimal

password_regex = "^[a-zA-Z0-9!@#\$%\^&\*\-\+,\.\?]{8,}$"
pattern = re.compile(password_regex)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if verify_session():
            return f(*args, **kwargs)
        else:
            set_session_next(request.path)
            return redirect(url_for("login"))
    return wrapper


def validate_password(password):
    return True if pattern.match(password) else False


@app.before_request
def regenerate():
    session.modified = True


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    artworks = art.Artwork.find().skip((page - 1) * 10).limit(10)
    pagination = Pagination(page=page, total=art.count(), record_name="artworks", bs_version=3)
    return render_template("index.html", artworks=artworks, pagination=pagination)


@app.route("/search")
def search():
    advanced = request.args.get("advanced")
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    if not advanced:
        query_string = request.args.get("q").lower()
        artworks = art.Artwork.find({"$or": [{"title_lower": query_string}, {"artist_name_lower": query_string}]}).skip((page - 1) * 10).limit(10)
    else:
        query_projection = []
        vendor_name = request.args.get("vendor_name")
        if vendor_name:
            query_projection.append({"vendor_name_lower": vendor_name.lower()})
        artist_name = request.args.get("artist_name")
        if artist_name:
            query_projection.append({"artist_name_lower": artist_name.lower()})
        piece_name = request.args.get("piece_name")
        if piece_name:
            query_projection.append({"title_lower": piece_name.lower()})
        medium = request.args.get("medium")
        if medium:
            mediums = map(lambda x: x.strip().lower(), medium.split(u","))
            query_projection.append({"mediums": {"$in": mediums.lower()}})
        price_low = request.args.get("price_low")
        if price_low:
            try:
                price_low_fields = price_low.split(".")
                price_low_dollars = 0 if not price_low_fields[0] else int(price_low_fields[0])
                price_low_cents = 0 if len(price_low_fields) < 2 else int(price_low_fields[1])
                price_low = price_low_dollars * 100 + price_low_cents
                query_projection.append({"$or": [{"bid_price": {"$gte": price_low}}, {"buy_price": {"$gte": price_low}}]})
            except ValueError:
                pass
        price_high = request.args.get("price_high")
        if price_high:
            try:
                price_high_fields = price_high.split(".")
                price_low_dollars = 0 if not price_high_fields[0] else int(price_high_fields[0])
                price_low_cents = 0 if len(price_high_fields) < 2 else int(price_high_fields[1])
                price_high = price_low_dollars * 100 + price_low_cents
                query_projection.append({"$or": [{"bid_price": {"$lte": price_high}}, {"buy_price": {"$lte": price_high}}]})
            except ValueError:
                pass
        width = request.args.get("width")
        if width:
            try:
                width = float(width)
                query_projection.append({"width": width})
            except ValueError:
                pass
        height = request.args.get("height")
        if height:
            try:
                height = float(height)
                query_projection.append({"height": height})
            except ValueError:
                pass
        artworks = art.Artwork.find({"$and": query_projection}).skip((page - 1) * 10).limit(10)
    pagination = Pagination(page=page, total=artworks.count(), record_name="artworks", bs_version=3)
    return render_template("search.html", artworks=artworks, pagination=pagination)


@app.route("/w/<string:wid>")
def work(wid):
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = SellAnArtworkForm()
    if form.validate_on_submit():
        artist_name = request.form.get("artist_name")
        piece_name = request.form.get("piece_name")
        medium = request.form["medium"]
        mediums = map(lambda x: x.strip().lower(), medium.split(u","))
        width = request.form["width"]
        height = request.form["height"]
        starting_bid = request.form["starting_bid"]
        buy_now = request.form.get("buy_now")
        artwork_description = request.form["artwork_description"]
        new_artwork = art.Artwork()
        new_artwork["vendor_name"] = session.get("username")
        new_artwork["vendor_name_lower"] = new_artwork["vendor_name"].lower()
        new_artwork["artist_name"] = artist_name
        new_artwork["artist_name_lower"] = artist_name.lower()
        new_artwork["title"] = u"Untitled" if not piece_name else piece_name
        new_artwork["title_lower"] = new_artwork["title"].lower()
        new_artwork["mediums"] = mediums
        new_artwork["width"] = float(width)
        new_artwork["height"] = float(height)
        starting_bid_fields = starting_bid.split(".")
        bid_price_dollars = 0 if not starting_bid_fields[0] else int(starting_bid_fields[0])
        bid_price_cents = 0 if len(starting_bid_fields) < 2 else int(starting_bid_fields[1])
        new_artwork["bid_price"] = bid_price_dollars * 100 + bid_price_cents
        buy_fields = buy_now.split(".")
        buy_price_dollars = 0 if not buy_fields[0] else int(buy_fields[0])
        buy_price_cents = 0 if len(buy_fields) < 2 else int(buy_fields[1])
        new_artwork["buy_price"] = buy_price_dollars * 100 + buy_price_cents
        new_artwork["description"] = u"None" if not artwork_description else artwork_description
        new_artwork["end_time"] = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        artwork_picture = Image.open(request.files["artwork_picture"]).convert("RGB")
        filename = binascii.hexlify(os.urandom(20)) + ".jpg"
        filepath = os.path.join("src/" + app.config["ARTWORK_FOLDER"], filename)
        with open(filepath, "w+b") as f:
            artwork_picture.save(f, format="JPEG", quality=90)
        new_artwork["photo_path"] = unicode(filename)
        new_artwork.save()
        return redirect("successful_upload")
    return render_template("upload.html", form=form)


@app.route("/advanced-search", methods=["GET", "POST"])
def advanced_search():
    form = AdvancedSearchForm()
    if form.validate_on_submit():
        return "test"
    return render_template("advanced_search.html", form=form)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    errors = False
    error_messages = set()
    if form.validate_on_submit():
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        address_1 = request.form["address_1"]
        address_2 = request.form.get("address_2")
        city = request.form["city"]
        state = request.form["state"]
        zip_code = request.form["zip"]
        country = request.form["country"]
        phone_number = request.form.get("phone_number")
        profile_picture_file = request.files.get("profile_picture")
        profile_picture_crop_options = request.form.get("profile_picture_crop_options")

        query_results = users.User.find(projection={"$or": [{"username": username}, {"email": email}, {"username": email}]})
        if query_results.count():
            for result in query_results:
                if result["username"] == username:
                    errors = True
                    error_messages.add("Username already in use")
                if result["email"] == email:
                    errors = True
                    error_messages.add("Email already in use")

        if not validate_password(password):
            errors = True
            error_messages.add("Password must be at least 8 characters and must follow some arbitrary rules")
        elif password != confirm_password:
            errors = True
            error_messages.add("Passwords do not match")

        if not errors:
            user = users.User()
            user["username"] = username
            user.set_password(password)
            user["email"] = email
            user["address1"] = address_1
            user["address2"] = address_2 if address_2 else u""
            user["city"] = city
            user["state"] = state
            user["zipcode"] = zip_code
            user["country"] = country
            user["phone_number"] = phone_number if phone_number else u""
            if profile_picture_file and profile_picture_crop_options:
                options = json.loads(profile_picture_crop_options)
                image = Image.open(profile_picture_file).convert("RGB")
                x = int(options["x"] / options["scale"])
                y = int(options["y"] / options["scale"])
                image = image.crop((x, y, int(x + 250 / options["scale"]), int(y + 250 / options["scale"])))
                image = image.resize((250, 250), Image.ANTIALIAS)
                filename = secure_filename(username + ".jpg")
                filepath = os.path.join("src/" + app.config["PROPIC_FOLDER"], filename)
                with open(filepath, "w+b") as f:
                    image.save(f, format="JPEG", quality=90)
                user["photo_path"] = unicode(filename)
            user.save()
            return redirect(url_for("login"))

    elif request.method != "GET":
        errors = True
        username = request.form.get("username")
        email = request.form.get("email")
        query_results = users.User.find(projection={"$or": [{"username": username}, {"email": email}]})
        if query_results.count():
            for result in query_results:
                if result["username"] == username:
                    error_messages.add("Username already in use")
                if result["email"] == email:
                    error_messages.add("Email already in use")
        error_messages.add("Please complete all non-optional fields")

    return render_template("sign_up.html", form=form, errors=errors, error_messages=error_messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    if verify_session():
        next_url = get_session_next()
        delete_session_next()
        return redirect(next_url)
    form = LoginForm()
    error = False
    error_message = None
    if form.validate_on_submit():
        username = request.form["username"]
        password = request.form["password"]
        user = users.User.find_one({"$or": [{"username": username}, {"email": username}]})
        if user and user.verify_password(password):
            session.permanent = form.data.get("remember_me")
            create_session(user["username"])
            next_url = get_session_next()
            delete_session_next()
            return redirect(next_url)
        else:
            error = True
            error_message = "Invalid Username or Password"
    return render_template("login.html", form=form, error=error, error_message=error_message)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    destroy_session()
    return redirect(url_for("index"))


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    return render_template("cart.html")


@app.route("/tos", methods=["GET"])
def tos():
    return render_template("tos.html")


@app.route("/password-reset", methods=["GET", "POST"])
def password_reset():
    form = RecoveryForm()
    if form.validate_on_submit():
        return "test"
    return render_template("password_reset.html", form=form)


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")


@app.route("/successful_upload", methods=["GET"])
def successful_upload():
    return render_template("successful_upload.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def default_profile():
    return redirect(url_for("user_profile", username=session["username"]))


@app.route("/edit_profile", methods=["GET"])
def edit_profile():
    return render_template("edit_profile.html")


@app.route("/profile/<string:username>")
def user_profile(username):
    user = users.User.find_one({"username": username})
    if not user:
        return "404 - User not found", 404
    return render_template("profile.html", user=user)


@app.route("/artwork", methods=["GET", "POST"])
def artwork():
    return render_template("artwork.html")


@app.route("/content/profile_pictures/<string:username>")
def profile_picture(username):
    return send_file(app.config["PROPIC_FOLDER"] + "/" + username)


@app.route("/content/artwork_pictures/<string:artwork_name>")
def artwork_picture(artwork_name):
    return send_file(app.config["ARTWORK_FOLDER"] + "/" + artwork_name)


@app.route("/pull", methods=["GET", "POST"])
def pull():
    os.system("git pull origin master")
    return ""

from flask import request, render_template, redirect, url_for, session, json
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

    artworks = art.Artwork.find()
    pagination = Pagination(page=page, total=art.count(), record_name="artwork", bs_version=3)
    return render_template("index.html", artworks=artworks, pagination=pagination)


@app.route("/w/<string:wid>")
def work(wid):
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = SellAnArtworkForm()
    if form.validate_on_submit():
        piece_name = request.form.get("piece_name")
        medium = request.form["medium"]
        width = request.form["width"]
        height = request.form["height"]
        starting_bid = request.form["starting_bid"]
        buy_now = request.form.get("buy_now")
        artwork_description = request.form["artwork_description"]
        new_artwork = art.Artwork()
        new_artwork["title"] = u"Untitled" if not piece_name else piece_name
        new_artwork["mediums"] = medium.split(",")
        new_artwork["width"] = float(width)
        new_artwork["height"] = float(height)
        starting_bid_fields = starting_bid.split(".")
        new_artwork["bid_price_dollars"] = 0 if not starting_bid_fields[0] else int(starting_bid_fields[0])
        new_artwork["bid_price_cents"] = 0 if len(starting_bid_fields) < 2 else int(starting_bid_fields[1])
        buy_fields = buy_now.split(".")
        new_artwork["buy_price_dollars"] = 0 if not buy_fields[0] else int(buy_fields[0])
        new_artwork["buy_price_dollars"] = 0 if len(buy_fields) < 2 else int(buy_fields[1])
        new_artwork["description"] = u"None" if not artwork_description else artwork_description
        new_artwork["end_time"] = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        new_artwork.save()
        s_io = StringIO()
        artwork_picture = Image.open(request.files["artwork_picture"]).convert("RGB")
        artwork_picture.save(s_io, format="JPEG", quality=90)
        image_data = s_io.getvalue()
        data_url = "data:image/jpg;base64," + base64.b64encode(image_data)
        new_artwork.fs.artwork_picture = data_url
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

        query_results = users.User.find(projection={"$or": [{"username": username}, {"email": email}]})
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
            user.save()
            if profile_picture_file and profile_picture_crop_options:
                options = json.loads(profile_picture_crop_options)
                image = Image.open(profile_picture_file).convert("RGB")
                s_io = StringIO()
                x = int(options["x"] / options["scale"])
                y = int(options["y"] / options["scale"])
                image = image.crop((x, y, int(x + 250 / options["scale"]), int(y + 250 / options["scale"])))
                image = image.resize((250, 250), Image.ANTIALIAS)
                image.save(s_io, format="JPEG", quality=90)
                im_data = s_io.getvalue()
                data_url = "data:image/jpg;base64," + base64.b64encode(im_data)
                user.fs.profile_picture = data_url
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
        user = collection.User.find_one({"$or": [{"username": username}, {"email": username}]})
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


@app.route("/profile/<string:username>")
def user_profile(username):
    user = users.User.find_one({"username": username})
    if not user:
        return "404", 404
    return render_template("profile.html", user=user)


@app.route("/artwork", methods=["GET", "POST"])
def artwork():
    return render_template("artwork.html")
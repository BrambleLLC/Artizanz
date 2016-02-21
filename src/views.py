from flask import request, render_template, redirect, url_for, session, json
from src import app
from forms import SignUpForm, LoginForm, RecoveryForm, AdvancedSearchForm
from functools import wraps
from sessions import verify_session, create_session, destroy_session, set_session_next, get_session_next, \
                     delete_session_next
from PIL import Image
from cStringIO import StringIO
from __init__ import collection
import base64

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if verify_session():
            return f(*args, **kwargs)
        else:
            set_session_next(request.path)
            return redirect(url_for("login"))
    return wrapper


@app.before_request
def regenerate():
    session.modified = True


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/w/<string:wid>")
def work(wid):
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")


@app.route("/advanced-search", methods=["GET", "POST"])
def advanced_search():
    form = AdvancedSearchForm()
    if form.validate_on_submit():
        return "test"
    return render_template("advanced_search.html", form=form)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return render_template("sign_up.html", form=form)
        address_1 = request.form["address_1"]
        address_2 = request.form.get("address_2")
        city = request.form["city"]
        state = request.form["state"]
        zip_code = request.form["zip"]
        country = request.form["country"]
        phone_number = request.form.get("phone_number")
        profile_picture_file = request.files.get("profile_picture")
        profile_picture_crop_options = request.form.get("profile_picture_crop_options")

        if collection.find(projection={"$or": [{"username": username}, {"email": email}]}):
            return "correct error condition"

        user = collection.User()
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
            image = Image.open(profile_picture_file)
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
            return """
                    <img src="{}" />
                   """.format(user.fs.profile_picture)
        else:
            return "hoober"

    return render_template("sign_up.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if verify_session():
        next_url = get_session_next()
        delete_session_next()
        return redirect(next_url)
    form = LoginForm()
    if form.validate_on_submit():
        session.permanent = form.data.get("remember_me")
        create_session(request.form["username"])
        next_url = get_session_next()
        delete_session_next()
        return redirect(next_url)
    return render_template("login.html", form=form)


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


@app.route("/profile", methods=["GET"])
@login_required
def default_profile():
    return redirect(url_for("user_profile", username=session["username"]))


@app.route("/profile/<string:username>")
def user_profile(username):
    return render_template("profile.html", username=username)

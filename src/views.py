from flask import request, render_template, redirect, url_for
from src import app
from forms import SignUpForm, LoginForm
from functools import wraps
from sessions import verify_session, create_session, destroy_session, set_session_next, get_session_next, \
                     delete_session_next


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if verify_session():
            return f(*args, **kwargs)
        else:
            set_session_next(request.path)
            return redirect(url_for("login"))
    return wrapper


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/w/<string:wid>")
def work(wid):
    return render_template("index.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        return request.form["username"] + " " + request.form["email"] + " " + request.form["password"]
    return render_template("sign_up.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if verify_session():
        next_url = get_session_next()
        delete_session_next()
        return redirect(next_url)
    form = LoginForm()
    if form.validate_on_submit():
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


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")

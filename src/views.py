from flask import request, render_template
from src import app
from forms import SignUpForm, LoginForm


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
    form = LoginForm()
    if form.validate_on_submit():
        return request.form["username"] + " " + request.form["password"]
    return render_template("login.html", form=form)


@app.route("/tos", methods=["GET"])
def tos():
    return render_template("tos.html")


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")

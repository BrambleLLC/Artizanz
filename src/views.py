from flask import request, render_template
from src import app
from forms import SignUp


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/w/<string:wid>")
def work(wid):
    return render_template("index.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        return request.form["username"] + " " + request.form["email"] + " " + request.form["password"]
    return render_template("sign_up.html", form=form)

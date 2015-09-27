from flask import request, render_template
from src import app


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

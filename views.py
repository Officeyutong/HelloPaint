from main import app
from flask import render_template
@app.route("/login")
def view_login():
    return render_template("login.html")


@app.route("/")
def view_main():
    return render_template("main.html")

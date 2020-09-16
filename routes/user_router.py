from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users


@app.route("/logout")
def logout():
    del session["username"]
    del session["auth_lvl"]
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.login(username, password)
    return redirect("/")


@app.route("/create_new_user", methods=["POST"])
def create_new_user():
    if session["auth_lvl"] != 6:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = request.form["username"]
    password = request.form["password"]
    password_check = request.form["password_check"]
    auth_lvl = request.form["auth_lvl"]

    if password != password_check:
        return redirect("/")
    else:
        users.create_user(username, password, auth_lvl)
    return redirect("/")

from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import security


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


@app.route("/create_new_user_form")
def create_user_form():
    if session["auth_lvl"] != 6:
        abort(403)

    return render_template("user/create_new_user_form.html")


@app.route("/create_new_user", methods=["POST"])
def create_new_user():
    security.has_role([6])
    security.has_csrf_token(request.form["csrf_token"])

    username = request.form["username"]
    password = request.form["password"]
    password_check = request.form["password_check"]
    auth_lvl = request.form["auth_lvl"]

    if len(username) < 4:
        flash("Username must be at least 4 characters long.")
        return redirect("/create_new_user_form")

    if len(password) < 4:
        flash("Password must be at least 4 characters long.")
        return redirect("/create_new_user_form")

    if password != password_check:
        flash("Passwords doesn't match.")
        return redirect("/create_new_user_form")
    else:
        flash("User %s created succesfully." % username)
        users.create_user(username, password, auth_lvl)
    return redirect("/create_new_user_form")

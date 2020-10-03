from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import security


@app.route("/logout")
def logout():
    del session["username"]
    del session["auth_lvl"]
    del session["cart"]
    del session["supply"]
    del session["batch"]
    del session["sale"]
    del session["item"]
    del session["batch_page_count"]
    del session["sale_page_count"]
    del session["order_page_count"]
    del session["item_page_count"]
    del session["row_count"]
    flash("Logged out successfully", "success")
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    loggedIn = users.login(username, password)
    if loggedIn:
        return redirect("/")
    else:
        return render_template("user/login.html", username=username)


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

    if auth_lvl == 'None' or auth_lvl == 0:
        flash("Enter authorization level (1-6")
        return render_template("controller/controller_create_new_user.html", auth_lvl=auth_lvl, username=username)

    if len(username) < 4:
        flash("Username must be at least 4 characters long.", "danger")
        return render_template("controller/controller_create_new_user.html", auth_lvl=auth_lvl, username=username)

    if len(password) < 4:
        flash("Password must be at least 4 characters long.", "danger")
        return render_template("controller/controller_create_new_user.html", auth_lvl=auth_lvl, username=username)

    if password != password_check:
        flash("Passwords doesn't match.", "danger")
        return render_template("controller/controller_create_new_user.html", auth_lvl=auth_lvl, username=username)
    else:
        flash("User %s created succesfully." % username, "success")
        users.create_user(username, password, auth_lvl)
    return redirect("/create_new_user_form")

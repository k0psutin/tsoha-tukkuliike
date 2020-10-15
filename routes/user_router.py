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
    security.has_role([6])

    return render_template("user/create_new_user_form.html")


@app.route("/change_user_password", methods=["POST"])
def change_user_password():
    security.has_role([6])
    security.has_csrf_token(request.form["csrf_token"])
    username = request.form["username"]
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    validate = request.form["validate"]
    users.change_password(old_password, validate, new_password, username)
    return render_template("controller/controller_change_user_password.html", users=users.get_all_users())


@app.route("/create_new_user", methods=["POST"])
def create_new_user():
    security.has_role([6])
    security.has_csrf_token(request.form["csrf_token"])

    username = request.form["username"]
    password = request.form["password"]
    validate = request.form["password_check"]
    auth_lvl = request.form["auth_lvl"]

    success = users.create_user(username, password, validate, auth_lvl)
    if success == False:
        return render_template("controller/controller_create_new_user.html", auth_lvl=auth_lvl, username=username)

    return redirect("/controller_create_new_user")

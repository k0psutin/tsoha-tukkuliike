from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import db_interfaces.item as item
import db_interfaces.orders as orders


@app.route("/create_new_company_user", methods=["POST"])
def create_new_company_user():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = request.form["username"]
    password = request.form["password"]
    password_check = request.form["password_check"]
    company_id = request.form["company_id"]

    if password != password_check:
        flash("Passwords doesn't match.")
        return redirect("/")
    else:
        users.create_user(username, password, 1, company_id)
    return redirect("/")


@app.route("/create_company_user")
def create_company_user():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("user/create_company_user.html")


@app.route("/place_order", methods=["POST"])
def place_order():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 1 and session["auth_lvl"] != 4:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    order_list = list(filter(None, request.form.getlist("item_id")))
    qty_list = list(filter(None, request.form.getlist("qty")))
    price_list = list(filter(None, request.form.getlist("price")))
    company_id = request.form["company_id"]

    if company_id in (None, ''):
        flash("Company id can't be empty.")
        return redirect("/")

    order_id = orders.create_sale_order(
        company_id,
        order_list,
        qty_list,
        price_list,
        users.get_user_id())

    if order_id == 0:
        return redirect("/")

    return redirect("/order_summary/%s" % (order_id))


@app.route("/list_sale_orders")
def list_sale_orders():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)
    return render_template("sale/list_sale_orders.html", orders=orders.get_all_sale_orders(True))


@app.route("/place_company_order")
def place_company_order():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)
    return render_template("sale/sales_order_form.html", items=item.get_all_items())


@app.route("/order_summary/<string:order_id>")
def order_summary(order_id):
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 1 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("company/order_summary.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))

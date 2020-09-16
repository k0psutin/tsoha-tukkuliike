from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import db_interfaces.item as item
import db_interfaces.orders as orders


@app.route("/list_supply_orders")
def list_supply_orders():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("buyer/list_supply_orders.html", orders=orders.get_all_supply_orders())


@app.route("/list_items")
def items():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("buyer/list_items.html", items=item.get_all_items())


@app.route("/new_item_form")
def new_item_form():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)
    return render_template("buyer/new_item_form.html")


@app.route("/add_new_item", methods=["POST"])
def add_new_item():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    itemname = request.form["name"]
    price = request.form["price"]
    item.add_item(itemname, price)

    return redirect("buyer/new_item_form")


@app.route("/supply_order_form")
def supply_order_form():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)
    return render_template("buyer/supply_order_form.html", items=item.get_all_items())


@app.route("/place_supply_order", methods=["POST"])
def place_supply_order():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    company_id_list = list(filter(None, request.form.getlist("company_id")))
    qty_list = list(filter(None, request.form.getlist("qty")))
    price_list = list(filter(None, request.form.getlist("price")))
    item_list = list(filter(None, request.form.getlist("item_id")))
    user_id = users.get_user_id()

    if len(item_list) != len(price_list) != len(qty_list) != len(company_id_list):
        flash("One or more values are missing.")
        return redirect("/supply_order_form")

    orders.create_supply_order(
        company_id_list, item_list, qty_list, price_list, user_id)
    return redirect("/supply_order_form")

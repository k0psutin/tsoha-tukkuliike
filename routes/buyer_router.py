from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import db_interfaces.item as item
import db_interfaces.orders as orders
import db_interfaces.companies as companies
import security
import pagetools


@app.route("/list_supply_orders")
def list_supply_orders():
    security.has_role([4, 5, 6])

    return render_template("buyer/buyer_list_supply_orders.html", page_count=pagetools.supply_order_page_count(), orders=orders.get_all_supply_orders())


@app.route("/items")
def items():
    security.has_role([4, 5, 6])
    return render_template("buyer/buyer_items.html", page_count=pagetools.item_page_count(), items=item.get_all_items())


@app.route("/new_item_form")
def new_item_form():
    security.has_role([5, 6])

    return render_template("buyer/buyer_new_item_form.html")


@app.route("/add_new_item", methods=["POST"])
def add_new_item():
    security.has_role([5, 6])
    security.has_csrf_token(request.form["csrf_token"])

    itemname = request.form["name"]
    price = request.form["price"]

    item.add_item(itemname, price)

    if security.has_auth([6]):
        return redirect("/controller_list_items#form")

    return redirect("/items#form")


@app.route("/supply_order_form")
def supply_order_form():
    security.has_role([5, 6])
    return render_template("buyer/buyer_supply_order.html", companies=companies.get_all_companies(), items=item.get_all_items())


@app.route("/place_supply_order", methods=["POST"])
def place_supply_order():
    security.has_role([5, 6])
    security.has_csrf_token(request.form["csrf_token"])

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

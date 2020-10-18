from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import db_interfaces.item as item
import db_interfaces.orders as orders
import db_interfaces.companies as companies
import db_interfaces.logistics as logistics
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


@app.route("/inventory_status")
def inventory_status():
    security.has_role([5, 6])
    return render_template("buyer/buyer_inventory_status.html")


@app.route("/supply_order_form")
def supply_order_form():
    security.has_role([5, 6])
    return render_template("buyer/buyer_supply_order.html", companies=companies.get_all_companies(), items=item.get_all_items(False))


@app.route("/inventory_report", methods=["POST"])
def inventory_report():
    security.has_role([5, 6])
    security.has_csrf_token(request.form["csrf_token"])

    return logistics.inventory_data()


@app.route("/create_new_supplier")
def create_new_supplier():
    security.has_role([5, 6])
    return render_template("buyer/buyer_create_new_supplier.html")

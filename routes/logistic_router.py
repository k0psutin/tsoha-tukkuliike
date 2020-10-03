from app import app
from flask import request, redirect, render_template

import db_interfaces.logistics as logistics
import db_interfaces.orders as orders
import security
import pagetools


@app.route("/create_batch", methods=["POST"])
def create_batch():
    security.has_role([2, 6])
    security.has_csrf_token(request.form["csrf_token"])

    order_id = request.form["order_id"]
    qty = request.form["qty"]

    logistics.create_new_batch(order_id, qty)
    return redirect("/#form")


@app.route("/inventory_view")
def list_batches():
    security.has_role([2, 4, 5, 6])
    return render_template("logistic/logistic_inventory_view.html", batches=logistics.get_all_batches())


@app.route("/batch_inventory")
def batch_inventory():
    security.has_role([2, 6])
    return render_template("logistic/logistic_batch_inventory.html", page_count=pagetools.batch_page_count(), batches=logistics.get_all_batches())


@app.route("/supply_order_inventory")
def supply_order_inventory():
    security.has_role([2, 6])
    return render_template("logistic/logistic_supply_order_inventory.html", page_count=pagetools.supply_order_page_count(), orders=orders.get_all_supply_orders())


@app.route("/update_batch", methods=["POST"])
def update_batch():
    security.has_role([2, 6])
    security.has_csrf_token(request.form["csrf_token"])

    batchnr = request.form["batchnr"]
    qty = request.form["qty"]

    logistics.update_batch_qty(batchnr, qty)
    if security.has_auth([6]):
        return redirect("/controller_batches")

    return redirect("/batch_inventory#form")


@app.route("/update_supply_order", methods=["POST"])
def update_supply_order():
    security.has_role([2, 6])
    security.has_csrf_token(request.form["csrf_token"])

    order_id = request.form["order_id"]
    qty = request.form["qty"]

    logistics.update_supply_order_qty(order_id, qty)
    if security.has_auth([6]):
        return redirect("/controller_supply_orders")

    return redirect("/supply_order_inventory#form")

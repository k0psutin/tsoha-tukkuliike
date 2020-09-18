from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.logistics as logistics
import db_interfaces.orders as orders
import security


@app.route("/create_shipment", methods=["POST"])
def create_shipment():
    security.has_role([3, 6])
    security.has_csrf_token(request.form["csrf_token"])

    order_id = request.form["order_id"]

    logistics.create_new_shipment(order_id)
    flash("Order %s completed." % order_id)
    return redirect("/")


@app.route("/collect_batch", methods=["POST"])
def collect_batch():
    security.has_role([3, 6])
    security.has_csrf_token(request.form["csrf_token"])

    order_id = request.form["order_id"]
    batch_nr = request.form["batch_nr"]
    qty = request.form["qty"]

    logistics.collect_to_batchorder(order_id, qty, batch_nr)
    return redirect("/collect_order/%s" % (order_id))


@app.route("/collect_order/<string:order_id>")
def collect_order(order_id):
    security.has_role([3, 6])

    return render_template("collector/collect_order.html",
                           order_id=order_id,
                           orderdetails=orders.get_sale_order(order_id),
                           batches=logistics.get_all_batches())

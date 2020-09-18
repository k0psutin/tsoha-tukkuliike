from typing import ItemsView
from app import app
from flask import render_template, session, abort
import db_interfaces.orders as orders
import db_interfaces.logistics as logistics
import security


@app.route("/logistics")
def logistic():
    security.has_role([6])

    return render_template("logistic/logistics.html", orders=orders.get_all_supply_orders())


@app.route("/collector")
def collector():
    security.has_role([6])

    return render_template("collector/collector.html", orders=orders.get_all_sale_orders(), batches=logistics.get_all_batches())


@app.route("/sales")
def sales():
    security.has_role([6])

    return render_template("sale/sales.html")


@app.route("/buyer")
def buyer():
    security.has_role([6])

    return render_template("buyer/buyer.html")

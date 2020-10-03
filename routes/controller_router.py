from app import app
from flask import render_template, session, abort
import db_interfaces.orders as orders
import db_interfaces.logistics as logistics
import db_interfaces.item as item
import db_interfaces.companies as companies
import security
import pagetools


@app.route("/controller_supply_orders")
def controller_supply_orders():
    security.has_role([6])
    return render_template("controller/controller_supply.html", page_count=pagetools.supply_order_page_count(), orders=orders.get_all_supply_orders())


@app.route("/controller_batches")
def controller_batches():
    security.has_role([6])
    return render_template("controller/controller_batches.html", page_count=pagetools.batch_page_count(), batches=logistics.get_all_batches())


@app.route("/controller_new_supply_order")
def controller_new_supply_order():
    security.has_role([6])
    return render_template("controller/controller_new_supply_order.html", companies=companies.get_all_companies(), items=item.get_all_items())


@app.route("/order_detail/<string:order_id>")
def order_detail(order_id):
    security.has_role([6])

    return render_template("controller/controller_order_detail.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))


@app.route("/controller_list_items")
def controller_list_items():
    security.has_role([6])
    return render_template("controller/controller_list_items.html", page_count=item.item_page_count(), items=item.get_all_items())


@app.route("/controller_list_sale_orders")
def controller_list_sale_orders():
    security.has_role([6])
    return render_template("controller/controller_list_sale_orders.html", page_count=pagetools.sales_page_count(), orders=orders.get_all_sale_orders())


@app.route("/controller_create_new_user")
def controller_create_new_user():
    security.has_role([6])
    return render_template("controller/controller_create_new_user.html")

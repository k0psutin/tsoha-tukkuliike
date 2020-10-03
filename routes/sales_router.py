from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.item as item
import db_interfaces.orders as orders
import db_interfaces.companies as companies
import pagetools
import security


@app.route("/create_company_user")
def create_company_user():
    security.has_role([4, 6])

    return render_template("sale/sale_create_company_user.html", companies=companies.get_all_companies())


@app.route("/place_order", methods=["POST"])
def place_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

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


@app.route("/list_orders")
def list_sale_orders():
    security.has_role([4, 6])
    return render_template("sale/sale_list_orders.html", page_count=pagetools.open_order_page_count(), orders=orders.get_all_sale_orders(True))


@app.route("/update_sale_order", methods=["POST"])
def update_sale_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_list = request.form["item_id"]
    qty_list = request.form["qty"]
    order_id = request.form["order_id"]
    company_id = request.form["company_id"]

    orders.update_sale_order_item_qty(
        order_id, item_list, company_id, qty_list)
    return redirect("/modify_order/%s" % order_id)


@app.route("/remove_item_from_sale_order", methods=["POST"])
def remove_item_From_sale_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_id = request.form["item_id"]
    order_id = request.form["order_id"]

    orders.remove_item_from_sale_order(item_id, order_id)
    removed_item = item.get_item_by_id(item_id)
    flash("%s removed from order" % removed_item[1], "successs")
    return redirect("/modify_order/%s" % order_id)


@app.route("/add_item_to_order", methods=["POST"])
def add_item_to_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_id = request.form["item_id"]
    order_id = request.form["order_id"]
    company_id = request.form["company_id"]
    qty = request.form["qty"]

    orders.add_item_to_sale_order(order_id, company_id, item_id, qty)
    return redirect("/modify_order/%s" % order_id)


@app.route("/create_order")
def place_company_order():
    security.has_role([4, 6])
    return render_template("sale/sale_create_order.html", companies=companies.get_all_companies(), items=item.get_all_items())


@app.route("/delete_order", methods=["POST"])
def delete_order():
    security.has_role([4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    order_id = request.form["order_id"]
    orders.delete_order_by_order_id(order_id)
    return redirect("/list_orders")


@app.route("/modify_order/<string:order_id>")
def modify_order(order_id):
    security.has_role([4, 6])

    return render_template("sale/sale_modify_order.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))

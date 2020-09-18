from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import db_interfaces.item as item
import db_interfaces.orders as orders
import security


@app.route("/create_new_company_user", methods=["POST"])
def create_new_company_user():
    security.has_role([4, 6])
    security.has_csrf_token(request.form["csrf_token"])

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
    security.has_role([4, 6])

    return render_template("user/create_company_user.html")


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


@app.route("/list_sale_orders")
def list_sale_orders():
    security.has_role([4, 6])
    return render_template("sale/list_sale_orders.html", orders=orders.get_all_sale_orders(True))


@app.route("/update_sale_order", methods=["POST"])
def update_sale_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_list = request.form.getlist("item_id")
    qty_list = request.form.getlist("qty")
    order_id = request.form["order_id"]
    company_id = request.form["company_id"]
    print(item_list)
    print(qty_list)
    orders.update_sale_order_item_qty(
        order_id, item_list, company_id, qty_list)
    return redirect("/modify_order/%s" % order_id)


@app.route("/remove_item_From_sale_order", methods=["POST"])
def remove_item_From_sale_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_id = request.form["item_id"]
    order_id = request.form["order_id"]
    orders.remove_item_from_sale_order(item_id, order_id)
    removed_item = item.get_item_by_id(item_id)
    flash("%s removed from order" % removed_item[1])
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


@app.route("/place_company_order")
def place_company_order():
    security.has_role([4, 6])
    return render_template("sale/sales_order_form.html", items=item.get_all_items())


@app.route("/order_summary/<string:order_id>")
def order_summary(order_id):
    security.has_role([1, 4, 6])

    return render_template("company/order_summary.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))


@app.route("/delete_order", methods=["POST"])
def delete_order():
    security.has_role([4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    order_id = request.form["order_id"]
    orders.delete_order_by_order_id(order_id)
    return redirect("/list_sale_orders")


@app.route("/modify_order/<string:order_id>")
def modify_order(order_id):
    security.has_role([4, 6])

    return render_template("sale/modify_order.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))

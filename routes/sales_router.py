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


@app.route("/create_company")
def create_company():
    security.has_role([4, 6])
    return render_template("sale/sale_create_company.html")


@app.route("/list_orders")
def list_sale_orders():
    security.has_role([4, 6])
    return render_template("sale/sale_list_orders.html", page_count=pagetools.sales_page_count(), orders=orders.get_all_sale_orders(False))


@app.route("/sale_report")
def sale_report():
    security.has_role([4, 6])
    return render_template("sale/sale_report.html")


@app.route("/sales_by_year", methods=["POST"])
def sales_by_month():
    security.has_role([4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    year = request.form["year"]

    return orders.get_sales_by_year(year)


@app.route("/update_sale_order", methods=["POST"])
def update_sale_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_id = request.form["item_id"]
    qty = request.form["qty"]
    order_id = request.form["order_id"]
    company_id = request.form["company_id"]

    orders.update_sale_order_item_qty(
        order_id, item_id, company_id, qty)
    return "OK"


@app.route("/remove_item_from_sale_order", methods=["POST"])
def remove_item_From_sale_order():
    security.has_role([1, 4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    item_id = request.form["item_id"]
    order_id = request.form["order_id"]

    order_deleted = orders.remove_item_from_sale_order(item_id, order_id)
    removed_item = item.get_item_by_id(item_id)
    if order_deleted:
        flash("Last item removed from order %s" % (order_id), "warning")
        return redirect("/list_orders")

    flash("%s removed from order" % removed_item[1], "success")
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
    return render_template("sale/sale_create_order.html", companies=companies.get_all_companies(), items=item.get_all_items(False))


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
                           items=item.get_all_items(False),
                           order_date=orders.get_order_date(order_id)[0],
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))

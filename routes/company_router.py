from app import app
from flask import session, abort, request, flash, redirect, render_template

import db_interfaces.users as users
import db_interfaces.item as item
import db_interfaces.orders as orders
import db_interfaces.companies as companies
import security


@app.route("/create_new_company_user", methods=["POST"])
def create_new_company_user():
    security.has_role([4, 6])
    security.has_csrf_token(request.form["csrf_token"])

    username = request.form["username"]
    password = request.form["password"]
    password_check = request.form["password_check"]
    company_id = request.form["company_id"]

    company = companies.get_company(company_id)

    if company_id == None or company_id == '' or company == None:
        flash("A company must be selected.", "danger")
        return render_template("sale/sale_create_company_user.html", username=username, company_id=company_id, companies=companies.get_all_companies())

    if password != password_check:
        flash("Passwords doesn't match.", "danger")
        return render_template("sale/sale_create_company_user.html", username=username, company_id=company_id, companies=companies.get_all_companies())
    else:
        users.create_user(username, password, 1, company_id)
    return redirect("/")


@app.route("/company_change_password", methods=["POST"])
def change_password():
    security.has_csrf_token(request.form["csrf_token"])
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    validate = request.form["validate"]

    users.change_password(old_password, validate, new_password)

    return redirect("/company_info")


@app.route("/company_info")
def company_info():
    user = users.get_current_user()
    company_id = user[4]
    return render_template("company/company_info.html", user=user, company=companies.get_company(company_id))


@app.route("/create_new_order")
def create_new_order():
    security.has_role([1, 6])
    return render_template("company/company_create_new_order.html", items=item.get_all_items())


@app.route("/order_summary/<string:order_id>")
def order_summary(order_id):
    security.has_role([1, 4, 6])
    return render_template("company/company_order_summary.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id),
                           order_date=orders.get_order_date(order_id)[0])

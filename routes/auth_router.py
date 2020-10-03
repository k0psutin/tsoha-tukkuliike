from flask import redirect, render_template, session
from app import app

import db_interfaces.users as users
import db_interfaces.logistics as logistics
import db_interfaces.orders as orders
import pagetools


@app.route("/")
def index():
    if session.get("username") == None:
        return render_template("user/login.html")
    else:
        return user_redirect()


def user_redirect():
    switcher = {
        0: error(),
        1: customer(),
        2: logistic(),
        3: collector(),
        4: sales(),
        5: buyer(),
        6: controller()
    }

    return switcher.get(session["auth_lvl"])


def error():
    return redirect("/")


def customer():
    company_id = users.get_company_id()
    return render_template("company/company.html", company_id=company_id, orders=orders.get_all_sales_by_company_id(company_id))


def logistic():
    return render_template("logistic/logistics.html", page_count=pagetools.supply_order_page_count(), orders=orders.get_all_supply_orders())


def collector():
    return render_template("collector/collector.html", page_count=pagetools.sales_page_count(), orders=orders.get_all_sale_orders())


def sales():
    return render_template("sale/sales.html", page_count=pagetools.batch_page_count(), batches=logistics.get_all_batches())


def buyer():
    return render_template("buyer/buyer.html", page_count=pagetools.batch_page_count(), batches=logistics.get_all_batches())


def controller():
    return render_template("controller/controller.html")

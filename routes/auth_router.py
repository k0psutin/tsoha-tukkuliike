from flask import redirect, render_template, session
from app import app

import db_interfaces.users as users
import db_interfaces.logistics as logistics
import db_interfaces.item as item
import db_interfaces.orders as orders


@app.route("/")
def index():
    if session.get("username") == None:
        return render_template("login.html")
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
    return render_template("company/company_order.html", company_id=users.get_company_id(), items=item.get_all_items())


def logistic():
    return render_template("logistic/logistics.html", orders=orders.get_all_supply_orders())


def collector():
    return render_template("collector/collector.html", orders=orders.get_all_sale_orders(), batches=logistics.get_all_batches())


def sales():
    return render_template("sale/sales.html")


def buyer():
    return render_template("buyer/buyer.html")


def controller():
    return render_template("controller/controller.html")

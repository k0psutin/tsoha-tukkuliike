from flask import redirect, render_template, session
from db import db
import users
import logistics
import item
import orders


def switch():
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
    return render_template("company_order.html", company_id=users.get_company_id(), items=item.get_all_items())


def logistic():
    return render_template("logistics.html", orders=orders.get_all_supply_orders())


def collector():
    return render_template("collector.html", orders=orders.get_all_sale_orders(), batches=logistics.get_all_batches())


def sales():
    return render_template("sales.html")


def buyer():
    return render_template("supply_order.html")


def controller():
    return render_template("controller.html")

from flask import session
import math
import db_interfaces.orders as orders
import db_interfaces.logistics as logistics
import db_interfaces.item as item

# I tried to refactor these into one function.
# While it worked in local, Heroku couldn't find some modules.


def supply_order_page_count():
    page_count = orders.get_orders_page_count(True)
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(page_count[0]/session["row_count"])

    if session["supply"] > page_count-1:
        session["supply"] = 0

    session["supply_page_count"] = page_count


def batch_page_count():
    page_count = logistics.get_batch_page_count()
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(page_count[0]/session["row_count"])

    if session["batch"] > page_count-1:
        session["batch"] = 0

    session["batch_page_count"] = page_count


def sales_page_count():
    page_count = orders.get_all_sale_order_page_count(False)
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(len(page_count)/session["row_count"])

    if session["sale"] > page_count-1:
        session["sale"] = 0

    session["sale_page_count"] = page_count


def open_order_page_count():
    page_count = orders.get_all_sale_order_page_count(True)
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(len(page_count)/session["row_count"])

    if session["sale"] > page_count-1:
        session["sale"] = 0

    session["sale_page_count"] = page_count


def item_page_count():
    page_count = item.item_page_count()
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(page_count)

    if session["item"] > page_count-1:
        session["item"] = 0

    session["item_page_count"] = page_count

from flask import session
import math
import db_interfaces.orders as orders
import db_interfaces.logistics as logistics
import db_interfaces.item as item


def supply_order_page_count():
    page_count = orders.get_orders_page_count(True)
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(page_count[0]/10)

    session["order_page_count"] = page_count


def batch_page_count():
    page_count = logistics.get_batch_page_count()
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(page_count[0]/10)
    session["batch_page_count"] = page_count


def sales_page_count():
    page_count = orders.get_all_sale_order_page_count(False)
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(len(page_count)/10)
    session["sale_page_count"] = page_count


def open_order_page_count():
    page_count = orders.get_all_sale_order_page_count(True)
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(len(page_count)/10)
    session["order_page_count"] = page_count


def item_page_count():
    page_count = item.item_page_count()
    if page_count == None:
        page_count = 0
    else:
        page_count = math.ceil(page_count)
    session["item_page_count"] = page_count

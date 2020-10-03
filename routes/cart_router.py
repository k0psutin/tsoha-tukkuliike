from app import app
from flask import request, session, jsonify, flash, redirect

import db_interfaces.users as users
import db_interfaces.orders as orders
import security

from random import randint


@app.route("/cart_count", methods=["GET"])
def cart_count():
    return str(len(session["cart"]))


@app.route("/get_cart", methods=["GET"])
def get_cart():
    return jsonify(session["cart"])


@app.route("/remove_item_from_cart", methods=["POST"])
def remove_item_from_cart():
    security.has_csrf_token(request.form["csrf_token"])
    security.has_role([1, 4, 5, 6])
    item_id = request.form["item_id"]
    cart = list(session["cart"])
    new_list = []

    for i in range(len(cart)):
        if cart[i]["item_id"] != item_id:
            new_list.append(cart[i])

    session["cart"] = new_list
    return "OK"


@app.route("/update_cart_item_qty", methods=["POST"])
def update_cart_item_qty():
    security.has_csrf_token(request.form["csrf_token"])
    security.has_role([1, 4, 5, 6])
    item_id = request.form["item_id"]
    qty = request.form["qty"]
    cart = list(session["cart"])

    for i in range(len(cart)):
        if cart[i]["item_id"] == item_id:
            cart[i]["qty"] = qty

    session["cart"] = cart
    return "OK"


@app.route("/add_item_to_cart", methods=["POST"])
def add_item_to_cart():
    security.has_csrf_token(request.form["csrf_token"])
    security.has_role([1, 4, 5, 6])

    item = None
    company_id = None

    if session["auth_lvl"] == 1:
        company_id = users.get_company_id()

    if session["auth_lvl"] == 5 or session["auth_lvl"] == 6:
        company_id = request.form["company_id"]
        if company_id == None or company_id == '':
            flash("Select a company", "danger")
            return "OK"

    item_name = request.form["item_name"]
    item_id = request.form["item_id"]
    qty = request.form["qty"]
    price = request.form["price"]
    user_id = users.get_user_id()

    if item_name == None or item_name == '':
        flash("Select an item", "danger")
        return "OK"

    if item_id == None or item_id == '':
        flash("Item id is missing", "danger")
        return "OK"

    if qty == None or qty == '' or int(qty) == 0 or int(qty) < 0:
        flash("Quantity must be non-empty and more than zero", "danger")
        return "OK"

    if price == None or price == '' or float(price) == 0 or float(price) < 0:
        flash("Price must be non-empty and more than zero", "danger")
        return "OK"

    cart = list(session["cart"])
    if session["auth_lvl"] == 6 or session["auth_lvl"] == 5 or session["auth_lvl"] == 1:
        item = {"company_id": company_id, "item_id": item_id, "item_name": item_name,
                "qty": qty, "price": price, "user_id": user_id}

    if session["auth_lvl"] == 4:
        item = {"item_id": item_id, "item_name": item_name,
                "qty": qty, "price": price, "user_id": user_id}

    new_item = True

    for i in range(len(cart)):
        if cart[i]["item_id"] == item_id:
            cart[i]["qty"] = int(cart[i]["qty"]) + int(qty)
            cart[i]["price"] = price
            new_item = False

    if new_item:
        cart.append(item)

    session["cart"] = cart
    return str(len(cart))


@app.route("/clear_cart", methods=["POST"])
def clear_cart():
    security.has_csrf_token(request.form["csrf_token"])
    security.has_role([1, 4, 5, 6])
    session["cart"] = {}
    return "OK"


@app.route("/finalize_order", methods=["POST"])
def finalize_order():
    security.has_csrf_token(request.form["csrf_token"])
    security.has_role([1, 4, 5, 6])
    company_id = None
    if session["auth_lvl"] == 4:
        company_id = request.form["company_id"]

    random_number = str(randint(0, 9999999))
    order_id = random_number.zfill(7)
    user_id = users.get_user_id()

    cart = session["cart"]

    orderList = []

    for i in range(len(cart)):
        order = None
        if session["auth_lvl"] == 4:
            order = {'order_id': order_id,
                     'company_id': company_id,
                     'item_id': cart[i]["item_id"],
                     'qty': cart[i]["qty"],
                     'user_id': user_id,
                     'price': cart[i]["price"]}

        if session["auth_lvl"] == 6 or session["auth_lvl"] == 5 or session["auth_lvl"] == 1:
            order = {'order_id': order_id,
                     'company_id': cart[i]["company_id"],
                     'item_id': cart[i]["item_id"],
                     'qty': cart[i]["qty"],
                     'user_id': user_id,
                     'price': cart[i]["price"]}
        orderList.append(order)

    session["cart"] = []

    if session["auth_lvl"] == 5 or session["auth_lvl"] == 6:
        orders.create_supply_order(orderList)
        flash("Order was successful", "success")
        return order_id
    if session["auth_lvl"] == 4 or session["auth_lvl"] == 1:
        success = orders.create_sale_order(order_id, orderList)
        if success:
            return order_id
        else:
            flash("Sale order unsuccessful", "danger")

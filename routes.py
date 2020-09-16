from flask import request, redirect, render_template, session, abort
from flask.helpers import flash
from app import app
import item
import users
import viewcontroller
import logistics
import orders
import companies


@app.route("/")
def index():
    if session.get("username") == None:
        return render_template("login.html")
    else:
        return viewcontroller.switch()


@app.route("/logout")
def logout():
    del session["username"]
    del session["auth_lvl"]
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.login(username, password)
    return redirect("/")


@app.route("/create_company_user")
def create_company_user():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("create_company_user.html")


@app.route("/create_new_company_user", methods=["POST"])
def create_new_company_user():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

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


@app.route("/create_new_user", methods=["POST"])
def create_new_user():
    if session["auth_lvl"] != 6:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = request.form["username"]
    password = request.form["password"]
    password_check = request.form["password_check"]
    auth_lvl = request.form["auth_lvl"]

    if password != password_check:
        return redirect("/")
    else:
        users.create_user(username, password, auth_lvl)
    return redirect("/")


@app.route("/create_batch", methods=["POST"])
def create_batch():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 2:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    order_id = request.form["order_id"]
    qty = request.form["qty"]

    logistics.create_new_batch(order_id, qty)

    return redirect("/")


@app.route("/list_batches")
def list_batches():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("list_batches.html", batches=logistics.get_all_batches())


@app.route("/new_item_form")
def new_item_form():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)
    return render_template("new_item_form.html")


@app.route("/add_new_item", methods=["POST"])
def add_new_item():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    itemname = request.form["name"]
    price = request.form["price"]
    item.add_item(itemname, price)

    return redirect("/new_item_form")


@app.route("/show_items")
def items():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("items.html", items=item.get_items())


@app.route("/place_order", methods=["POST"])
def place_order():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 1 and session["auth_lvl"] != 4:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    order_list = list(filter(None, request.form.getlist("item_id")))
    qty = list(filter(None, request.form.getlist("qty")))
    company_id = request.form["company_id"]

    order_id = orders.create_sale_order(
        company_id,
        order_list,
        qty,
        users.get_user_id())

    if order_id == 0:
        return redirect("/")

    return redirect("/order_summary/%s" % (order_id))


@app.route("/order_summary/<string:order_id>")
def order_summary(order_id):
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 1 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("order_summary.html",
                           order_id=order_id,
                           total=orders.get_order_total(order_id),
                           company=orders.get_company_by_order_id(order_id),
                           order=orders.get_sale_order(order_id))


@app.route("/collect_order/<string:order_id>")
def collect_order(order_id):
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 3:
        abort(403)

    return render_template("collect_order.html",
                           order_id=order_id,
                           orderdetails=orders.get_sale_order(order_id),
                           batches=logistics.get_all_batches())


@app.route("/collect_batch", methods=["POST"])
def collect_batch():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 3:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    order_id = request.form["order_id"]
    batch_nr = request.form["batch_nr"]
    qty = request.form["qty"]
    logistics.collect_to_batchorder(order_id, qty, batch_nr)
    return redirect("/collect_order/%s" % (order_id))


@app.route("/supply_order_form")
def supply_order_form():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)
    return render_template("supply_order_form.html", items=item.get_all_items())


@app.route("/place_company_order")
def place_company_order():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)
    return render_template("sales_order_form.html", items=item.get_all_items())


@app.route("/list_sale_orders")
def list_sale_orders():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 4:
        abort(403)
    return render_template("list_sale_orders.html", orders=orders.get_all_sale_orders(True))


@app.route("/place_supply_order", methods=["POST"])
def place_supply_order():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    company_id_list = list(filter(None, request.form.getlist("company_id")))
    qty_list = list(filter(None, request.form.getlist("qty")))
    price_list = list(filter(None, request.form.getlist("price")))
    item_list = list(filter(None, request.form.getlist("item_id")))
    user_id = users.get_user_id()

    if len(item_list) != len(price_list) != len(qty_list) != len(company_id_list):
        flash("One or more values are missing.")
        return redirect("/supply_order_form")

    orders.create_supply_order(
        company_id_list, item_list, qty_list, price_list, user_id)
    return redirect("/supply_order_form")


@app.route("/list_supply_orders")
def list_supply_orders():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 5 and session["auth_lvl"] != 4:
        abort(403)

    return render_template("list_supply_orders.html", orders=orders.get_all_supply_orders())


@app.route("/create_shipment", methods=["POST"])
def create_shipment():
    if session["auth_lvl"] != 6 and session["auth_lvl"] != 3:
        abort(403)

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    order_id = request.form["order_id"]
    logistics.create_new_shipment(order_id)
    flash("Order %s completed." % order_id)
    return redirect("/")

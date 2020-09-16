from app import app
from flask import session, abort, request, redirect, render_template

import db_interfaces.logistics as logistics
import db_interfaces.orders as orders


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

    return render_template("logistic/list_batches.html", batches=logistics.get_all_batches())

from flask.helpers import flash
from flask import session
from datetime import date
from db_interfaces.db import db

import db_interfaces.users as users
import db_interfaces.item as item


def get_batch_page_count():
    sql = "SELECT COUNT(*) FROM batches WHERE qty > 0"
    result = db.session.execute(sql)
    return result.fetchone()


def get_all_batches():
    row_count = session["row_count"]
    offset = session["batch"] * 10
    sql = """SELECT batch_nr, items.itemname, batches.qty, date
             FROM batches
             INNER JOIN items ON (batches.item_id = items.item_id)
             WHERE qty > 0 LIMIT :row_count OFFSET :offset"""

    result = db.session.execute(
        sql, {"row_count": row_count, "offset": offset})
    return result.fetchall()


def get_batch_by_batchnr(batchnr):
    sql = """SELECT * FROM batches WHERE batch_nr = :batchnr"""
    result = db.session.execute(sql, {"batchnr": batchnr})
    return result.fetchone()


def check_if_batch_exists(batch_nr):
    sql = "SELECT batch_nr FROM batches WHERE batch_nr = :batch_nr"
    result = db.session.execute(sql, {"batch_nr": batch_nr})
    return result.fetchone() != None


def update_supply_order_qty(order_id, new_qty):
    order = get_supply_order_by_id(order_id)

    if order == None:
        flash("Invalid order id", "danger")
        return

    if int(new_qty) < 0:
        flash("Negative quantity not allowed", "danger")
        return

    sql = "UPDATE orders SET qty = :updated_qty WHERE order_id = :order_id"
    db.session.execute(
        sql, {"updated_qty": new_qty, "order_id": order_id})

    db.session.commit()
    flash("Supply order %s quantity updated" % order_id, "success")
    return


def update_batch_qty(batchnr, new_qty):
    new_qty = int(new_qty)
    if check_if_batch_exists(batchnr) == False:
        flash("Invalid batch number", "danger")
        return

    if new_qty < 0:
        flash("Negative quantity not allowed", "danger")
        return

    sql = "UPDATE batches SET qty = :updated_qty WHERE batch_nr = :batchnr"
    db.session.execute(
        sql, {"updated_qty": new_qty, "batchnr": batchnr})

    db.session.commit()
    flash("Batch %s quantity updated" % batchnr, "success")
    return


def get_supply_order_by_id(order_id):
    sql = """SELECT orders.company_id,
                    orders.item_id,
                    items.itemname,
                    companies.country,
                    orders.qty,
                    NOW()
             FROM orders
                INNER JOIN items ON (orders.item_id = items.item_id)
                INNER JOIN companies ON (orders.company_id = companies.company_id)
             WHERE order_id = :order_id"""

    result = db.session.execute(sql, {"order_id": order_id})

    return result.fetchone()


def create_new_batch(order_id, qty):

    qty = int(qty)
    if qty <= 0:
        flash("Quantity must be larger than zero", "danger")
        return False

    order = get_supply_order_by_id(order_id)

    if qty > order[4]:
        flash("Quantity exceeds order quantity", "danger")
        return False

    if order == None:
        flash("Order %s does not exist" % order_id, "danger")
        return False

    current_date = date.today().strftime("%d%m%y")
    item = order[2]
    prefix = item[0].upper() + item[len(item)-1].upper()
    batch_nr = prefix + current_date + order[3]

    if check_if_batch_exists(batch_nr):
        order_qty = int(order[4])
        updated_qty = order_qty - qty

        if updated_qty < 0:
            updated_qty = 0

        add_batch_qty(batch_nr, qty)
        update_supply_order_qty(order_id, updated_qty)
        flash("Batch %s updated succesfully" % batch_nr, "success")
        return False

    order_qty = int(order[4])
    updated_qty = order_qty - qty

    if updated_qty < 0:
        flash("Transfererd quantity exceeds order quantity", "danger")
        return False

    user_id = users.get_user_id()
    sql2 = """INSERT INTO batches (batch_nr, company_id, item_id, qty, date, user_id)
             VALUES (:batch_nr, :company_id, :item_id, :qty, :now, :user_id)"""

    db.session.execute(sql2, {
                       "batch_nr": batch_nr, "company_id": order[0], "item_id": order[1], "qty": qty, "now": order[5], "user_id": user_id})

    sql3 = "UPDATE orders SET qty = :updated_qty WHERE order_id = :order_id"
    db.session.execute(
        sql3, {"updated_qty": updated_qty, "order_id": order_id})

    db.session.commit()
    flash("Batch %s created successfully" % batch_nr, "success")
    return True


def add_batch_qty(batch_nr, qty):
    qty = int(qty)
    sql = "SELECT qty FROM batches WHERE batch_nr = :batch_nr"
    result = db.session.execute(sql, {"batch_nr": batch_nr})
    validate_qty = int(result.fetchone()[0])
    result_qty = validate_qty + qty

    if result_qty < 0:
        flash("Negative batch qty is not allowed", "danger")
        return False

    sql = "UPDATE batches SET qty = (batches.qty+:qty) WHERE batch_nr = :batch_nr"
    db.session.execute(sql, {"qty": qty, "batch_nr": batch_nr})
    db.session.commit()
    return True


def add_batchorder_qty(batchorder_id, qty):
    qty = int(qty)
    sql = "SELECT qty FROM batchorders WHERE batchorder_id = :batchorder_id"
    result = db.session.execute(sql, {"batchorder_id": batchorder_id})
    validate_qty = result.fetchone()[0]
    result_qty = validate_qty + qty

    if result_qty < 0:
        flash("Negative quantity is not allowed", "danger")
        return False

    sql = "UPDATE batchorders SET qty = (batchorders.qty + :qty) WHERE batchorder_id = :batchorder_id"
    db.session.execute(sql, {"qty": qty, "batchorder_id": batchorder_id})
    db.session.commit()
    return True


def collect_to_batchorder(order_id, qty, batch_nr):
    qty = int(qty)

    if qty <= 0 or qty == '':
        flash("Quantity must be more than zero", "danger")
        return False

    sql = """SELECT batches.item_id,
                    orders.item_id
             FROM batches
             INNER JOIN orders ON (batches.item_id = orders.item_id)
             WHERE batch_nr = :batch_nr and order_id = :order_id"""

    result = db.session.execute(
        sql, {"order_id": order_id, "batch_nr": batch_nr})
    valid_order = result.fetchall()

    if len(valid_order) == 0:
        flash("This item doesn't belong to this order", "danger")
        return False

    sql = """SELECT batchorders.batchorder_id,
                    items.itemname,
                    (orders.qty - batchorders.qty),
                    batchorders.qty
             FROM batchorders
             INNER JOIN batches ON (batchorders.batch_nr = batches.batch_nr)
             INNER JOIN items ON (batches.item_id = items.item_id)
             INNER JOIN orders ON (orders.item_id = items.item_id)
             WHERE batchorders.order_id = :order_id
                AND orders.supply = FALSE
                AND batchorders.batch_nr = :batch_nr"""

    result = db.session.execute(
        sql, {"order_id": order_id, "batch_nr": batch_nr})
    batchorder = result.fetchone()

    if batchorder == None:
        sql = "SELECT orders.qty FROM orders WHERE order_id = :order_id"
        result = db.session.execute(sql, {"order_id": order_id})
        valid_qty = result.fetchone()[0]

        if qty > valid_qty:
            flash("Collected quantity exceeds remaining quantity", "danger")
            return False

        item_id = item.get_itemid_by_batchnr(batch_nr)
        sql = "INSERT INTO batchorders (order_id, item_id, batch_nr, qty) VALUES (:order_id, :item_id, :batch_nr, :qty)"
        db.session.execute(
            sql, {"order_id": order_id, "qty": qty, "batch_nr": batch_nr, "item_id": item_id})
        db.session.commit()
        new_qty = qty * -1
        add_batch_qty(batch_nr, new_qty)
        return True
    else:
        valid_qty = batchorder[2]
        if qty > valid_qty:
            flash("Collected quantity exceeds remaining quantity", "danger")
            return False

        add_batchorder_qty(batchorder[0], qty)
        new_qty = qty * -1
        add_batch_qty(batch_nr, new_qty)
        return True


def create_new_shipment(order_id):
    sql = "SELECT batchorders.batchorder_id FROM batchorders WHERE batchorders.order_id = :order_id"
    result = db.session.execute(sql, {"order_id": order_id})
    batchorder_ids = result.fetchall()

    if batchorder_ids == None:
        flash("Invalid order id", "danger")
        return False

    user_id = users.get_user_id()

    inserts = []

    for id in batchorder_ids:
        insert = {"user_id": user_id,
                  "batchorder_id": id[0],
                  "order_id": order_id}
        inserts.append(insert)

    sql = "INSERT INTO shipments (batchorder_id, user_id, order_id, done, collected) VALUES (:batchorder_id, :user_id, :order_id, NOW(), TRUE)"
    db.session.execute(sql, inserts)
    db.session.commit()
    flash("Order %s completed" % order_id, "success")
    return True

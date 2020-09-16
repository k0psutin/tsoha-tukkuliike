from flask.helpers import flash
from db import db
from datetime import date
import users
import item


def get_all_batches():
    sql = """SELECT batch_nr, items.itemname, batches.qty, date
             FROM batches
             INNER JOIN items ON (batches.item_id = items.item_id)
             WHERE qty > 0"""
    result = db.session.execute(sql)
    return result.fetchall()


def check_if_batch_exists(batch_nr):
    sql = "SELECT batch_nr FROM batches WHERE batch_nr = :batch_nr"
    result = db.session.execute(sql, {"batch_nr": batch_nr})
    return result.fetchone() != None


def update_order_qty(order_id, updated_qty):
    sql3 = "UPDATE orders SET qty = :updated_qty WHERE order_id = :order_id"
    db.session.execute(
        sql3, {"updated_qty": updated_qty, "order_id": order_id})

    db.session.commit()
    return 0


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
    if qty < 0:
        flash("Negative quantity is not allowed.")
        return 0

    order = get_supply_order_by_id(order_id)

    if order == None:
        flash("Order %s does not exist." % order_id)
        return 0

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
        update_order_qty(order_id, updated_qty)
        flash("Batch %s updated succesfully." % batch_nr)
        return 0

    order_qty = int(order[4])
    updated_qty = order_qty - qty

    if updated_qty < 0:
        flash("You're trying to move more items than we have ordered.")
        return 0

    user_id = users.get_user_id()
    sql2 = """INSERT INTO batches (batch_nr, company_id, item_id, qty, date, user_id)
             VALUES (:batch_nr, :company_id, :item_id, :qty, :now, :user_id)"""

    db.session.execute(sql2, {
                       "batch_nr": batch_nr, "company_id": order[0], "item_id": order[1], "qty": qty, "now": order[5], "user_id": user_id})

    sql3 = "UPDATE orders SET qty = :updated_qty WHERE order_id = :order_id"
    db.session.execute(
        sql3, {"updated_qty": updated_qty, "order_id": order_id})

    db.session.commit()
    flash("Batch %s created succesfully." % batch_nr)


def add_batch_qty(batch_nr, qty):
    qty = int(qty)
    sql = "SELECT qty FROM batches WHERE batch_nr = :batch_nr"
    result = db.session.execute(sql, {"batch_nr": batch_nr})
    validate_qty = int(result.fetchone()[0])
    result_qty = validate_qty + qty

    if result_qty < 0:
        flash("Negative batch qty is not allowed.")
        return 0

    sql = "UPDATE batches SET qty = (batches.qty+:qty) WHERE batch_nr = :batch_nr"
    db.session.execute(sql, {"qty": qty, "batch_nr": batch_nr})
    db.session.commit()


def add_batchorder_qty(batchorder_id, qty):
    qty = int(qty)
    sql = "SELECT qty FROM batchorders WHERE batchorder_id = :batchorder_id"
    result = db.session.execute(sql, {"batchorder_id": batchorder_id})
    validate_qty = result.fetchone()[0]
    result_qty = validate_qty + qty

    if result_qty < 0:
        flash("Negative stock is not allowed.")
        return 0

    sql = "UPDATE batchorders SET qty = (batchorders.qty + :qty) WHERE batchorder_id = :batchorder_id"
    db.session.execute(sql, {"qty": qty, "batchorder_id": batchorder_id})
    db.session.commit()


def collect_to_batchorder(order_id, qty, batch_nr):
    qty = int(qty)

    if qty < 0:
        flash("Negative quantity is not allowed.")
        return 0

    sql = """SELECT batches.item_id,
                    orders.item_id
             FROM batches
             INNER JOIN orders ON (batches.item_id = orders.item_id)
             WHERE batch_nr = :batch_nr and order_id = :order_id"""

    result = db.session.execute(
        sql, {"order_id": order_id, "batch_nr": batch_nr})
    valid_order = result.fetchall()

    if len(valid_order) == 0:
        flash("This item doesn't belong to this order.")
        return 0

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
            flash("Collected quantity exceeds remaining quantity.")
            return 0

        item_id = item.get_itemid_by_batchnr(batch_nr)
        sql = "INSERT INTO batchorders (order_id, item_id, batch_nr, qty) VALUES (:order_id, :item_id, :batch_nr, :qty)"
        db.session.execute(
            sql, {"order_id": order_id, "qty": qty, "batch_nr": batch_nr, "item_id": item_id})
        db.session.commit()
        new_qty = qty * -1
        add_batch_qty(batch_nr, new_qty)
    else:
        valid_qty = batchorder[2]
        if qty > valid_qty:
            flash("Collected quantity exceeds remaining quantity.")
            return 0

        add_batchorder_qty(batchorder[0], qty)
        new_qty = qty * -1
        add_batch_qty(batch_nr, new_qty)


def create_new_shipment(order_id):
    sql = "SELECT batchorders.batchorder_id FROM batchorders WHERE batchorders.order_id = :order_id"
    result = db.session.execute(sql, {"order_id": order_id})
    batchorder_ids = result.fetchall()

    print(batchorder_ids)

    if batchorder_ids == None:
        flash("Error happened.")
        return 0

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

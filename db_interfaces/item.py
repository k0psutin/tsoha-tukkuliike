from flask.helpers import flash
from flask import session
from db_interfaces.db import db


def item_page_count():
    sql = "SELECT COUNT(*) FROM items"
    result = db.session.execute(sql)
    pages = result.fetchone()[0]
    if pages == None:
        return 0
    return int(pages) / 10


def add_item(itemname, price):
    if float(price) <= 0:
        flash("Price must be larger than zero", "danger")
        return 0

    if len(itemname) < 3:
        flash("Item name must be longer than two characters", "danger")
        return 0

    if get_item_by_name(itemname) != None:
        flash("Item named %s already exists" % itemname, "danger")
        return 0

    sql = "INSERT INTO items (itemname, price) VALUES (:itemname, :price)"
    db.session.execute(sql, {"itemname": itemname, "price": price})
    db.session.commit()
    flash("Added new item %s" % itemname, "success")


def get_item_by_id(item_id):
    sql = "SELECT * FROM items WHERE item_id = :item_id"
    result = db.session.execute(sql, {"item_id": item_id})
    return result.fetchone()


def get_item_by_name(itemname):
    sql = "SELECT item_id FROM items WHERE LOWER(itemname)=:itemname"
    result = db.session.execute(sql, {"itemname": itemname.lower()})
    return result.fetchone()


def get_price(item_id):
    sql = "SELECT price FROM items WHERE item_id=:item_id"
    result = db.session.execute(sql, {"item_id": item_id})
    return result.fetchone()[0]


def get_all_items():
    row_count = session["row_count"]
    offset = session["item"] * 10
    result = db.session.execute(
        "SELECT * FROM items LIMIT :row_count OFFSET :offset", {"row_count": row_count, "offset": offset})
    return result.fetchall()


def close_item(item_id):
    sql = "UPDATE items SET closed = TRUE WHERE item_id = :item_id"
    db.session.execute(sql, {"item_id": item_id})
    db.session.commit()


def open_item(item_id):
    sql = "UPDATE items SET closed = FALSE WHERE item_id = :item_id"
    db.session.execute(sql, {"item_id": item_id})
    db.session.commit()


def get_itemid_by_batchnr(batch_nr):
    sql = "SELECT item_id FROM batches WHERE batch_nr = :batch_nr"
    result = db.session.execute(sql, {"batch_nr": batch_nr})
    return result.fetchone()[0]

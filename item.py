from flask.helpers import flash
from db import db


def add_item(itemname, price):
    if int(price) < 0:
        flash("Price can't be a negative value.")
        return 0

    if len(itemname) < 3:
        flash("Item name is too short.")
        return 0

    if get_item_by_name(itemname) != None:
        flash("Item named %s already exists." % itemname)
        return 0

    sql = "INSERT INTO items (itemname, price) VALUES (:itemname, :price)"
    db.session.execute(sql, {"itemname": itemname, "price": price})
    db.session.commit()
    flash("Added new item %s" % itemname)


def get_item_by_name(itemname):
    sql = "SELECT item_id FROM items WHERE LOWER(itemname)=:itemname"
    result = db.session.execute(sql, {"itemname": itemname.lower()})
    return result.fetchone()


def get_price(item_id):
    sql = "SELECT price FROM items WHERE item_id=:item_id"
    result = db.session.execute(sql, {"item_id": item_id})
    return result.fetchone()[0]


def get_all_items():
    result = db.session.execute("SELECT * FROM items")
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

from flask.helpers import flash
from flask import session
from db_interfaces.db import db
import db_interfaces.item as item
import db_interfaces.users as users


def get_all_sales_by_company_id(company_id):
    sql = """SELECT MAX(orders.order_id),
                    MAX(orders.company_id),
                    companies.compname,
                    MAX(orders.orderdate),
                    SUM(orders.qty) AS qty,
                    MAX(companies.route)
             FROM orders
             INNER JOIN companies ON (orders.company_id = companies.company_id)
             WHERE orders.supply = false AND orders.company_id = :company_id
             GROUP BY companies.compname, orders.orderdate
             ORDER BY orders.orderdate"""

    result = db.session.execute(sql, {"company_id": company_id})
    orders = result.fetchall()
    return orders


def get_order_date(order_id):
    sql = "SELECT TO_CHAR(orderdate :: DATE, 'dd Month, yyyy') FROM orders WHERE order_id = :order_id"
    result = db.session.execute(sql, {"order_id": order_id})
    order = result.fetchone()
    return order


def get_sale_order(order_id):
    sql = """SELECT orders.item_id,
                    items.itemname,
	                orders.qty AS required,
	                (SELECT COALESCE(SUM(qty),0)
	                 FROM batchorders
	                 WHERE batchorders.item_id = orders.item_id
	                 AND order_id = :order_id) AS collected_qty,
	            	orders.qty - (SELECT COALESCE(SUM(qty),0)
	                              FROM batchorders
	                              WHERE batchorders.item_id = orders.item_id
	                              AND order_id = :order_id) AS remaining_qty,
                     orders.price
              FROM orders
              INNER JOIN items ON (orders.item_id = items.item_id)
              WHERE order_id = :order_id;"""

    result = db.session.execute(sql, {"order_id": order_id})
    orders = result.fetchall()

    return orders


def get_all_sale_orders(show_all=False):
    row_count = session["row_count"]
    offset = session["sale"] * 10
    if show_all == False:
        sql = """SELECT MAX(orders.order_id),
                    MAX(orders.company_id),
                    companies.compname,
                    MAX(orders.orderdate),
                    SUM(orders.qty) AS qty,
                    MAX(companies.route)
             FROM orders
             INNER JOIN companies ON (orders.company_id = companies.company_id)
             WHERE orders.supply = false AND qty > 0 AND orders.order_id
             NOT IN (SELECT shipments.order_id FROM shipments)
             GROUP BY companies.compname, orders.orderdate
             ORDER BY orders.orderdate LIMIT :row_count OFFSET :offset"""
    else:
        sql = """SELECT MAX(orders.order_id),
                    MAX(orders.company_id),
                    companies.compname,
                    MAX(orders.orderdate),
                    SUM(orders.qty) AS qty,
                    MAX(companies.route)
             FROM orders
             INNER JOIN companies ON (orders.company_id = companies.company_id)
             WHERE orders.supply = false AND qty > 0
             GROUP BY companies.compname, orders.orderdate
             ORDER BY orders.orderdate LIMIT :row_count OFFSET :offset"""

    result = db.session.execute(
        sql, {"row_count": row_count, "offset": offset})
    sale_order_list = result.fetchall()

    return sale_order_list


def get_order_total(order_id):
    sql = "SELECT SUM(orders.price * orders.qty) FROM orders WHERE order_id = :order_id"
    result = db.session.execute(sql, {"order_id": order_id})
    return result.fetchone()[0]


def remove_item_from_sale_order(item_id, order_id):
    sql = "DELETE FROM orders WHERE item_id = :item_id AND order_id = :order_id"
    db.session.execute(sql, {"item_id": item_id, "order_id": order_id})
    db.session.commit()


def add_item_to_sale_order(order_id, company_id, item_id, qty):
    sql = "SELECT qty FROM orders WHERE order_id = :order_id AND item_id = :item_id AND company_id = :company_id"
    result = db.session.execute(
        sql, {"order_id": order_id, "item_id": item_id, "company_id": company_id})
    sale = result.fetchone()
    qty = int(qty)

    if sale == None:
        sql = """INSERT INTO orders (order_id, company_id, item_id, supply, orderDate, dispatchDate, qty, price, user_id)
             VALUES (:order_id, :company_id, :item_id, FALSE, NOW(), NOW() + INTERVAL '1 DAY', :qty, :price, :user_id);"""
        price = round((float(qty) * float(item.get_price(item_id))*1.0), 2)

    else:
        sql = "UPDATE orders SET price = :price, qty = :qty WHERE company_id = :company_id AND item_id = :item_id"
        qty += int(sale[0])
        price = round(float(item.get_price(item_id)) * float(qty), 2)

    user_id = users.get_user_id()

    db.session.execute(
        sql, {"order_id": order_id, "company_id": company_id, "item_id": item_id, "qty": qty, "price": price, "user_id": user_id})
    db.session.commit()


def update_sale_order_item_qty(order_id, item_list, company_id, qty_list):
    sql = "UPDATE orders SET price = :price, qty = :qty WHERE company_id = :company_id AND item_id = :item_id AND order_id = :order_id"

    inserts = []

    for i in range(len(qty_list)):

        if qty_list[i] == '':
            continue

        if qty_list[i] == '0':
            remove_item_from_sale_order(item_list[i], order_id)
            continue

        else:
            price = round(float(item.get_price(
                item_list[i])) * float(qty_list[i]), 2)

            insert = {"order_id": order_id,
                      "company_id": company_id,
                      "item_id": item_list[i],
                      "qty": qty_list[i],
                      "price": price}

            inserts.append(insert)

    if len(inserts) == 0:
        return

    db.session.execute(sql, inserts)
    db.session.commit()


def create_sale_order(order_id, saleList):
    sql = "SELECT order_id FROM orders WHERE order_id = :order_id"
    result = db.session.execute(sql, {"order_id": order_id})
    if order_id == result.fetchone():
        flash("Error occurred.", "danger")
        return False

    sql = """INSERT INTO orders (order_id, company_id, item_id, supply, orderDate, dispatchDate, qty, price, user_id)
             VALUES (:order_id, :company_id, :item_id, FALSE, NOW(), NOW() + INTERVAL '1 DAY', :qty, :price, :user_id);"""

    db.session.execute(sql, saleList)
    db.session.commit()

    return order_id


def get_orders_page_count(supply):
    sql = "SELECT COUNT(*) FROM orders WHERE qty > 0 AND supply = :supply"
    result = db.session.execute(sql, {"supply": supply})
    return result.fetchone()


def get_all_sale_order_page_count(show_all):
    if show_all == False:
        sql = """SELECT MAX(orders.order_id),
                    MAX(orders.company_id),
                    companies.compname,
                    MAX(orders.orderdate),
                    SUM(orders.qty) AS qty,
                    MAX(companies.route)
             FROM orders
             INNER JOIN companies ON (orders.company_id = companies.company_id)
             WHERE orders.supply = false AND qty > 0 AND orders.order_id
             NOT IN (SELECT shipments.order_id FROM shipments)
             GROUP BY companies.compname, orders.orderdate
             ORDER BY orders.orderdate"""
    else:
        sql = """SELECT MAX(orders.order_id),
                    MAX(orders.company_id),
                    companies.compname,
                    MAX(orders.orderdate),
                    SUM(orders.qty) AS qty,
                    MAX(companies.route)
             FROM orders
             INNER JOIN companies ON (orders.company_id = companies.company_id)
             WHERE orders.supply = false AND qty > 0
             GROUP BY companies.compname, orders.orderdate
             ORDER BY orders.orderdate"""

    result = db.session.execute(sql)
    count = result.fetchall()
    return count


def get_all_supply_orders():
    row_count = session["row_count"]
    offset = session["supply"] * 10
    sql = """SELECT orders.order_id, orders.company_id, companies.compname, companies.country, orders.orderdate, orders.item_id, items.itemname, orders.qty
           FROM orders
           INNER JOIN companies ON
           (orders.company_id = companies.company_id)
           INNER JOIN items ON
           (orders.item_id= items.item_id) WHERE orders.supply = TRUE AND orders.qty > 0
           ORDER BY orders.orderdate LIMIT :row_count OFFSET :offset"""

    result = db.session.execute(
        sql, {"row_count": row_count, "offset": offset})
    return result.fetchall()


def create_supply_order(orderList):

    sql = """INSERT INTO orders (order_id, company_id, item_id, supply, orderDate, dispatchDate, qty, price, user_id)
             VALUES (:order_id, :company_id, :item_id, TRUE, NOW(), NOW() + INTERVAL '1 DAY', :qty, :price, :user_id);"""

    db.session.execute(sql, orderList)
    db.session.commit()


def delete_order_by_order_id(order_id):
    sql = "DELETE FROM orders WHERE order_id = :order_id"
    db.session.execute(sql, {"order_id": order_id})
    db.session.commit()
    flash("Order %s removed successfully" % order_id, "success")


def get_company_by_order_id(order_id, supply=False):
    sql = """SELECT companies.compname,
                    companies.address,
                    companies.email,
                    companies.country,
                    companies.company_id
            FROM orders
            INNER JOIN companies ON (companies.company_id = orders.company_id)
            WHERE order_id=:order_id AND supply = :supply"""
    result = db.session.execute(sql, {"order_id": order_id, "supply": supply})
    if result == None:
        flash("Wrong order id.", "danger")
        return 0
    return result.fetchone()

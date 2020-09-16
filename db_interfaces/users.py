from flask import session, flash
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
from db_interfaces.db import db


def get_user_by_name(username):  # TODO lowercase checks etc...
    sql = "SELECT username, pswd, auth_lvl FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    db.session.commit()
    return result.fetchone()


def login(username, password):
    user = get_user_by_name(username)
    if user == None:
        flash("Incorrect username or password")
        return 0
    else:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            session["auth_lvl"] = user[2]
            return 0
        else:
            flash("Incorrect username or password")
            return 0


def create_user(username, password, auth_lvl, company_id=None):
    user = get_user_by_name(username)
    if user != None:
        flash("Username is taken.")
        return 0

    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, pswd, auth_lvl, company_id) VALUES (:username, :pswd, :auth_lvl, :company_id)"
    db.session.execute(
        sql, {"username": username, "pswd": hash_value, "auth_lvl": auth_lvl, "company_id": company_id})
    db.session.commit()


def get_user_id():  # TODO errormessages
    username = session["username"]
    sql = "SELECT user_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]


def get_company_id():  # TODO errormessages
    username = session["username"]
    sql = "SELECT company_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]

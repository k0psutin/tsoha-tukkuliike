from flask import session, flash
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
from db_interfaces.db import db
from getpass import getpass
from app import app


@app.cli.command("init")
def create_user():
    print("<-- Create new user for fresh database -->")
    print("<--         Press CTRL+C to abort      -->")
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    password2 = getpass("Retype password: ")

    if username == '' or password == '' or password2 == '':
        print("Username and/or password is empty. Exiting.")
        quit()

    if len(username) < 4:
        print("Username must be at least 4 charachters long. Exiting.")
        quit()

    if len(password) < 4:
        print("Password must be at least 4 charachters long. Exiting.")
        quit()

    if password != password2:
        print("Passwords doesn't match. Exiting.")
        quit()

    error = create_user(username, password, 6)
    if error == 0:
        print("That username is taken.")
        quit()

    print("User %s created succesfully." % username)
    print("Type 'flask run' to start the application. Exiting.")
    quit()


def get_user_by_name(username):  # TODO lowercase checks etc...
    sql = "SELECT username, pswd, auth_lvl FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_current_user():
    sql = "SELECT user_id, company_id, username, pswd FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": session["username"]})
    return result.fetchone()


def login(username, password):
    user = get_user_by_name(username)
    if user == None:
        flash("User %s does not exist." % username, "danger")
        return False
    else:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            session["auth_lvl"] = user[2]
            session["cart"] = []

            # Keeps track of the current page number

            session["supply"] = 0
            session["sale"] = 0
            session["batch"] = 0
            session["item"] = 0

            # How many rows per page

            session["row_count"] = 10

            # Total pages

            session["supply_page_count"] = 0
            session["batch_page_count"] = 0
            session["sale_page_count"] = 0
            session["item_page_count"] = 0
            return True
        else:
            flash("Incorrect password", "danger")
            return False


def create_user(username, password, validate, auth_lvl, company_id=None):
    user = get_user_by_name(username)
    if user != None:
        flash("Username is taken.", "error")
        return False

    if auth_lvl == 'None' or auth_lvl == 0:
        flash("Enter authorization level (1-6")
        return False

    if len(username) < 4:
        flash("Username must be at least 4 characters long.", "danger")
        return False

    if len(password) < 4:
        flash("Password must be at least 4 characters long.", "danger")
        return False

    if password != validate:
        flash("Passwords doesn't match.", "danger")
        return False

    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, pswd, auth_lvl, company_id) VALUES (:username, :pswd, :auth_lvl, :company_id)"
    db.session.execute(
        sql, {"username": username, "pswd": hash_value, "auth_lvl": auth_lvl, "company_id": company_id})
    db.session.commit()
    flash("User %s created succesfully" % username, "success")


def get_user_id():
    username = session["username"]
    sql = "SELECT user_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]


def get_company_id():
    sql = "SELECT company_id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": session["username"]})
    return result.fetchone()[0]


def get_user_pswd(username=None):
    sql = "SELECT pswd FROM users WHERE username=:username"
    if username is None:
        result = db.session.execute(sql, {"username": session["username"]})
    else:
        result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]


def change_password(old_password, validate, new_password, username=None):
    if validate != new_password:
        flash("Passwords doesn't match!", "danger")
        return False

    if len(new_password) < 4:
        flash("Password must be at least 4 characters long.", "danger")
        return False

    pswd = get_user_pswd(username)

    if check_password_hash(pswd, old_password) == False:
        flash("Old password is wrong", "danger")
        return False

    if username is None:
        username = session["username"]

    hash_value = generate_password_hash(new_password)
    sql = "UPDATE users SET pswd = :password WHERE username = :username"
    db.session.execute(
        sql, {"username": username, "password": hash_value})
    db.session.commit()
    flash("Password changed succesfully", "success")
    return True


def get_all_users():
    sql = "SELECT username FROM users"
    result = db.session.execute(sql)
    return result.fetchall()

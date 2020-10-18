from db_interfaces.db import db
from flask import flash
import re
import security


def create_company(compname, address, email, country, route):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9]+[.][a-z][a-z]+$'

    if re.search(regex, email.lower()) == None:
        flash("Invalid email address", "danger")
        return False

    if len(compname) < 4:
        flash("Company name must be at least 4 characters", "danger")
        return False

    if len(address) < 4:
        flash("Address length must be at least 4 characters", "danger")
        return False

    if len(compname) < 4:
        flash("Company name length must be at least 4 characters", "danger")
        return False

    if len(country) < 2:
        flash("Countrycode length must be at least 2 characters", "danger")

    company = get_company_by_name(compname)

    if company != None:
        flash("Company %s already exists" % compname, "danger")
        return False

    sql = """INSERT INTO 
            companies (compname, address, email, country, route) 
            VALUES (:compname, :address, :email, :country, :route)"""
    db.session.execute(sql, {"compname": compname, "address": address,
                             "email": email, "country": country, "route": route})
    db.session.commit()
    if security.has_auth([4]):
        flash("Company %s added succesfully" % compname, "success")
    else:
        flash("Supplier %s added succesfully" % compname, "success")
    return True


def get_company(company_id):
    sql = "SELECT * FROM companies WHERE company_id=:company_id"
    result = db.session.execute(sql, {"company_id": company_id})
    return result.fetchone()


def get_company_by_name(compname):
    sql = "SELECT * FROM companies WHERE LOWER(compname) = LOWER(:compname)"
    result = db.session.execute(sql, {"compname": compname})
    return result.fetchone()


def get_all_companies():
    sql = "SELECT * FROM companies"
    result = db.session.execute(sql)
    return result.fetchall()

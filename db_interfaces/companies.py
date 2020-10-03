from db_interfaces.db import db


def create_company():
    return None


def get_company(company_id):
    sql = "SELECT * FROM companies WHERE company_id=:company_id"
    result = db.session.execute(sql, {"company_id": company_id})
    return result.fetchone()


def get_all_companies():
    sql = "SELECT * FROM companies"
    result = db.session.execute(sql)
    return result.fetchall()

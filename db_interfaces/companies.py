import db_interfaces.db as db


def create_client():
    return None


def create_supplier():
    return None


def get_company_info(company_id):
    sql = "SELECT * FROM companies WHERE company_id=:company_id"
    result = db.session.execute(sql, {"company_id": company_id})
    return result.fetchone()


def get_all_companies():
    sql = "SELECT * FROM companies"
    result = db.session.execute(sql)
    return result.fetchall()

from flask import session, abort

# 1 - Company
# 2 - Logistics
# 3 - Collector
# 4 - Sales
# 5 - Buyer
# 6 - Controller (admin)


def has_csrf_token(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)


def has_role(auth_levels):
    if session["auth_lvl"] not in auth_levels:
        abort(403)

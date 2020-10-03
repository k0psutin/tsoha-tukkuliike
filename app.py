from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes.auth_router
import routes.logistic_router
import routes.collector_router
import routes.sales_router
import routes.buyer_router
import routes.user_router
import routes.controller_router
import routes.company_router
import routes.cart_router
import routes.page_router
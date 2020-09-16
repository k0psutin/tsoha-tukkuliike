from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

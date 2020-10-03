from flask import request, session
from app import app


@app.route("/next_page", methods=["POST"])
def next_page():
    page = request.form["page"]
    page_count_type = request.form["page_count_type"]
    page_number = int(session[page]) + 1

    if session[page_count_type] == page_number:
        return "OK"

    session[page] = page_number
    return "OK"


@app.route("/prev_page", methods=["POST"])
def prev_page():
    page = request.form["page"]
    page_count_type = request.form["page_count_type"]
    page_number = int(session[page]) - 1

    if session[page_count_type] == page_number:
        return "OK"

    session[page] = page_number
    return "OK"


@app.route("/change_page", methods=["POST"])
def change_page():
    page = request.form["page"]
    page_number = request.form["page_number"]
    page_count_type = request.form["page_count_type"]
    page_number = int(page_number) - 1

    if page_number < 0 or page_number > session[page_count_type]:
        return "OK"

    session[page] = page_number
    return "OK"

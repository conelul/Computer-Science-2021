from db_helper import DBHelper
from flask import Flask, render_template, request
import json
import dateutil.parser as dp
import string
from loguru import logger

app = Flask(__name__)
DB = DBHelper()

categories = ["mugging", "break-in"]


@app.route("/")
def home(error_message=None) -> str:
    crimes = DB.get_all_crimes()
    logger.info("getting all crimes")
    crimes = json.dumps(crimes)
    logger.info("returning rendered home template")
    return render_template(
        "home.html", crimes=crimes, categories=categories, error_message=error_message
    )


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        logger.error(e)
    return home()


@app.route("/clear")
def clear() -> str:
    logger.info("clearing the database")
    try:
        DB.clear_all()
    except Exception as e:
        logger.error(e)
    return home()


@app.route("/submitcrime", methods=["POST"])
def submitcrime() -> str:
    logger.info("getting user form input")
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    description = sanitize_string(request.form.get("description"))
    logger.info(f"adding a new crime to the database")
    DB.add_crime(category, date, latitude, longitude, description)
    return home()


def format_date(userdate: str | None) -> str | None:
    date = dp.parse(userdate)
    logger.info(f"formatting date: {date}")
    try:
        return date.strftime("%Y-%m-%d")
    except TypeError as e:
        logger.error(f"could not format date: {e}")
        return None


def sanitize_string(userinput: str | None) -> str:
    logger.info("santizing description")
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return "".join(list(filter(lambda x: x in whitelist, userinput)))


if __name__ == "__main__":
    app.run(port=8000, debug=True)

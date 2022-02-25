#!/usr/bin/env python3
from flask import Flask, render_template, request
import requests as rq
from datetime import datetime as dt
from loguru import logger

#! API Keys
HISTORICAL_WEATHER_KEY = "a11e1a4352e7dd87433928500b05ee93"

#! API Links
DAY_EVENTS_URL = "https://today.zenquotes.io/api/{}"
IP_INFO_URL = "http://ip-api.com/json/{}"
IP_GET_URL = "https://api.ipify.org/?format=json"
WIKIPEDIA_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={}"
HISTORICAL_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?units={units}&lat={lat}&lon={lon}&appid={key}"


app = Flask(__name__)


def get_location(ip: str) -> list[str]:
    response = rq.get(IP_INFO_URL.format(ip)).json()
    return response


def get_date(id: str) -> dt:
    """Get the date from a form (using the specified method).

    Args:
        id (str): What key/id to look for?

    Returns:
        dt: Returns the date as a datetime in %Y-%m-%d format.
        NOTE: DEFAULTS TO THE CURRENT DATE IF INVALID OR NO DATE PROVIDED.
    """
    date: str | None = request.args.get(id)
    try:  # Try to convert to datetime
        date = dt.strptime(date, "%Y-%m-%d").date()
    except Exception:  # Fall back to the current date if date is invalid or None.
        date = dt.now().date()
    return date


def add_images(data: dict) -> dict:
    """Add image links to the day data dictionary.

    Args:
        data (dict): The entire day data dictionary.

    Returns:
        dict: Returns a new dictionary with image links added.
    """
    titles = []
    for event in data["Events"]:
        try:
            titles.append(event["links"]["1"]["1"].split("/")[-1])
        except KeyError:
            continue
    query = "|".join(titles)
    response = rq.get(WIKIPEDIA_URL.format(query)).json()
    img_links = []
    for _, page in response["query"]["pages"].items():
        try:
           img_links.append(page["original"]["source"])
        except KeyError:
            img_links.append("")
    for i, event in enumerate(data["Events"]):
        try:
            event["links"]["image_link"] = img_links[i]
        except IndexError:
            event["links"]["image_link"] = ""
    return data


def get_historical_data(day: str) -> dict[str, dict[str, list[dict[str, str]]]]:
    """Get historical event data for a given day using the "DAY_EVENTS_URL" link.

    Args:
        day (str): Day to get the historical events for, in (month/day) format.

    Returns:
        dict: Returns the events in dictionary format (from json).
    """
    # Get raw historical event data from the API.
    # NOTE: The API responds with data for the current date if the query/date is invalid.
    response = rq.get(DAY_EVENTS_URL.format(day)).json()

    # Return only the data portion of the response
    return response["data"]


def get_weather(lat: str | int, lon: str | int) -> dict[str, str]:
    """Returns the current weather for lat&lon coordinates"""
    response = rq.get(
        HISTORICAL_WEATHER_URL.format(
            units="imperial", lat=lat, lon=lon, key=HISTORICAL_WEATHER_KEY
        )
    ).json()
    return response


@app.route("/", methods=["GET"])
def index() -> str:
    #! HISTORICAL DATA
    date: dt = get_date("date")
    logger.info(f"Date: {date}")

    day: str = date.strftime(
        "%m/%d"
    )  # Convert %Y-%m-%d to %m/%d format for the events API
    logger.info(f"Day: {day}")

    historical_event_data = add_images(
        get_historical_data(day)
    )  # Get the historical event data for the day
    logger.info("Got historical information and added images")

    #! WEATHER AND LOCATION
    user_ip: str = rq.get(IP_GET_URL).json()["ip"]  # Get the user's IP
    logger.info(f"Got user IP: {user_ip}")

    lctn: dict[str, str | int] = get_location(
        user_ip
    )  # Get user's location based on ip
    str_lctn: str = f"{lctn['city']}, {lctn['countryCode']}"
    logger.info(f"Got user location information from the API: {str_lctn}")

    current_weather = get_weather(lctn["lat"], lctn["lon"])

    #! RETURNING HTML
    logger.info("Rendering and returning the template")
    # Return the rendered html
    return render_template(
        "index.html",
        user_ip=user_ip,
        user_location=str_lctn,
        current_weather=current_weather,
        day=day,
        day_historical_data=historical_event_data,
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)

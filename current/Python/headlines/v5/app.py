#!/usr/bin/env python3
from flask import Flask, render_template, request, make_response
import datetime
import requests
import feedparser as fp

DEFAULTS = {
    "publication": "cnn",
    "city": "Chicago,US",
    "currency_from": "USD",
    "currency_to": "GBP",
}

# API KEYS
WEATHER_API_KEY = "a11e1a4352e7dd87433928500b05ee93"
EXCHANGE_API_KEY = "0410c4e91f794b2281d07ceb262ce07d"

# API LINKS
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}"
EXCHANGE_URL = "https://openexchangerates.org//api/latest.json?app_id={}"

RSS_FEEDS = {
    "fox": "https://moxie.foxnews.com/feedburner/world.xml",
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "cnn": "http://rss.cnn.com/rss/edition_world.rss",
    "fox": "https://moxie.foxnews.com/feedburner/latest.xml",
    "bbc": "http://feeds.bbci.co.uk/news/world/rss.xml",
}


def get_news(query: str) -> list[fp.util.FeedParserDict]:
    """Return news from a given feed

    Args:
        query (str): Which news source to use? Defaults to DEFAULTS["publication"] if not in RSS_FEEDS.

    Returns:
        List of latest news articles from the news source.
    """
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = fp.parse(RSS_FEEDS[publication])
    print(feed)
    return feed["entries"]


def get_weather(location: str, units: str = "imperial") -> dict[str]:
    """Returns weather data for a given location (city).

    Args:
        location (str, optional): City and country of location ("Chicago,US" for example).
        units (str, optional): Which units to use? (standard | metric | imperial). Defaults to "imperial".

    Returns:
        dict[str]: Weather description, temperature, and city/country information for the location.
    """
    resp = requests.get(WEATHER_URL.format(location, units, WEATHER_API_KEY)).json()
    if resp.get("weather"):
        weather = {
            "description": resp["weather"][0]["description"],
            "temperature": resp["main"]["temp"],
            "units": units,
            "city": resp["name"],
            "country": resp["sys"]["country"],
        }
    else:
        weather = {
            "description": "NOT FOUND",
            "temp": "NOT FOUND",
            "city": location,
        }
    return weather


def get_rate(frm: str, to: str) -> tuple[int, list[str]]:
    """Get currency exchange rates.

    Args:
        frm (str):  Currency to convert from.
        to (str): Currency to convert to.

    Returns:
        (rate, currencies): Conversion rate of {frm} to {to}, as well as a list of currencies.
    """
    rates = requests.get(EXCHANGE_URL.format(EXCHANGE_API_KEY)).json().get("rates")
    frm_rate = rates[frm.upper()]
    to_rate = rates[to.upper()]
    return (to_rate / frm_rate, rates.keys())


#! Actual website
app = Flask(
    __name__,
)


@app.route("/", methods=["GET"])
def home():
    # Get headlines
    publication = request.args.get("publication")
    # Use cookie if no publication parameter was passed and the cookie exists, otherwise use the value in DEFAULTS
    if not publication or publication not in RSS_FEEDS.keys():
        publication = request.cookies.get("publication")
        if not publication:
            publication = DEFAULTS["publication"]
    articles = get_news(publication)

    # Get weather data
    city = request.args.get("city")
    # Use cookie if no city parameter was passed and the cookie exists, otherwise use the value in DEF  AULTS
    if not city:
        city = request.cookies.get("city")
        if not city:
            city = DEFAULTS["city"]
    weather = get_weather(city)

    # Get currency data
    currency_from = request.args.get("currency_from")
    # Use cookie if no currency_from parameter was passed and the cookie exists, otherwise use the value in DEFAULTS
    if not currency_from:
        currency_from = request.cookies.get("currency_from")
        if not currency_from:
            currency_from = DEFAULTS["currency_from"]

    currency_to = request.args.get("currency_to")
    # Use cookie if no currency_to parameter was passed and the cookie exists, otherwise use the value in DEFAULTS
    if not currency_to:
        currency_to = request.cookies.get("currency_to")
        if not currency_to:
            currency_to = DEFAULTS["currency_to"]

    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(
        render_template(
            "home.html",
            news_source=publication.upper(),
            articles=articles,
            weather=weather,
            currency_from=currency_from,
            currency_to=currency_to,
            rate=round(rate, 2),  # Round currency rate so you don't have a super long number.
            currencies=sorted(currencies),
        )
    )

    # Cookie expiration date
    expires = datetime.datetime.now() + datetime.timedelta(days=365)

    # Set cookies
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


if __name__ == "__main__":
    app.run(debug=True, ssl_context=("certs/cert.pem", "certs/key.pem"))

#!/usr/bin/env python3
from flask import Flask, render_template, request
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
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "cnn": "http://rss.cnn.com/rss/edition_world.rss",
    "fox": "https://moxie.foxnews.com/feedburner/latest.xml",
    "bbc": "http://feeds.bbci.co.uk/news/world/rss.xml",
}


def get_news(query: str) -> list[fp.util.FeedParserDict]:
    """Return news from a given feed

    Args:
        query (str): Which news source to use? Defaults to DEFAULTS["publication"] if invalid.

    Returns:
        List of latest news articles from the news source.
    """
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = fp.parse(RSS_FEEDS[publication])
    return feed["entries"]


def get_weather(location: str, units: str = "imperial") -> dict[str]:
    """
    Returns weather data for a given location (city).

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
    """Get currency exchange rates

    Args:
        frm (str):  Currency to convert from
        to (str): Currency to convert to

    Returns:
        (rate, currencies): Conversion rate of {frm} to {to}, as well as a list of currencies.
    """
    rates = requests.get(EXCHANGE_URL.format(EXCHANGE_API_KEY)).json().get("rates")
    frm_rate = rates[frm.upper()]
    to_rate = rates[to.upper()]
    return (to_rate / frm_rate, rates.keys())


#! Actual website
app = Flask(__name__,)


@app.route("/", methods=["GET"])
def home():
    # Get headlines
    publication = request.args.get("publication", DEFAULTS["publication"])
    articles = get_news(publication)

    # Get weather data
    city = request.form.get("city", DEFAULTS["city"])
    weather = get_weather(city)

    # Get currency data
    currency_from = request.args.get("currency_from", DEFAULTS["currency_from"])
    currency_to = request.args.get("currency_to", DEFAULTS["currency_to"])
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template(
        "home.html",
        news_source=publication.upper(),
        articles=articles,
        weather=weather,
        currency_from=currency_from,
        currency_to=currency_to,
        rate=round(rate, 2),
        currencies=sorted(currencies),
    )


if __name__ == "__main__":
    app.run(debug=True)

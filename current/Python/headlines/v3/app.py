#!/usr/bin/env python3
from flask import Flask, render_template, request
import feedparser as fp

app = Flask(
    __name__,
)

RSS_FEEDS = {
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "cnn": "http://rss.cnn.com/rss/edition_world.rss",
    "fox": "https://moxie.foxnews.com/feedburner/latest.xml",
    "bbc": "http://feeds.bbci.co.uk/news/world/rss.xml",
}


@app.route("/", methods=["GET", "POST"])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "cnn"
    else:
        publication = query.lower()

    feed = fp.parse(RSS_FEEDS[publication])

    return render_template(
        "news.html", 
        source=f"{publication.upper()} NEWS", 
        articles=feed["entries"]
    )


if __name__ == "__main__":
    app.run(debug=True)

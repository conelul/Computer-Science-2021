#!/usr/bin/env python3
from flask import Flask
import feedparser as fp

# News feeds
NYTIMES_FEED = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"

app = Flask(__name__, instance_relative_config=True)


@app.route("/")
def get_news():
    feed = fp.parse(NYTIMES_FEED)
    first_article = feed["entries"][0]

    return """
    <html>
        <body>
            <h1> New York Times Headlines </h1>
                <b>{0}</b> <br/>
                <i>{1}</i> <br/>
                <p>{2}</p> <br/>
        </body>
    </html>
    """.format(
        first_article.get("title"),
        first_article.get("published"),
        first_article.get("summary"),
    )


if __name__ == "__main__":
    app.run(debug=True)

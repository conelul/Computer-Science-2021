from flask import Flask, render_template
import feedparser as fp

app = Flask(
    __name__,
)

RSS_FEEDS = {
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "cnn": "http://rss.cnn.com/rss/edition_world.rss",
}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="nytimes"):
    feed = fp.parse(RSS_FEEDS[publication])
    return render_template(
        "news.html",
        source=f"{publication} news:".upper(),
        articles=feed["entries"]
    )


if __name__ == "__main__":
    app.run(debug=True)
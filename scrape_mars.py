from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time
import scrape_func

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# scrape app.route 
@app.route("/")
def index():
    mars_news = mongo.db.collection.find_one()
    return render_template("index.html", mars_news=mars_news)


@app.route("/scrape")
def scrape():
    mars_info = scrape_func.scrape()
    mongo.db.collection.drop()
    mongo.db.collection.update({}, mars_info, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

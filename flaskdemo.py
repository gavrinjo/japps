from flask import Flask, render_template, url_for
from bs4 import BeautifulSoup as bs
from requests import get
import re
app = Flask(__name__)

posts = [
    {
        "company": "STUDIO ARTIS d.o.o.",
        "position": "Projektant suradnik(m / ž)",
        "location": "Seget Donji",
        "deadline": "19.09.2018.",
        "href": "https://www.moj-posao.net/Posao/395550/Projektant-suradnik-mz/"
    },
    {
        "company": "Quid Est",
        "position": "Promotor / Prodajni predstavnik (m/ž)",
        "location": "Zagreb",
        "deadline": "27.09.2018.",
        "href": "https://www.moj-posao.net/Posao/393666/Promotor-Prodajni-predstavnik-mz/"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, url_for
from bs4 import BeautifulSoup as bs
from requests import get
import re
app = Flask(__name__)
"""
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
"""

# keyword = input("Input search keyword ->->->->->")
base_url = f"https://www.moj-posao.net/Pretraga-Poslova/?keyword=projektant&area=2&category="

r = get(base_url)
html_soup = bs(r.text, "html.parser")

# Make sure there are more than one page, otherwise, set to 1.
try:
    num_pages = int(re.findall("\d+$", html_soup.find(class_="last icon").a.get("href"))[0])
except AttributeError:
    num_pages = 1

# Build up a URL list
url_list = ["{}&page={}".format(base_url, str(page)) for page in range(1, num_pages + 1)]

# define a dictionary list
posts = []

# define a lists of dictionary items
company_lst = []
position_lst = []
location_lst = []
deadline_lst = []
href_lst = []

# grab items from list of URLs
for url in url_list:
    rp = get(url)
    soup = bs(rp.text, "html.parser")
    for company in soup.find_all(True, {"class": ["job-position", "job-title"]}):
        if company.get("class")[0] == "job-position":
            try:
                company_lst.append(company.parent.parent.parent.a.img.get("title"))
            except AttributeError:
                company_lst.append(company.parent.parent.parent.img.get("title"))
            deadline_lst.append(company.find_next_sibling(class_="deadline").text.strip())
            href_lst.append(company.parent.get("href"))
        else:
            company_lst.append(company.find_next_sibling("p").text.strip())
            deadline_lst.append(company.find_next_sibling(class_="deadline").time.text.strip())
            href_lst.append(company.a.get("href"))
        position_lst.append(company.text.strip())
        location_lst.append(company.find_next_sibling(class_="job-location").text.strip())


# zip dictionary keys wit corresponding values
for a, b, c, d, e in zip(company_lst, position_lst, location_lst, deadline_lst, href_lst):
    posts.append(dict(company=a, position=b, location=c, deadline=d, href=e))



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == "__main__":
    app.run(debug=True)

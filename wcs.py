from bs4 import BeautifulSoup as bs
from requests import get
# from requests.exceptions import RequestException
from contextlib import closing
import json
import re
from datetime import datetime, timedelta


def get_url(src):
    with closing(get(src, stream=True)) as source:
        if response_check(source):
            return source.content
        else:
            log_error(source)


def response_check(check):
    content_type = check.headers["Content-Type"].lower()
    return check.status_code == 200 and content_type is not None


def log_error(error):
    exit(f"ERROR, check your URLs, invalid response code \"{error.status_code}\"")


def url_list():
    url_lst = []
    for page in range(2, 3):
        if page < 22:
            url_lst.append(f"https://burzarada.hzz.hr/rss/rsszup{page}.xml")
        else:
            url_lst.append("https://burzarada.hzz.hr/rss/rsszup1000.xml")
    url_lst.append("https://feeds2.feedburner.com/mojposao")
    return url_lst


def get_data():
    for url in url_list():
        raw_data = get_url(url)
        soup_data = bs(raw_data, "lxml")
        for item in soup_data.find_all("item"):
            if datetime.now() - datetime.strptime(get_pdate(item), "%d.%m.%Y") < timedelta(days=5):
                title = get_title(item)
                pdate = get_pdate(item)
                ddate = get_ddate(item)
                location = get_location(item)
                link = get_link(item)
            else:
                continue
            data.append(dict(Title=title, PubDate=pdate, DueDate=ddate, Location=location, Link=link))
        # return data
        with open('poss.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def get_title(item):
    return item.title.text


def get_pdate(item):
    if "burzarada" in item.guid.text:
        return item.pubdate.text
    else:
        return datetime.strptime(item.pubdate.text, "%a, %d %b %Y %H:%M:%S %z").strftime("%d.%m.%Y")


def get_ddate(item):
    try:
        return re.search(r"(?<=ve: |vu: )(.*)(?=<b|, Mj)", item.description.text)[0]
    except TypeError:
        return None


def get_location(item):
    try:
        return re.search(r"(?<=rada: )(.*)(?=, Op|<)", item.description.text)[0]
    except TypeError:
        return None


def get_link(item):
    return item.guid.text


data = []
get_data()

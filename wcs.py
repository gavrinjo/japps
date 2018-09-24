from bs4 import BeautifulSoup as bs
from requests import get
# from requests.exceptions import RequestException
from contextlib import closing
import json
import re
from datetime import datetime


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
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
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
            title = item.title.text
            if url.find("hzz") > 2:
                pdate = item.pubdate.text
                src = "HZZ"
            else:
                pdate = datetime.strptime(item.pubdate.text, "%a, %d %b %Y %H:%M:%S %z").strftime("%d.%m.%Y")
                src = "MojPosao"
            try:
                ddate = \
                re.search(r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d", item.description.text)[0]
            except TypeError:
                ddate = None
            try:
                local = re.search(r"(?<=Mjesto rada: )(.*)(?=, Op|<)", item.description.text)[0]
            except TypeError:
                local = None
            link = item.guid.text
            data.append(dict(Title=title, Date=pdate, Link=link, Deadline=ddate, Location=local, Izvor=src))
        # return data
        with open('poss.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


# urls = ["https://burzarada.hzz.hr/rss/rsszup", "https://feeds2.feedburner.com/mojposao"]
data = []
get_data()
print(url_list())

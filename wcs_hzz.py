from bs4 import BeautifulSoup as bs
from requests import get
# from requests.exceptions import RequestException
from contextlib import closing
import json
import re


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


def url_list(url):
    url_lst = []
    for i in range(1, 2):
        if i < 22:
            url_lst.append(f"{url}{i}.xml")
        else:
            url_lst.append(f"{url}1000.xml")
    return url_lst


def get_data(src):
    for i in url_list(src):
        raw_data = get_url(i)
        soup_data = bs(raw_data, "lxml")
        for item in soup_data.find_all("item"):
            title = item.title.text
            pdate = item.pubdate.text
            link = item.guid.text
            try:
                cat = re.search(r"(?<=Kategorija: )(.*)(?=, Rok)", item.description.text)[0]
            except TypeError:
                cat = None
            try:
                ddate = re.search(r"(?<=Rok za prijavu: )(.*)(?=, Mjesto)", item.description.text)[0]
            except TypeError:
                ddate = None
            try:
                local = re.search(r"(?<=Mjesto rada: )(.*)(?=, Op)", item.description.text)[0]
            except TypeError:
                local = None
            data.append(dict(Title=title, Date=pdate, Link=link, Category=cat, Deadline=ddate, Location=local))
        # return data
        with open('hzz.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


url = "https://burzarada.hzz.hr/rss/rsszup"
data = []
get_data(url)


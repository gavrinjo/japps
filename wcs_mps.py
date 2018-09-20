from bs4 import BeautifulSoup as bs
from requests import get
import json
import lxml


payload = {"keyword": "projektant", "area": 2, "category": ""}
base_url = "https://www.moj-posao.net/Pretraga-Poslova/"
source = get(base_url, params=payload)
soup = bs(source.text, "lxml")


try:
    num_pages = int((soup.find(class_="last icon").a.get("href")).split("=")[-1])
except AttributeError:
    num_pages = 1


url_list = [f"{source.url}&page={str(page)}" for page in range(1, num_pages + 1)]
data = []


for url in url_list:
    rp = get(url).text
    soup = bs(rp, "lxml")
    for article in soup.find_all("div", class_="job-data"):
        if article.parent.get("class")[0] == "featured-job":
            job_title = article.a.span.text
            job_company = article.parent.a.img.get("title")
            job_location = article.a.span.find_next_sibling().text
            job_deadline = article.a.time.text
        else:
            job_title = article.p.text.strip()
            job_company = article.p.find_next_sibling(class_="job-company").text.strip()
            job_location = article.p.find_next_sibling(class_="job-location").text.strip()
            job_deadline = article.p.find_next_sibling(class_="deadline").time.text.strip()
        data.append(dict(Title=job_title, Company=job_company, Location=job_location, Deadline=job_deadline))


with open('mps.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


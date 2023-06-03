import requests
import datetime
import time
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

crawl_delay = 5
class_name = "PostsTitle-eaTitleDesktopEllipsis"
post_ids_file = "post_ids.txt"

def form_allposts_url(timeframe, date1, date2, limit=2500):
    date1 = date1.strftime("%Y-%m-%d")
    date2 = date2.strftime("%Y-%m-%d")
    return f"https://www.lesswrong.com/allPosts?timeframe={timeframe}&after={date1}&before={date2}&limit={limit}&karmaThreshold=-1000&filter=frontpage"

def form_month_url(year, month):
    date1 = datetime.datetime(year, month, 1) 
    date2 = datetime.datetime(year, month, 1) + relativedelta(months=1)
    return form_allposts_url("monthly", date1, date2)

def get_post_ids(url):
    response = requests.get(url, headers={"User-Agent": "XY"})
    response_text = response.text

    soup = BeautifulSoup(response_text, "html.parser")
    elements = soup.find_all("span", class_=class_name)

    post_ids = []
    for element in elements:
        try:
            post_ids.append(element.find("a")["href"].split("/")[2])
        except Exception:
            pass

    return post_ids


for year in range(2010, 2023):
    for month in range(1, 13):
        time.sleep(crawl_delay)
        post_ids = get_post_ids(form_month_url(2023, month))
        with open(post_ids_file, "a") as f:
            for post_id in post_ids:
                f.write(post_id + "\n")
        print(f"Finished {2023}-{month}")
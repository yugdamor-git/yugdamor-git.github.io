import pip
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
install("bs4")
install("kora")
install("selenium")
install("tqdm")

from kora.selenium import wd
import json
import time
import tqdm
from bs4 import BeautifulSoup
import os
from datetime import datetime
try:
    website_name = "www.thebetterindia.com"
    try:
      os.mkdir(website_name)
      print("website folder created")
    except:
      print("website folder already present")

    now = datetime.now().strftime('%d-%m-%Y')

    try:
      os.mkdir(os.path.join(website_name,now))
      print("date folder created")
    except:
      print("date folder already present")

    final_json_list = []
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_options=opts)
    driver = wd
    url = "https://www.thebetterindia.com/stories/"
    driver.get(url)
    time.sleep(2)
    i = 754
    url = "https://www.thebetterindia.com/stories/page/{}/"
    all_links = []
    final_data = []
    wd.get("https://www.thebetterindia.com/stories/page/1")
    time.sleep(1)
    title = wd.title
    print("scraping url from all pages - STARTED")
    while(title != "Page Not Found - The Better India"):
      i = i + 1
      url_new = url.format(i)
      wd.get(url_new)
      title = wd.title
      soup = BeautifulSoup(wd.page_source)
      #table = soup.find("div",{"class":"elementor-widget-container"}).div
      #print(table)
      all_items = soup.find_all("article")
      #print(all_items)
      for item in all_items:
        post_link = item.find("a").get("href")
        all_links.append(post_link)
    print("scraping url from all pages - DONE")
    print("scraping data from all url - STARTED")
    for link in tqdm(all_links):
      try:
        wd.get(link)
        page_soup = BeautifulSoup(wd.page_source)
        descp = ""
        try:
          descp = page_soup.find("p",{"class":"subtitle"}).text
        except:
          pass
        title = page_soup.find("h1",{"class":"single-post-title entry-title"}).text
        tags = []
        for tag in page_soup.find("li",{"class":"meta-cat"}).find_all("a"):
          tags.append(tag.text)
        img_link = page_soup.find("div",{"class":"thumbnail"}).img.get("src")
        final_data.append({"ContentTitle":title,"Description":descp,"ContentType":"IMAGE","ContentLink":img_link,"ContentOrigin":link,"Tags":tags})
      except:
        print("no data found for {}".format(link))
    print("scraping data from all url - DONE")
date_path = os.path.join(website_name,now)
with open(os.path.join(date_path,"data.json"), "w") as outfile:
    json.dump(all_data, outfile)
except:
    print("There is some issue with script. Contact yugdamor.dev@gmail.com")
    wd.close()
wd.close()

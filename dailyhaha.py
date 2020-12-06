
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
from tqdm import tqdm
from datetime import datetime
from kora.selenium import wd
from bs4 import BeautifulSoup
import time
import json
import os
website_name = "www.dailyhaha.com"
try:
    os.mkdir(website_name)
    print("www.dailyhaha.com folder created")
except:
    print("www.dailyhaha.com folder already exists")

url2 = "https://www.dailyhaha.com/archive/{}"

all_data = []
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# wd = webdriver.Chrome(ChromeDriverManager().install())
# 1293
print("scrapping all links : started")
all_links = []
i =0
wd.get("https://www.dailyhaha.com/archive/1")
while(wd.title != "404"):
    try:
        i = i + 1
        wd.get(url2.format(i))
        soup = BeautifulSoup(wd.page_source,features="lxml")
        for i in soup.find_all("a",{"class","item gif"}):
            all_links.append(i.get("href"))
        for i in soup.find_all("a",{"class","item picture"}):
            all_links.append(i.get("href"))
    except:
        pass
print("scrapping all links : done")

for link in tqdm(all_links):
    try:
        wd.get(link)
        item_soup = BeautifulSoup(wd.page_source,features="lxml")
        category = item_soup.find("div",{"class":"category"}).a.text
        type_content = ""
        type_of_content = item_soup.find("div",{"class":"single"}).figure.get("class")[0]
        link_content = ""
        title = item_soup.find("div",{"class":"h1d"}).h1.text
        if type_of_content == "picture-view":
          type_content = "IMAGE"
          link_content = "https://www.dailyhaha.com{}".format(item_soup.find("div",{"class":"picholder"}).img.get("src"))
        if type_of_content == "gif-view":
          type_content = "VIDEO"
          link_content = "https://www.dailyhaha.com{}".format(item_soup.find("div",{"class":"gifholder"}).find("source").get("src"))
        all_data.append({"ContentTitle":title,"Description":"","ContentType":type_content,"ContentLink":link_content,"Tags":[category]})
    except:
        pass
now = datetime.now().strftime('%d-%m-%Y')

try:
    date_path = os.path.join(website_name,now)
    os.mkdir(date_path)
    print("date folder created : {}".format(now))
except:
    print("date folder already present : {}".format(now))


with open(os.path.join(date_path,"data.json"), "w") as outfile:
    json.dump(all_data, outfile)



import pip
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
install("bs4")
install("kora")
install("selenium")
from kora.selenium import wd
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
import os
from datetime import datetime
website_name = "www.animalsinfluence.com"
try:
  os.mkdir(website_name)
  print("website folder created")
except:
  print("website folder already present")

now = datetime.now().strftime('%d-%m-%Y')

try:
  os.mkdir(os.path.join(website_name,now))
  print("date folder already created")
except:
  print("date folder already present")

final_json_list = []
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_options=opts)
driver = wd
url = "https://www.animalsinfluence.com/"

driver.get(url)

time.sleep(2)
try:
  tags = driver.find_element_by_id("portfolio-filter").find_elements_by_tag_name("li")
  list_tag = [i.text for i in tags]
  for index,tag in enumerate(list_tag):
    if index >=1:
      driver.get(url)
      time.sleep(2)
      tags = driver.find_element_by_id("portfolio-filter").find_elements_by_tag_name("li")
      tag_ele = tags[index]
      driver.execute_script("return arguments[0].scrollIntoView(true);", tag_ele)
      driver.execute_script("arguments[0].click();", tag_ele)
      tag_name = tag.strip()
      print("Scraping : ",tag_name)
      see_more = driver.find_elements_by_id("btn-next-page")

      # print(len(see_more))

      try:
          for i in range(0,50):
              see_more[0].click()
              time.sleep(1)
      except:
          try:
              for i in range(0,50):
                  see_more[1].click()
                  time.sleep(1)
          except:
              try:
                  for i in range(0,50):
                      see_more[2].click()
                      time.sleep(1)
              except:
                  try:
                    for i in range(0,50):
                      see_more[3].click()
                      time.sleep(1)
                  except:
                    soup = BeautifulSoup(driver.page_source)
                    portfolio1 = soup.find("div",{"id":"portfolio"})
                    all_items = portfolio1.find_all("div",{"class":"grid-item portfolio-item"})
                    all_raw_links=[]
                    for i in all_items:
                        link = i.find("img").get("src").split("/")[-2]
                        title = i.find("h4",{"class":"modal-title"}).text.strip()
                        #print(link)
                        link2 = "https://youtu.be/{}".format(link)
                        final_json_list.append({"ContentTitle":title,"Description":"","ContentType":"VIDEO","ContentLink":link2,"Category":tag_name,"Tags":[tag_name]})

                    portfolio2 = soup.find("div",{"id":"portfolio2"})
                    all_items = portfolio2.find_all("div",{"class":"grid-item portfolio-item"})
                    for i in all_items:
                        link = i.find("img").get("src").split("/")[-2]
                        title = i.find("h4",{"class":"modal-title"}).text.strip()
                        #print(link)
                        link2 = "https://youtu.be/{}".format(link)
                        final_json_list.append({"ContentTitle":title,"Description":"","ContentType":"VIDEO","ContentLink":link2,"Category":"Most Viral","Tags":[tag_name]})

                    portfolio3 = soup.find("div",{"id":"portfolio3"})
                    all_items = portfolio3.find_all("div",{"class":"grid-item portfolio-item"})
                    for i in all_items:
                        link = i.find("img").get("src").split("/")[-2]
                        title = i.find("h4",{"class":"modal-title"}).text.strip()
                        #print(link)
                        link2 = "https://youtu.be/{}".format(link)
                        final_json_list.append({"ContentTitle":title,"Description":"","ContentType":"VIDEO","ContentLink":link2,"Category":"Animal Friends","Tags":[tag_name]})

                    portfolio4 = soup.find("div",{"id":"portfolio4"})
                    all_items = portfolio4.find_all("div",{"class":"grid-item portfolio-item"})
                    for i in all_items:
                        link = i.find("img").get("src").split("/")[-2]
                        title = i.find("h4",{"class":"modal-title"}).text.strip()
                        #print(link)
                        link2 = "https://youtu.be/{}".format(link)
                        final_json_list.append({"ContentTitle":title,"Description":"","ContentType":"VIDEO","ContentLink":link2,"Category":"Cute Eaters","Tags":[tag_name]})

  path = os.path.join(website_name,now)
  path2 = os.path.join(path,"data.json")
  with open(path2, "w") as outfile:
      json.dump(final_json_list, outfile)
except:
  print("There is some issue with script . \n Contact me @ yugdamor.dev@gmail.com")

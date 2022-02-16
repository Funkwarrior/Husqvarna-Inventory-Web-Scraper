# import libraries
import urllib.request
from selenium import webdriver
import time
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup as soup
from numpy import product
import requests
import ftfy
import pandas as pd
from soupsieve import select_one

# specify the url


urlpage = 'https://www.husqvarna.com/it/motoseghe/120-mark-ii/' 
# run firefox webdriver from executable path of your choice
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# get web page
driver.get(urlpage)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(10)




def retrieve_product_info(page):
  product_name = page.find("h1").text
  product_price = page.select(".hbd-product-aside__container  div.hui-box")
  #product_image = page.find("picture", {"class": "hui-picture--block"}, srcset=True).get('srcset')
 # print(product_price)
  
product_soup = soup((driver.page_source), "html.parser")

with open('ex_prod.html', 'w') as f:
  f.write(str(product_soup))
#print(retrieve_product_info(product_soup))
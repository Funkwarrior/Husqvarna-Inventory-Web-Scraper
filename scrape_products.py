#!/usr/bin/python
from lxml import html
from bs4 import BeautifulSoup
from numpy import product
import requests
import ftfy
import pandas as pd
from soupsieve import select_one

base_url="https://www.husqvarna.com/it/motoseghe/"
 # opens the connection and downloads html page from url
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}

def import_links_from_excel():
  df = pd.read_excel('urls.xlsx')
  #df = df.reset_index()
  for index, row in df.iterrows():
      index

def scan_for_products_link(page):
  products_links = {}
  product_type = page.find("h1").text
  products = page.find("div", {"class": "hui-grid__grid-lg-9"}).findAll("a", {"class": "hbd-link"})

  for item in products:
    if item.find('h4') is not None:
      product_link = item.get('href')
      product_name = ftfy.fix_text(item.find("h4").text)
      products_links[product_name] = product_link
  return products_links

with open('ex_prodcat.html', 'r') as f:
  content = f.read()
  page = BeautifulSoup(content, 'html.parser')
 # print(scan_for_products_link(page))
f.close()


def retrieve_product_info(page):
  product_name = page.select_one("h1").text
  product_price = page.select_one(".hbd-product-aside__container div.hui-box > div > div > span:first-child").text.replace("€", "")
  product_image = page.select_one("source", {"class": "hui-picture--block > source"},  attrs = {'srcset' : True})
  print(list(product_image))
  product_image = product_image.split(',')
  high_resolution_pair = product_image[-1].split(' ')
  high_resolution_image_url = high_resolution_pair[1].replace("@2x", "@3x")
  print(high_resolution_image_url)

with open('ex_prod.html', 'r') as f:
  content = f.read()
  page = BeautifulSoup(content, 'html.parser')
  retrieve_product_info(page)
f.close()

#product_soup = BeautifulSoup(requests.get("https://www.husqvarna.com/it/motoseghe/120-mark-ii/", headers=headers).text, "html.parser")

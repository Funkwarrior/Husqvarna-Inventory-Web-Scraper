#!/usr/bin/python
from lxml import html
from bs4 import BeautifulSoup as soup
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
      print(row[index])

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
  page = soup(content, 'html.parser')
 # print(scan_for_products_link(page))
f.close()


def retrieve_product_info(page):
  product_name = page.find("h1").text
  product_price = page.select(".hbd-product-aside__container  div.hui-box")
  #product_image = page.find("picture", {"class": "hui-picture--block"}, srcset=True).get('srcset')
 # print(product_price)

with open('ex_prod.html', 'r') as f:
  content = f.read()
  page = soup(content, 'html.parser')
 # print(retrieve_product_info(page))
f.close()

#product_soup = soup(requests.get("https://www.husqvarna.com/it/motoseghe/120-mark-ii/", headers=headers).text, "html.parser")

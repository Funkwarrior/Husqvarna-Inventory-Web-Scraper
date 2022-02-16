#!/usr/bin/python
from lxml import html
from bs4 import BeautifulSoup as soup
import requests
import ftfy
import pandas as pd

products_link = []

def scan_for_product_link(page):
  product_type = page.find("h1").text
  products = page.find("div", {"class": "hui-grid__grid-lg-9"}).findAll("a", {"class": "hbd-link"})

  for product in products:
    if product.find('h4') is not None:
      product_name = product.find('h4').text
      product_link = product.get('href')
      products_link = {
        'type': product_type,
        'name': ftfy.fix_text(product_name),
        'link': str(product_link)
      }


  print(products_link)

with open('ex_prodcat.html', 'r') as f:
  content = f.read()
  page = soup(content, 'html.parser')
  scan_for_product_link(page)
f.close()

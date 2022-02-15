#!/usr/bin/python
from lxml import html
from bs4 import BeautifulSoup as soup
import requests
import ftfy
import pandas as pd


with open('ex_prodcat.html', 'r') as f:

    content = f.read()
    page = soup(content, 'html.parser')
    type = page.find("h1").text

    products = page.find("div", {"class": "hui-grid__grid-lg-9"}).findAll("a", {"class": "hbd-link"})
    for product in products:
      if product.find('h4') is not None:
        product_name = product.find('h4').text
        product_link = product.get('href')
      # prints the dataset to console
        print("name: " + ftfy.fix_text(product_name))
        print("link: " + str(product_link))
        # writes the dataset to file
    # f.write(product_name + ", " + article_number.replace(",", "|") + ", " + price + imglink +"\n")
f.close()

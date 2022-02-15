#!/usr/bin/python
from lxml import html
from bs4 import BeautifulSoup as soup  
import requests

with open('/Users/funkwarrior/Python/Husqvarna-Inventory-Web-Scraper/ex_prodcat.html', 'r') as f:

    contents = f.read()
    page = soup(contents, 'html.parser')
    containers = page.findAll("div", {"class": "hui-grid__grid-lg-9"})

    for container in containers
        product_name = container.h4
        product_link = container.find("a", {"class": "hbd-link"}).get('href')
        # prints the dataset to console
      #  print("name: " + product_name.string() + " link: " + product_link.string())

        # writes the dataset to file
    # f.write(product_name + ", " + article_number.replace(",", "|") + ", " + price + imglink +"\n")

f.close()  

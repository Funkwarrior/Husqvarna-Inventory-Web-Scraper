#!/usr/bin/python

from bs4 import BeautifulSoup as soup
from lxml import html
import requests
import scrape_products as sp


# my_url = input("Please enter the url \n >: ")
base_url="https://www.husqvarna.com/it/motoseghe/"
 # opens the connection and downloads html page from url
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}
# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(requests.get(my_url, headers=headers).text, "html.parser")

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "hui-grid__grid-lg-9"})

# name the output file to write to local disk
# out_filename = "files.csv"
# header of csv file to be written
# headers = "product_name,article_number,price,imagelink \n"

# opens file, and writes headersshipping
# f = open(out_filename, "w")
# f.write(headers)

# loops over each product and grabs attributes about
# each product
for container in containers:

    product_name = container.find("h4"})
    product_link = container.find("a", {"class": "hbd-link"})

    # all span with the class "price".
    # Then cleans the text of white space with strip()
    # Cleans the strip of "Shipping $" if it exists to just get number
    price = container.findAll("span", {"class": "price"})[0].text.strip().replace("$", "")


    # Finds image container
    # save image source as a strink
    # removes the first "//" from the link
    image = container.div.div.div.div.div.div.a.picture.img
    imagelink = image['srcset']
    imglink = imagelink[2:]

    # prints the dataset to console
    print("name: " + product_name + "\n")
    print("article: " + article_number + "\n")
    print("price: " + price + "\n")
    print("image link: " + imglink + "\n")

    # writes the dataset to file
    f.write(product_name + ", " + article_number.replace(",", "|") + ", " + price + imglink +"\n")

f.close()

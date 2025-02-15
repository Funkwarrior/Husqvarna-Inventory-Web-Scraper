from xmlrpc.client import Boolean
import requests
from requests_html import HTMLSession
import pandas as pd
from bs4 import BeautifulSoup
from skimage.io import imread, imsave
from skimage.color import rgba2rgb
from skimage import img_as_ubyte
import numpy as np
import os
import jmespath
import ftfy
import json
from itertools import chain
import pandas as pd
from io import BytesIO
from styleframe import StyleFrame
import re
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

baseurl = "https://www.husqvarna.com"
HVA_graphql = "https://www.husqvarna.com/hbd/graphql"

language = "it"

proxy_list = ['62.94.192.101:1080',
              '93.150.57.242:1088',
              '185.78.16.76:5678',
              '85.37.149.178:1088',
              '185.132.228.226:4145',
              '188.95.20.139:5678',
              '94.101.55.201:4153',
              '213.82.192.26:1088',
              '93.64.244.34:1088',
              '81.174.11.159:43516',
              '151.22.181.212:8080',
              '2.228.124.218:8080',
              '31.199.12.150:80',
              '185.47.230.232:80']

headers = {
    'authority': 'www.husqvarna.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'dnt': '1',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'accept': '*/*',
    'origin': 'https://www.husqvarna.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.husqvarna.com',
    'accept-language': 'en-GB,en;q=0.9,it-IT;q=0.8,it;q=0.7,en-US;q=0.6',
    'cookie': 'sessionid=vq1dc4henrngbo1v1tmppumo; hsqglobal#lang=it-IT; ASP.NET_SessionId=q3xq25km0fovv1f5fnpeldcz; SC_ANALYTICS_GLOBAL_COOKIE=68f29e1e7f704e90805b059c6353b096|False; OptanonAlertBoxClosed=2022-02-10T13:05:36.776Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+21+2022+17%3A17%3A07+GMT%2B0100+(Central+European+Standard+Time)&version=6.29.0&isIABGlobal=false&hosts=&consentId=59065fbc-8362-47f7-9fc9-7117155d9e71&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0001%3A1&geolocation=IT%3B36&AwaitingReconsent=false',
}

VAT = float(0.22)
danea_codfornitore = "0042"
danea_produttore = "Husqvarna"
danea_imagepath = "C:\\Users\\funkwarrior\\Pictures\\HVA_images\\"
danea_importGrossPrice = Boolean(True)
image_path = "HVA_images"
categories = []
products_links = []
product = []

def get_product_details():
  get_categories()
  scan_for_products_link()
#  products_links = ['https://www.husqvarna.com/it/motoseghe/535i-xp/']
  start = "createElement(ProductDetails, "
  end = "), document.getElementById("

  for i in range(len(products_links)):
    try:
      product_session = HTMLSession()
      product_response = product_session.get(products_links[i], headers=headers)
    except requests.exceptions.RequestException as e:
      logging.error("Session error {a}".format(a=e))

    time.sleep(1.5)

    script_css = 'script:contains("ProductDetails")'
    script_text = product_response.html.find(script_css, first=True)
    script_content = script_text.text
    json_dirty = script_content[script_content.find(start)+len(start):script_content.rfind(end)].strip() #get the token out the html

    json_clean = json.loads(json_dirty)

    p_specs = []
    p_specs_data = jmespath.search("initialData.site.products.get.articles[0].specificationValues", json_clean)
    p_name = jmespath.search("initialData.site.products.get.name.longName", json_clean)
    p_sku = jmespath.search("initialData.site.products.get.sku", json_clean)
    p_url = jmespath.search("initialData.site.products.get.url", json_clean)
    p_cat = jmespath.search("initialData.site.products.get.category.name", json_clean)
    p_subcat = jmespath.search("initialData.site.products.get.subCategories[0].name", json_clean)
    p_id = jmespath.search("initialData.site.products.get.articles[0].id", json_clean)
    p_desc = jmespath.search("initialData.site.products.get.articles[0].introductionText", json_clean)
    p_normalPrice, p_offerPrice = get_prices(p_id)
    p_image = jmespath.search("initialData.site.products.get.articles[0].mainImage.sources[7].url", json_clean)
    if p_image is None:
      p_image = jmespath.search("initialData.site.products.get.articles[0].studioImages[0].sources[7].url", json_clean)

    logging.info("Getting price of {a} (Normal Net: {b} | Offer Net: {c})".format(a=p_name, b=p_normalPrice, c=p_offerPrice))

    for i in range(len(p_specs_data)):
      if p_specs_data[i].get("formattedValue") is not None:
        p_specs.append(
          p_specs_data[i]["specificationDefinitions"]["name"] + " " +
          p_specs_data[i]["formattedValue"]
        )

    img_name = p_id + "-" + re.sub(r"\W+|-", "_", p_name )+ '.jpg'

    product.append({
      "p_name" : p_name,
      "p_sku" : p_sku,
      "p_url" : baseurl+p_url,
      "p_cat" : p_cat,
      "p_subcat" : p_subcat,
      "p_id" : p_id,
      "p_desc" : "\n".join(p_specs) + "\n" + p_desc,
      "p_image" : danea_imagepath + img_name,
      "p_normalPrice" : p_normalPrice,
      "p_offerPrice" : p_offerPrice,
    })

    if p_image is not None: save_image(p_name, img_name, p_image)

  return product


def save_image(p_name, img_name, p_image):
    os.makedirs(image_path, exist_ok=True)

    img_data = imread(BytesIO(requests.get(p_image).content))
    imsave(f"{image_path}/{img_name}", (img_as_ubyte(rgba2rgb(img_data), (1,1,1))))

    logging.info("Saving {a} image with name {b}".format(a=p_name, b=img_name))

def get_categories():
  try:
    s = HTMLSession()
    r = s.get(baseurl+"/"+language, headers=headers)
  except requests.exceptions.RequestException as e:
    print(e)

  page = BeautifulSoup(r.content, "html.parser")
  links = page.select("a:-soup-contains('Gamma completa')")

  for link in links:
    categories.append(baseurl+link['href'])
    logging.info("Get categories link of {a}: {b}".format(a=link.text.strip(), b=baseurl+link['href']))

  return categories


def scan_for_products_link():

  for products in categories:
    try:
      products_session = HTMLSession()
      products_response = products_session.get(products, headers=headers)
    except requests.exceptions.RequestException as e:
      print(e)

    category_page = BeautifulSoup(products_response.content, 'html.parser')
    product_type = category_page.find("h1").text
    products_pages = category_page.find("div", {"class": "hui-grid__grid-lg-9"}).findAll("a", {"class": "hbd-link"})

    for item in products_pages:
      if item.find('h4') is not None:
        product_link = baseurl + item.get('href')
        product_name = ftfy.fix_text(item.find("h4").text)
        products_links.append(product_link)

        logging.info("Getting product link of {a}".format(a=product_name))

    time.sleep(1.5)


  return products_links


def get_prices(id):
  json_data_for_price = {
    'query': '\n    query getCommerceData($articleIds: [ID!]!, $productSkus: [ID!]!, $siteName: String!) {\n  site(name: $siteName) {\n    articles {\n      byIds(ids: $articleIds) {\n        ...ArticleCommerceData\n      }\n    }\n    products {\n      bySkus(skus: $productSkus) {\n        ...ProductCommerceData\n      }\n    }\n  }\n}\n    \n    fragment ArticleCommerceData on Article {\n  id\n  inventory\n  commerceLink {\n    ...LinkDataFields\n  }\n  campaignPrice {\n    ...PriceFragment\n  }\n  price {\n    ...PriceFragment\n  }\n  isNew\n  hasCampaigns\n  campaigns {\n    ...CampaignData\n  }\n  buyableOnline\n}\n    \n\n    fragment LinkDataFields on LinkData {\n  text\n  href\n  target\n  kind\n  title\n}\n    \n\n    fragment PriceFragment on Price {\n  disclaimer\n  displayPrice {\n    ...MoneyFragment\n  }\n}\n    \n\n    fragment MoneyFragment on Money {\n  amount\n  currency\n}\n    \n\n    fragment CampaignData on CampaignType {\n  title\n  description\n}\n    \n\n    fragment ProductCommerceData on Product {\n  sku\n  fromListPrice {\n    ...PriceFragment\n  }\n  fromCampaignPrice {\n    ...PriceFragment\n  }\n  isNew\n  hasCampaigns\n}\n    ',
    'variables': {
        'articleIds': id,
        'productSkus': [],
        'siteName': 'hbd-it-it-it',
    },
  }
  response = requests.post(HVA_graphql, headers=headers, json=json_data_for_price)
  data = response.json()

  normalPrice = jmespath.search(f"data.site.articles.byIds[0].price.displayPrice.amount", data)
  offerPrice = jmespath.search(f"data.site.articles.byIds[0].campaignPrice.displayPrice.amount", data)
  if not danea_importGrossPrice :
    if normalPrice is not None : normalPrice = np.around(normalPrice / (1+VAT), decimals=1)
    if offerPrice is not None : offerPrice = np.around(offerPrice / (1+VAT), decimals=1)

  return normalPrice, offerPrice


def single_yes_or_no_question(question, default_no=False):
    choices = ' [y/N]: ' if default_no else ' [Y/n]: '
    default_answer = 'n' if default_no else 'y'
    reply = str(input(question + choices)).lower().strip() or default_answer
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False if default_no else True


def main(convert):
  df = pd.DataFrame(get_product_details())

  if convert:
    df['Cod. fornitore'] = pd.Series([danea_codfornitore for x in range(len(df.index))])
    df['Produttore'] = pd.Series([danea_produttore for x in range(len(df.index))])
    logging.info("Adding Husqvarna columns for Danea")

    ListinoA = "Listino 4"
    ListinoB = "Listino 5"

    if danea_importGrossPrice:
      ListinoA = "Listino 4 (ivato)"
      ListinoB = "Listino 5 (ivato)"

    df.rename(columns={
        'p_cat': 'Categoria',
        'p_subcat': 'Sottocategoria',
        'p_name': 'Descrizione',
        'p_id': 'Cod.',
        'p_url': 'Internet',
        'p_desc': 'Note',
        'p_normalPrice': ListinoA,
        'p_offerPrice': ListinoB,
        'p_image': 'Immagine',
      }, inplace=True)

    logging.info("Renaming columns for Danea")

  StyleFrame(df).to_excel("single_product.xlsx", index=False, sheet_name="Prodotti Husqvarna").save()
  logging.info("Done!")


if __name__ == '__main__':
  convertDanea = single_yes_or_no_question('Convert for Danea import? (Yes/No)')
  main(convertDanea)

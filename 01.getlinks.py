
import requests
from requests_html import HTMLSession
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint

baseurl = 'https://www.husqvarna.com/it'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

try:
  s = HTMLSession()
  r = s.get(baseurl, headers=headers)

except requests.exceptions.RequestException as e:
    print(e)

soup = BeautifulSoup(r.content, "html.parser")
links = soup.select('a:-soup-contains("Gamma completa")')

for link in links:
  print(link['href'])

# with open('home.html', 'w',encoding="utf-8") as f:
#  f.write(soup)

import requests
from requests_html import HTMLSession
import chompjs
import pandas as pd
from bs4 import BeautifulSoup
import regex

baseurl = 'https://www.husqvarna.com/it'

try:
  s = HTMLSession()
  r = s.get(baseurl)

except requests.exceptions.RequestException as e:
    print(e)

soup = BeautifulSoup(r.content, "html.parser")
child_soup = soup.select_one('a:-soup-contains("Gamma completa")').text.strip()

print(child_soup)

with open('home.html', 'w',encoding="utf-8") as f:
  f.write(r.html)
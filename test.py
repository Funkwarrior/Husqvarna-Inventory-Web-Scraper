
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import chompjs

url="https://www.husqvarna.com/it/motoseghe/120-mark-ii/"
img_list = []
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
container = soup.find("script").string
print(container)
#r = chompjs.parse_js_object(container, unicode_escape=True)
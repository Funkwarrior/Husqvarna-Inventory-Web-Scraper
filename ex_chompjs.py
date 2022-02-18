from requests_html import HTMLSession
import chompjs
import ftfy
import pprint


s = HTMLSession()
url ="https://www.husqvarna.com/it/motoseghe/120-mark-ii/"

r = s.get(url)

script_css = 'script:contains("ProductDetails")'
script_text = r.html.find(script_css, first=True)
json_data = chompjs.parse_js_object(script_text.text, unicode_escape=True)
pprint.pprint((json_data))
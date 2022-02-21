from requests_html import HTMLSession
import chompjs
import ftfy


s = HTMLSession()
url ="https://www.husqvarna.com/uk/chainsaws/120-mark-ii/"

r = s.get(url)

script_css = 'script:contains("ProductDetails")'
script_text = r.html.find(script_css, first=True)
# json_data = chompjs.parse_js_object(script_text.text)



with open('scriptjson.html', 'w',encoding="utf-8") as f:
  f.write(script_text.text)
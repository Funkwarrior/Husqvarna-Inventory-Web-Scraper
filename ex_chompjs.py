from requests_html import HTMLSession
import chompjs
import ftfy
import pprint


s = HTMLSession()
url ="https://www.husqvarna.com/it/motoseghe/120-mark-ii/"

r = s.get(url)

script_css = 'script:contains("ProductDetails")'
script_text = r.html.find(script_css, first=True)
#json_data = chompjs.parse_js_object(script_text.text, unicode_escape=True)
#pprint.pprint((json_data))

def replace_unicode_character(self, content: str):
    content = content.encode('utf-8')
    if "\\x80" in str(content):
        count_unicode = 0
        i = 0
        while i < len(content):
            if "\\x" in str(content[i:i + 1]):
                if count_unicode % 3 == 0:
                    content = content[:i] + b'\x80\x80\x80' + content[i + 3:]
                i += 2
                count_unicode += 1
            i += 1

        content = content.replace(b'\x80\x80\x80', b'')
    return content.decode('utf-8')

print (type(script_text))
print (dir(script_text))
#with open('scriptjson.html', 'w') as f:
#  html_scraped = replace_unicode_character(script_text, script_text)
#  f.write(html_scraped.html.html)
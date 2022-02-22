from requests_html import HTMLSession
from PIL import Image
import json
import pprint
import jmespath
import urllib


s = HTMLSession()
url ="https://www.husqvarna.com/it/motoseghe/120-mark-ii/"
r = s.get(url)

script_css = 'script:contains("ProductDetails")'
script_text = r.html.find(script_css, first=True)

start = "createElement(ProductDetails, "
end = "), document.getElementById("

z = script_text.text
json_dirty = z[z.find(start)+len(start):z.rfind(end)].strip() #get the token out the html

json_clean = json.loads(json_dirty)
save_filepath = 'ex_json_json_clean.json'

with open(file=save_filepath, mode='w') as output_file:
    json.dump(json_clean, output_file, indent=4)

product = []
#p_name = jmespath.search('initialData.site.products.get.name.longName', json_clean)
#p_sku = jmespath.search('initialData.site.products.get.sku', json_clean)
#p_url = jmespath.search('initialData.site.products.get.url', json_clean)
#p_cat = jmespath.search('initialData.site.products.get.category.name', json_clean)
#p_id = jmespath.search('initialData.site.products.get.articles[0].id', json_clean)
#p_desc = jmespath.search('initialData.site.products.get.articles[0].introductionText', json_clean)

product.append(jmespath.search('initialData.site.products.get.name.longName', json_clean))
product.append(jmespath.search('initialData.site.products.get.sku', json_clean))
product.append(jmespath.search('initialData.site.products.get.url', json_clean))
product.append(jmespath.search('initialData.site.products.get.category.name', json_clean))
product.append(jmespath.search('initialData.site.products.get.articles[0].id', json_clean))
product.append(jmespath.search('initialData.site.products.get.articles[0].introductionText', json_clean))
product.append(jmespath.search('initialData.site.products.get.articles[0].mainImage.sources[2].url', json_clean))
print(product)

#urllib.urlretrieve(product[-1], f(product[1]+".jpg"))


#urllib.urlretrieve(each, filename)
#im = Image.open(product[-1]).convert("RGB")
#im.save(f(product[1]+".jpg"), "jpeg)"
from requests_html import HTMLSession

  s = HTMLSession()

  url = f'https://themes.woocommerce.com/storefront/product-category/clothing/page/1'
  links = []
  r = s.get(url)
  products = r.html.find('ul.products li')
  print(products)

  for item in products:
    links.append(item.find('a', first=True).attrs['href'])
    print(links)
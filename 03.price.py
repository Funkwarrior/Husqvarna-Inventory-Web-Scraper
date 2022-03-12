from ast import Not
from re import I
import requests
import json
import pprint
import jmespath

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
    'referer': 'https://www.husqvarna.com/it/motoseghe/120-mark-ii/',
    'accept-language': 'en-GB,en;q=0.9,it-IT;q=0.8,it;q=0.7,en-US;q=0.6',
    'cookie': 'sessionid=vq1dc4henrngbo1v1tmppumo; hsqglobal#lang=it-IT; ASP.NET_SessionId=q3xq25km0fovv1f5fnpeldcz; SC_ANALYTICS_GLOBAL_COOKIE=68f29e1e7f704e90805b059c6353b096|False; OptanonAlertBoxClosed=2022-02-10T13:05:36.776Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+21+2022+17%3A17%3A07+GMT%2B0100+(Central+European+Standard+Time)&version=6.29.0&isIABGlobal=false&hosts=&consentId=59065fbc-8362-47f7-9fc9-7117155d9e71&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0001%3A1&geolocation=IT%3B36&AwaitingReconsent=false',
}
ids = ['967193401','967893912']

json_data_for_price = {
    'query': '\n    query getCommerceData($articleIds: [ID!]!, $productSkus: [ID!]!, $siteName: String!) {\n  site(name: $siteName) {\n    articles {\n      byIds(ids: $articleIds) {\n        ...ArticleCommerceData\n      }\n    }\n    products {\n      bySkus(skus: $productSkus) {\n        ...ProductCommerceData\n      }\n    }\n  }\n}\n    \n    fragment ArticleCommerceData on Article {\n  id\n  inventory\n  commerceLink {\n    ...LinkDataFields\n  }\n  campaignPrice {\n    ...PriceFragment\n  }\n  price {\n    ...PriceFragment\n  }\n  isNew\n  hasCampaigns\n  campaigns {\n    ...CampaignData\n  }\n  buyableOnline\n}\n    \n\n    fragment LinkDataFields on LinkData {\n  text\n  href\n  target\n  kind\n  title\n}\n    \n\n    fragment PriceFragment on Price {\n  disclaimer\n  displayPrice {\n    ...MoneyFragment\n  }\n}\n    \n\n    fragment MoneyFragment on Money {\n  amount\n  currency\n}\n    \n\n    fragment CampaignData on CampaignType {\n  title\n  description\n}\n    \n\n    fragment ProductCommerceData on Product {\n  sku\n  fromListPrice {\n    ...PriceFragment\n  }\n  fromCampaignPrice {\n    ...PriceFragment\n  }\n  isNew\n  hasCampaigns\n}\n    ',
    'variables': {
        'articleIds': ids,
        'productSkus': [],
        'siteName': 'hbd-it-it-it',
    },
}

response = requests.post('https://www.husqvarna.com/hbd/graphql', headers=headers, json=json_data_for_price)
data = response.json()

for i in range(len(ids)):
    price = jmespath.search(f"data.site.articles.byIds[{i}].price.displayPrice.amount", data)
    campaignprice = jmespath.search(f"data.site.articles.byIds[{i}].campaignPrice.displayPrice.amount", data)
    print (ids[i], price, campaignprice)
import requests
from bs4 import BeautifulSoup
import json
import geocoder

HOST = 'https://som1.ru'
URL = 'https://som1.ru/shops/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "BITRIX_SM_GUEST_ID=7833786; BITRIX_SM_SALE_UID=63536544; _ym_uid=1665790975857760280; _ym_d=1665790975; BX_USER_ID=b25f6f445313fc435974f10dde0e0e40; BITRIX_SM_DETECTED=N; POLICY=Y; BITRIX_SM_CITY_ID=3653; PHPSESSID=qigcHeM03NDwwl6QGJUO58YuGeDCrWqJ; BITRIX_SM_LAST_VISIT=16.10.2022%2020%3A53%3A20; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1665946740%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ym_isad=2"
  }

ls = []


def get_id_city(URL):
    req = requests.post(URL, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    items = soup.find_all('div', class_='cities-container')
    for item in items:
        regions = item.find_all('label')
        for region in regions:
            id_city = region.get('id')
            ls.append(id_city)
    print('id магазинов получены')
    return ls


ls_link = []


def get_link_shops(ls):
    for one in ls:
        payload = {'CITY_ID': one}
        req = requests.post(URL, headers=headers, data=payload)
        soup = BeautifulSoup(req.text, 'lxml')
        items = soup.find_all('div', class_='shops-col shops-button')
        for item in items:
            id_link = HOST + item.find('a').get('href')
            ls_link.append(id_link)
    print('создан список ссылок на магазины')
    return ls_link


def get_content(ls_link):
    shops = []
    for shop in ls_link:
        print('Получение информации о магазине')
        req = requests.get(shop, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        name = soup.find('h1').text
        items = soup.find('div', class_='col-md-6 col-xs-12').find('div', class_='shop-detail-block') \
            .find('table', class_='shop-info-table').find_all('td')
        latlon = geocoder.arcgis(items[2].text).latlng
        shops.append(
            {
                "address": items[2].text,
                "latlon": latlon,
                "name": name,
                "phones": (items[5].text,),
                "working_hours": (items[8].text,)
            }
        )
    with open('shops_2.json', 'w', encoding='utf-8') as f:
        json.dump(shops, f, ensure_ascii=False, indent=4)


get_id_city(URL)
get_link_shops(ls)
get_content(ls_link)

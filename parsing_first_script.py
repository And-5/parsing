import requests
from bs4 import BeautifulSoup
import json
import geocoder

HOST = 'https://oriencoop.cl'
URL = 'https://oriencoop.cl/sucursales.htm'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}

ls = []


def get_link(URL, headers):
    req = requests.get(URL, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    items = soup.find_all('ul', class_='sub-menu')
    for item in items:
        find_teg = item.find_all('a')
        for k in find_teg:
            url_shop = HOST + k.get('href')
            ls.append(url_shop)
    print('создан список ссылок на магазины')
    return ls


def get_content(ls):
    shops = []
    for shop in ls:
        print('Получение информации о магазине')
        try:
            req = requests.get(shop)
            soup = BeautifulSoup(req.text, 'html.parser')
            items = soup.find_all('div', class_='sucursal')
            for item in items:
                r = item.find(class_='s-dato').find_all('span')
                latlon = geocoder.arcgis(r[0].text).latlng
                s = r[3].text.split()
                d = r[4].text.split()
                if len(s) == 5 and len(d) == 13:
                    working_hours = 'mon-thu: ' + s[1] + '-' + s[3] + ' ' + d[1] + '-' +\
                                    d[3], 'fri: ' + s[1] + '-' + d[10]
                elif len(s) == 8 and len(d) == 6:
                    working_hours = 'mon-thu: ' + s[1] + '-' + s[3] + ',fri ' + d[1] + '-' + d[3]
                else:
                    working_hours = 'mon-thu: ' + s[1] + '-' + s[3] + ' ' + s[6] + '-' + s[8] + ',fri: ' + s[1] + '-' +\
                                    s[3] + ' ' + d[2] + '-' + d[4] + ',sun: ' + d[6] + '-' + d[8]
                shops.append(
                    {
                        "address": r[0].text,
                        "latlon": latlon,
                        "name": "Oriencoop",
                        "phones": (r[1].text,),
                        "working_hours": (working_hours,)
                    }
                )
        except requests.exceptions.ConnectionError:
            continue
    with open('shops_1.json', 'w', encoding='utf-8') as f:
        json.dump(shops, f, ensure_ascii=False, indent=2)


get_link(URL, headers)
get_content(ls)

import requests
import json
import geocoder

URL = "https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php"
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "cookie": "BITRIX_SM_GUEST_ID=12149855; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1665957540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ga=GA1.2.1344263755.1665908233; _gid=GA1.2.181545072.1665908233; BX_USER_ID=b25f6f445313fc435974f10dde0e0e40; _ym_uid=166590823959901424; _ym_d=1665908239; _ym_isad=2; PHPSESSID=bfa19631055372f109a07d2301f622d9; _gat=1; _ym_visorc=w; BITRIX_SM_LAST_VISIT=16.10.2022+15%3A10%3A35",
    "Referer": "https://naturasiberica.ru/our-shops/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

payload = {'type': 'all'}


def fetch(url, headers, payload):
    shops = []
    req = requests.post(url, headers=headers, data=payload)
    for shop in req.json()['original']:
        print('Получение информации магазина')
        address = shop['city'] + ', ' + shop['address']
        latlon = geocoder.arcgis(address).latlng
        shops.append(
            {
                "address": address,
                "latlon": latlon,
                "name": 'Natura Siberica',
                "phones": (shop['phone'],),
                "working_hours": (shop['schedule'],)
            }
        )
        with open('shops_3.json', 'w', encoding='utf-8') as f:
            json.dump(shops, f, ensure_ascii=False, indent=4)


fetch(URL, headers, payload)

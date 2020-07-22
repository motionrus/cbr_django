import os
import datetime

import requests

from xml.etree.ElementTree import XML, Element

URL_SCHEME = os.getenv('URL_SCHEME', 'http')
URL_HOST = os.getenv('URL_HOST', 'www.cbr.ru')

URL = '{}://{}'.format(URL_SCHEME, URL_HOST)

API_URLS = {
    'info': '{}/scripts/XML_valFull.asp'.format(URL),
    'daily_rus': '{}/scripts/XML_daily.asp?'.format(URL),
    'daily_eng': '{}/scripts/XML_daily_eng.asp?'.format(URL),
    'dynamic': '{}/scripts/XML_dynamic.asp?'.format(URL),
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}


def date_to_str(date: datetime.datetime) -> str:
    return '{}'.format(date.strftime("%d/%m/%Y")) if date else ''


def str_to_date(date: str) -> datetime.datetime:
    date = date.split('.')
    date.reverse()
    y, m, d = date
    return datetime.datetime(int(y), int(m), int(d))


def get_currencies_info() -> Element:
    response = requests.get(API_URLS['info'], headers=HEADERS)

    return XML(response.text)


def get_dynamic_rates(date_req1: datetime.datetime, date_req2: datetime.datetime, currency_id: str) -> Element:
    url = API_URLS['dynamic'] + 'date_req1={}&date_req2={}&VAL_NM_RQ={}'.format(
        date_to_str(date_req1),
        date_to_str(date_req2),
        currency_id
    )

    response = requests.get(url=url, headers=HEADERS)
    return XML(response.text)

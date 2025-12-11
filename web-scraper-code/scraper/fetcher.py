import requests
from time import sleep

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_page(url):
    for _ in range(3):  # reintentos
        try:
            res = requests.get(url, headers=HEADERS, timeout=5)
            if res.status_code == 200:
                res.encoding = 'utf-8'
                return res.text
        except:
            sleep(1)
    return None

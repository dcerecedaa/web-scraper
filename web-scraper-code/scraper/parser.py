from bs4 import BeautifulSoup
from .config import SELECTORS, BASE_URL

def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    
    for item in soup.select(SELECTORS["product"]):
        title = item.select_one(SELECTORS["title"])["title"]
        price = item.select_one(SELECTORS["price"]).text.replace("£", "")
        availability = item.select_one(SELECTORS["availability"]).text.strip()
        img = item.select_one(SELECTORS["image"])["src"].replace("../", BASE_URL)

        products.append({
            "title": title,
            "price": float(price),
            "availability": availability,
            "image_url": img
        })
    
    return products

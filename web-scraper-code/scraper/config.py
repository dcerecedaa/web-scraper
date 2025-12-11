BASE_URL = "http://books.toscrape.com/"

SELECTORS = {
    "product": "article.product_pod",
    "title": "h3 a",
    "price": "p.price_color",
    "availability": "p.instock.availability",
    "image": "div.image_container img"
}

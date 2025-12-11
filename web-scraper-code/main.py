from scraper.fetcher import get_page
from scraper.parser import parse_products
from scraper.paginator import get_next_page
from scraper.storage import save_csv
from scraper.config import BASE_URL

def run_scraper():
    url = BASE_URL
    all_products = []

    while url:
        print(f"Scraping: {url}")
        html = get_page(url)
        if not html:
            print("Error al cargar la página.")
            break
        
        products = parse_products(html)
        all_products.extend(products)
        
        url = get_next_page(html, url)

    save_csv(all_products)
    print("Scraping completado. Datos guardados en data/products.csv")

if __name__ == "__main__":
    run_scraper()

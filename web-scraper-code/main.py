import sys
import logging
from datetime import datetime
from scraper.fetcher import get_page, close_fetcher
from scraper.parser import UniversalParser
from scraper.storage import save_csv


def setup_logging():
    log_dir = 'logs'
    import os
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f'logs/scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_filename


def print_banner():
    print("\n" + "=" * 60)
    print("SCRAPER UNIVERSAL DE PRODUCTOS")
    print("=" * 60 + "\n")


def get_user_url():
    print("Introduce la URL que quieres scrapear:")

    url = input("URL: ").strip()

    if not url.startswith('http'):
        url = 'https://' + url

    return url


def extract_category_from_url(url):
    url_lower = url.lower()

    genero = "Sin clasificar"
    if any(w in url_lower for w in ['mujer', 'woman', 'women', 'femme']):
        genero = "Mujer"
    elif any(w in url_lower for w in ['hombre', 'man', 'men', 'homme']):
        genero = "Hombre"
    elif any(w in url_lower for w in ['niño', 'niña', 'kids', 'children']):
        genero = "Niños"

    categoria = "General"
    if any(w in url_lower for w in ['pantalon', 'pants', 'trousers', 'jeans']):
        categoria = "Pantalones"
    elif any(w in url_lower for w in ['abrigo', 'chaqueta', 'coat', 'jacket']):
        categoria = "Abrigos"
    elif any(w in url_lower for w in ['camiseta', 't-shirt', 'tshirt', 'top']):
        categoria = "Camisetas"
    elif any(w in url_lower for w in ['vestido', 'dress']):
        categoria = "Vestidos"
    elif any(w in url_lower for w in ['falda', 'skirt']):
        categoria = "Faldas"
    elif any(w in url_lower for w in ['sudadera', 'hoodie', 'sweatshirt']):
        categoria = "Sudaderas"
    elif any(w in url_lower for w in ['zapato', 'shoe', 'sneaker']):
        categoria = "Zapatos"

    return genero, categoria


def run_scraper():
    log_file = setup_logging()
    print_banner()

    url = get_user_url()
    print(f"Iniciando scraper para: {url}")
    print(f"Log guardado en: {log_file}\n")

    all_products = []

    try:
        parser = UniversalParser(url)

        genero, categoria = extract_category_from_url(url)
        print(f"Clasificación detectada: {genero} -> {categoria}\n")

        print("Cargando página.")
        html = get_page(url)

        if not html:
            print("No se pudo cargar la página")
            return

        print("Buscando productos...")
        products = parser.parse_products(html)

        if not products:
            print("No se encontraron productos en esta página")
            return

        for product in products:
            product['genero'] = genero
            product['categoria'] = categoria

        all_products.extend(products)
        print(f"{len(products)} productos encontrados")

        response = input("\n¿Scrapear otra URL? (s/n): ").strip().lower()

        while response == 's':
            url = input("Nueva URL: ").strip()
            if not url.startswith('http'):
                url = 'https://' + url

            genero, categoria = extract_category_from_url(url)
            html = get_page(url)

            if html:
                products = parser.parse_products(html)
                for product in products:
                    product['genero'] = genero
                    product['categoria'] = categoria
                all_products.extend(products)
                print(f"{len(products)} productos encontrados (Total: {len(all_products)})")

            response = input("¿Scrapear otra URL? (s/n): ").strip().lower()

        if not all_products:
            print("No se encontraron productos")
            return

        brand_name = parser.domain.replace('www.', '').replace('www2.', '').split('.')[0]
        filepath = save_csv(all_products, brand_name)

        print("\n" + "=" * 60)
        print("SCRAPING COMPLETADO")
        print("=" * 60)
        print(f"\nTotal productos: {len(all_products)}")
        print(f"Archivo generado: {filepath}")
        print(f"Log: {log_file}")

        from collections import Counter

        categorias_count = Counter(p.get('categoria', 'Sin categoría') for p in all_products)
        print("\nPor categoría:")
        for cat, count in categorias_count.most_common():
            print(f"  {cat}: {count}")

        generos_count = Counter(p.get('genero', 'Sin clasificar') for p in all_products)
        print("\nPor género:")
        for gen, count in generos_count.most_common():
            print(f"  {gen}: {count}")

    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario")
    except Exception as e:
        print(f"\nError fatal: {e}")
        logging.error(f"Error fatal: {e}", exc_info=True)
    finally:
        print("\nCerrando fetcher.")
        close_fetcher()
        print("Proceso finalizado\n")


if __name__ == "__main__":
    run_scraper()

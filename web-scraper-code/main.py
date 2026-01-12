import sys
import logging
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm
from scraper.fetcher import get_page, close_fetcher
from scraper.parser import UniversalParser
from scraper.storage import save_csv
from scraper.config import MAX_PRODUCTS_PER_CATEGORY, MAX_CATEGORIES

# Inicializar colorama para colores en terminal
init(autoreset=True)

# Configurar logging
def setup_logging():
    """Configura el sistema de logging"""
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
    """Imprime el banner del scraper"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🛍️  SCRAPER UNIVERSAL DE PRODUCTOS")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def get_user_url():
    """Solicita la URL al usuario"""
    print(f"{Fore.YELLOW}📌 Introduce la URL de la tienda que quieres scrapear:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   Ejemplo: https://www2.hm.com/")
    print(f"{Fore.WHITE}   Ejemplo: https://www.zara.com/es/\n")
    
    url = input(f"{Fore.GREEN}➜ URL: {Style.RESET_ALL}").strip()
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    return url

def scrape_category(parser, category_info, all_products):
    """Scrape una categoría específica"""
    genero = category_info['genero']
    categoria = category_info['categoria']
    url = category_info['url']
    
    print(f"\n{Fore.BLUE}📂 Scrapeando: {genero} → {categoria}{Style.RESET_ALL}")
    
    try:
        html = get_page(url)
        if not html:
            return
        
        products = parser.parse_products(html)
        
        # Añadir género y categoría a cada producto
        for product in products:
            product['genero'] = genero
            product['categoria'] = categoria
        
        all_products.extend(products)
        print(f"{Fore.GREEN}✅ {len(products)} productos encontrados{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error en {categoria}: {e}{Style.RESET_ALL}")
        logging.error(f"Error scrapeando {url}: {e}")

def run_scraper():
    """Ejecuta el scraper completo"""
    log_file = setup_logging()
    print_banner()
    
    # Obtener URL del usuario
    base_url = get_user_url()
    
    print(f"\n{Fore.CYAN}🚀 Iniciando scraper para: {base_url}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}📝 Log guardado en: {log_file}{Style.RESET_ALL}\n")
    
    all_products = []
    
    try:
        # Inicializar parser
        parser = UniversalParser(base_url)
        
        # Obtener página principal
        print(f"{Fore.YELLOW}🔍 Analizando página principal...{Style.RESET_ALL}")
        home_html = get_page(base_url)
        
        if not home_html:
            print(f"{Fore.RED}❌ No se pudo cargar la página principal{Style.RESET_ALL}")
            return
        
        # Encontrar todas las categorías
        categories = parser.find_categories(home_html)
        
        if not categories:
            print(f"{Fore.YELLOW}⚠️  No se encontraron categorías automáticamente{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Intentando scrapear la página principal...{Style.RESET_ALL}")
            
            products = parser.parse_products(home_html)
            for product in products:
                product['genero'] = 'Sin clasificar'
                product['categoria'] = 'General'
            all_products.extend(products)
        else:
            print(f"\n{Fore.GREEN}✅ {len(categories)} categorías detectadas{Style.RESET_ALL}")
            
            # Limitar categorías si hay demasiadas
            if len(categories) > MAX_CATEGORIES:
                print(f"{Fore.YELLOW}⚠️  Limitando a {MAX_CATEGORIES} categorías{Style.RESET_ALL}")
                categories = categories[:MAX_CATEGORIES]
            
            # Mostrar resumen de categorías
            print(f"\n{Fore.CYAN}📋 Categorías a scrapear:{Style.RESET_ALL}")
            generos = {}
            for cat in categories:
                genero = cat['genero']
                if genero not in generos:
                    generos[genero] = []
                generos[genero].append(cat['categoria'])
            
            for genero, cats in generos.items():
                print(f"  • {genero}: {', '.join(set(cats))}")
            
            # Preguntar si continuar
            print(f"\n{Fore.YELLOW}¿Continuar con el scraping? (s/n): {Style.RESET_ALL}", end='')
            response = input().strip().lower()
            
            if response != 's':
                print(f"{Fore.RED}❌ Scraping cancelado{Style.RESET_ALL}")
                return
            
            # Scrapear cada categoría
            for category_info in tqdm(categories, desc="Progreso total", colour='green'):
                scrape_category(parser, category_info, all_products)
                
                # Limitar productos por categoría
                if len(all_products) > MAX_PRODUCTS_PER_CATEGORY * len(categories):
                    print(f"\n{Fore.YELLOW}⚠️  Límite de productos alcanzado{Style.RESET_ALL}")
                    break
        
        # Guardar resultados
        print(f"\n{Fore.CYAN}💾 Guardando resultados...{Style.RESET_ALL}")
        
        if not all_products:
            print(f"{Fore.RED}❌ No se encontraron productos{Style.RESET_ALL}")
            return
        
        brand_name = parser.brand_config.get('name', parser.domain) if parser.brand_config else parser.domain
        filepath = save_csv(all_products, brand_name.replace(' ', '_'))
        
        # Resumen final
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"✅ SCRAPING COMPLETADO")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}📊 Resumen:{Style.RESET_ALL}")
        print(f"  • Total productos: {Fore.GREEN}{len(all_products)}{Style.RESET_ALL}")
        print(f"  • Archivo principal: {Fore.BLUE}{filepath}{Style.RESET_ALL}")
        print(f"  • Log: {Fore.BLUE}{log_file}{Style.RESET_ALL}")
        
        # Desglose por categoría
        from collections import Counter
        categorias_count = Counter([p.get('categoria', 'Sin categoría') for p in all_products])
        print(f"\n{Fore.CYAN}📂 Por categoría:{Style.RESET_ALL}")
        for cat, count in categorias_count.most_common():
            print(f"  • {cat}: {count}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}⚠️  Scraping interrumpido por el usuario{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error fatal: {e}{Style.RESET_ALL}")
        logging.error(f"Error fatal: {e}", exc_info=True)
    finally:
        # Cerrar navegador
        print(f"\n{Fore.YELLOW}🔒 Cerrando navegador...{Style.RESET_ALL}")
        close_fetcher()
        print(f"{Fore.GREEN}✅ Proceso finalizado{Style.RESET_ALL}\n")

if __name__ == "__main__":
    run_scraper()
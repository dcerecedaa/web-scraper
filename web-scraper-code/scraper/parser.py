from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import logging
from scraper.config import BRAND_CONFIGS, GENERIC_SELECTORS, CATEGORY_KEYWORDS

logger = logging.getLogger(__name__)

class UniversalParser:
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.brand_config = self._get_brand_config()
        self.soup = None
    
    def _get_brand_config(self):
        for domain, config in BRAND_CONFIGS.items():
            if domain in self.domain:
                logger.info(f"  Configuración encontrada para {config['name']}")
                return config
        logger.info("  Usando detección automática (marca no configurada)")
        return None
    
    def parse_html(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        return self.soup
    
    def find_categories(self, html=None):
        if html:
            self.parse_html(html)
        
        if self.brand_config and 'categories' in self.brand_config:
            categories = []
            for genero, urls in self.brand_config['categories'].items():
                for url in urls:
                    full_url = urljoin(self.base_url, url)
                    categoria = self._extract_category_from_url(url)
                    categories.append({
                        'genero': genero,
                        'categoria': categoria,
                        'url': full_url
                    })
            logger.info(f"  {len(categories)} categorías configuradas")
            return categories
        
        return self._auto_detect_categories()
    
    def _auto_detect_categories(self):
        categories = []
        seen_urls = set()
        
        links = self.soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()
            
            genero = self._detect_gender(text, href)
            if not genero:
                continue
            
            categoria = self._detect_category(text, href)
            if not categoria:
                continue
            
            full_url = urljoin(self.base_url, href)
            
            if full_url not in seen_urls:
                seen_urls.add(full_url)
                categories.append({
                    'genero': genero,
                    'categoria': categoria,
                    'url': full_url
                })
        
        logger.info(f"  {len(categories)} categorías detectadas automáticamente")
        return categories
    
    def _detect_gender(self, text, url):
        combined = f"{text} {url}".lower()
        for genero, keywords in CATEGORY_KEYWORDS['genero'].items():
            if any(kw in combined for kw in keywords):
                return genero
        return None
    
    def _detect_category(self, text, url):
        combined = f"{text} {url}".lower()
        for categoria, keywords in CATEGORY_KEYWORDS['categoria'].items():
            if any(kw in combined for kw in keywords):
                return categoria
        return None
    
    def _extract_category_from_url(self, url):
        patterns = [
            r'/([^/]+?)(?:-l\d+)?\.html',  
            r'/([^/]+)/?$',                 
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url.lower())
            if match:
                categoria_raw = match.group(1)
                for categoria, keywords in CATEGORY_KEYWORDS['categoria'].items():
                    if any(kw in categoria_raw for kw in keywords):
                        return categoria
        
        return "General"
    
    def parse_products(self, html):
        self.parse_html(html)
        products = []
        
        # Usar selectores de la config o genéricos
        selectors = (
            self.brand_config.get('selectors', {}) 
            if self.brand_config 
            else {}
        )
        
        # Encontrar tarjetas de productos
        product_cards = self._find_elements(
            selectors.get('product_card', GENERIC_SELECTORS['product_card'])
        )
        
        logger.info(f"  {len(product_cards)} productos encontrados en la página")
        
        for card in product_cards:
            try:
                product = self._extract_product_data(card, selectors)
                if product and product.get('nombre') and product.get('precio'):
                    products.append(product)
            except Exception as e:
                logger.debug(f"Error parseando producto: {e}")
                continue
        
        return products
    
    def _find_elements(self, selectors):
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            try:
                elements = self.soup.select(selector)
                if elements:
                    return elements
            except:
                continue
        
        return []
    
    def _extract_product_data(self, card, selectors):
        product = {}
        
        # Nombre
        name_elem = card.select_one(selectors.get('product_name', 'h3, h2, .product-name'))
        product['nombre'] = name_elem.get_text(strip=True) if name_elem else None
        
        # Precio
        price_elem = card.select_one(selectors.get('product_price', '.price, .product-price'))
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            product['precio'] = self._parse_price(price_text)
        else:
            product['precio'] = None
        
        # URL
        link_elem = card.select_one(selectors.get('product_link', 'a[href]'))
        if link_elem:
            product['url'] = urljoin(self.base_url, link_elem.get('href', ''))
        else:
            product['url'] = None
        
        # Imagen
        img_elem = card.select_one(selectors.get('product_image', 'img'))
        if img_elem:
            product['imagen'] = img_elem.get('src') or img_elem.get('data-src', '')
            product['imagen'] = urljoin(self.base_url, product['imagen'])
        else:
            product['imagen'] = None
        
        product['marca'] = self.brand_config.get('name', self.domain) if self.brand_config else self.domain
        
        return product
    
    def _parse_price(self, price_text):
        price_clean = re.sub(r'[^\d,.]', '', price_text)
        price_clean = price_clean.replace(',', '.')
        
        try:
            return float(price_clean)
        except:
            return None
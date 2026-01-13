from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import logging
from scraper.config import GENERIC_SELECTORS, CATEGORY_KEYWORDS

logger = logging.getLogger(__name__)


class UniversalParser:
    """Parser adaptable a diferentes estructuras de sitios"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.soup = None

    def parse_html(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        return self.soup

    def find_categories(self, html=None):
        if html:
            self.parse_html(html)
        return self._auto_detect_categories()

    def _auto_detect_categories(self):
        categories = []
        seen_urls = set()

        links = self.soup.find_all('a', href=True)
        logger.info(f"Analizando {len(links)} enlaces")

        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()

            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            genero = self._detect_gender(text, href)
            if not genero:
                continue

            categoria = self._detect_category(text, href)
            if not categoria:
                continue

            full_url = urljoin(self.base_url, href)

            if self.domain not in urlparse(full_url).netloc:
                continue

            if full_url not in seen_urls:
                seen_urls.add(full_url)
                categories.append({
                    'genero': genero,
                    'categoria': categoria,
                    'url': full_url
                })

        logger.info(f"{len(categories)} categorías detectadas")
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

    def parse_products(self, html):
        self.parse_html(html)
        products = []

        product_cards = []

        for selector in GENERIC_SELECTORS['product_card']:
            try:
                cards = self.soup.select(selector)
                if len(cards) > 5:
                    product_cards = cards
                    logger.info(f"Selector válido: {selector} ({len(cards)} elementos)")
                    break
            except:
                continue

        if not product_cards:
            logger.warning("No se encontraron productos con selectores estándar")
            product_cards = self._find_by_price()

        logger.info(f"{len(product_cards)} tarjetas encontradas")

        for card in product_cards:
            try:
                product = self._extract_product_data(card)
                if product and product.get('nombre') and product.get('precio'):
                    products.append(product)
            except Exception as e:
                logger.debug(f"Error parseando producto: {e}")

        logger.info(f"{len(products)} productos válidos extraídos")
        return products

    def _find_by_price(self):
        price_pattern = re.compile(r'[€$£]\s*\d+[.,]?\d*|\d+[.,]?\d*\s*[€$£]')
        elements_with_price = []

        for elem in self.soup.find_all(['div', 'article', 'li']):
            if price_pattern.search(elem.get_text()):
                elements_with_price.append(elem)

        return elements_with_price[:50]

    def _extract_product_data(self, card):
        product = {}

        for selector in GENERIC_SELECTORS['product_name']:
            try:
                name_elem = card.select_one(selector)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    if len(name) > 3:
                        product['nombre'] = name
                        break
            except:
                continue

        for selector in GENERIC_SELECTORS['product_price']:
            try:
                price_elem = card.select_one(selector)
                if price_elem:
                    parsed_price = self._parse_price(price_elem.get_text(strip=True))
                    if parsed_price and parsed_price > 0:
                        product['precio'] = parsed_price
                        break
            except:
                continue

        if 'precio' not in product:
            product['precio'] = self._parse_price(card.get_text())

        for selector in GENERIC_SELECTORS['product_link']:
            try:
                link_elem = card.select_one(selector)
                if link_elem and link_elem.get('href'):
                    product['url'] = urljoin(self.base_url, link_elem['href'])
                    break
            except:
                continue

        for selector in GENERIC_SELECTORS['product_image']:
            try:
                img_elem = card.select_one(selector)
                if img_elem:
                    img_src = (
                        img_elem.get('src')
                        or img_elem.get('data-src')
                        or img_elem.get('data-lazy-src')
                    )
                    if img_src:
                        product['imagen'] = urljoin(self.base_url, img_src)
                        break
            except:
                continue

        product['marca'] = (
            self.domain.replace('www.', '')
            .replace('www2.', '')
            .split('.')[0]
            .upper()
        )

        return product

    def _parse_price(self, price_text):
        if not price_text:
            return None

        price_pattern = re.compile(r'(\d+[.,]\d+|\d+)')
        matches = price_pattern.findall(price_text)

        if matches:
            try:
                return float(matches[0].replace(',', '.'))
            except:
                return None

        return None

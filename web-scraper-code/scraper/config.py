import os
from dotenv import load_dotenv

load_dotenv()

# Configuración general
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
TIMEOUT = int(os.getenv('TIMEOUT', 30000))
HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
MIN_DELAY = float(os.getenv('MIN_DELAY', 1))
MAX_DELAY = float(os.getenv('MAX_DELAY', 3))
MAX_PRODUCTS_PER_CATEGORY = int(os.getenv('MAX_PRODUCTS_PER_CATEGORY', 100))
MAX_CATEGORIES = int(os.getenv('MAX_CATEGORIES', 50))

# Configuraciones específicas por marca 
BRAND_CONFIGS = {
    'hm.com': {
        'name': 'H&M',
        'categories': {
            'Mujer': [
                '/es_es/mujer/compra-por-producto/abrigos-chaquetas.html',
                '/es_es/mujer/compra-por-producto/pantalones.html',
                '/es_es/mujer/compra-por-producto/camisetas-tops.html',
                '/es_es/mujer/compra-por-producto/vestidos.html',
                '/es_es/mujer/compra-por-producto/faldas.html',
            ],
            'Hombre': [
                '/es_es/hombre/compra-por-producto/abrigos-chaquetas.html',
                '/es_es/hombre/compra-por-producto/pantalones.html',
                '/es_es/hombre/compra-por-producto/camisetas-tops.html',
                '/es_es/hombre/compra-por-producto/sudaderas-jerseis.html',
            ]
        },
        'selectors': {
            'product_card': 'article.product-item, li.product-item',
            'product_name': 'h3, a.link',
            'product_price': '.price, .product-price',
            'product_link': 'a[href*="/product/"]',
            'product_image': 'img',
            'next_page': 'a.load-more, button[class*="load"]',
        }
    },
    'zara.com': {
        'name': 'Zara',
        'categories': {
            'Mujer': [
                '/es/es/mujer-abrigos-l1055.html',
                '/es/es/mujer-pantalones-l1335.html',
                '/es/es/mujer-camisetas-l1362.html',
                '/es/es/mujer-vestidos-l1066.html',
            ],
            'Hombre': [
                '/es/es/hombre-abrigos-l1432.html',
                '/es/es/hombre-pantalones-l1432.html',
                '/es/es/hombre-camisetas-l1432.html',
            ]
        },
        'selectors': {
            'product_card': 'li.product-grid-product',
            'product_name': 'h2, .product-name',
            'product_price': '.price, .product-detail-selected-price',
            'product_link': 'a.product-link',
            'product_image': 'img.product-image',
            'next_page': 'button[class*="load-more"]',
        }
    },
}

# Selectores genéricos para detección automática
GENERIC_SELECTORS = {
    'product_card': [
        'article.product', 'li.product', 'div.product-item',
        'div.product-card', 'article[data-product]', 
        'li[class*="product"]', 'div[class*="product-grid"]'
    ],
    'product_name': [
        'h3', 'h2', '.product-name', '.product-title',
        'a.product-link', '[class*="product-name"]'
    ],
    'product_price': [
        '.price', '.product-price', '[class*="price"]',
        'span[class*="amount"]', '[data-price]'
    ],
    'product_link': [
        'a[href*="/product"]', 'a[href*="/p/"]',
        'a[href*="item"]', 'a.product-link'
    ],
    'product_image': [
        'img[src*="product"]', 'img.product-image',
        'img[class*="product"]', 'picture img'
    ]
}

# Palabras clave para categorización automática
CATEGORY_KEYWORDS = {
    'genero': {
        'Mujer': ['mujer', 'woman', 'women', 'femme', 'donna', 'damen'],
        'Hombre': ['hombre', 'man', 'men', 'homme', 'uomo', 'herren'],
        'Niños': ['niño', 'niña', 'kids', 'children', 'enfant', 'bambino'],
    },
    'categoria': {
        'Abrigos': ['abrigo', 'chaqueta', 'coat', 'jacket', 'parka', 'blouson'],
        'Pantalones': ['pantalon', 'pants', 'trousers', 'jeans', 'jean'],
        'Camisetas': ['camiseta', 't-shirt', 'tshirt', 'top', 'shirt'],
        'Vestidos': ['vestido', 'dress', 'robe'],
        'Faldas': ['falda', 'skirt', 'jupe'],
        'Sudaderas': ['sudadera', 'hoodie', 'sweatshirt', 'jersey', 'pull'],
        'Zapatos': ['zapato', 'shoe', 'sneaker', 'boot', 'sandal'],
        'Accesorios': ['accesorio', 'accessory', 'bolso', 'bag', 'cinturon', 'belt'],
    }
}
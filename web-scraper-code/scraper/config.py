import os
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
TIMEOUT = int(os.getenv('TIMEOUT', 60000))
HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
MIN_DELAY = float(os.getenv('MIN_DELAY', 2))
MAX_DELAY = float(os.getenv('MAX_DELAY', 5))
MAX_PRODUCTS_PER_CATEGORY = int(os.getenv('MAX_PRODUCTS_PER_CATEGORY', 100))
MAX_CATEGORIES = int(os.getenv('MAX_CATEGORIES', 50))


GENERIC_SELECTORS = {
    'product_card': [
        'article.product',
        'li.product',
        'div.product-item',
        'div.product-card',
        'article[data-product]',
        'li[class*="product"]',
        'div[class*="product-grid"]',
        'article[class*="product"]',
        'div[class*="product-card"]',
        'li[class*="item"]',
        'div[class*="item-card"]',
        'li.product-grid-product',
        'article.product-item',
        'div.product-tile',
        'article.ProductItem',
        'li[data-productid]',
        'div[data-product-id]',
        'article',
        'li',
        'div[class*="card"]'
    ],
    'product_name': [
        'h3',
        'h2',
        'h4',
        '.product-name',
        '.product-title',
        'a.product-link',
        '[class*="product-name"]',
        '[class*="title"]',
        'a[class*="name"]',
        '.name',
        'span[class*="name"]',
        'p[class*="name"]'
    ],
    'product_price': [
        '.price',
        '.product-price',
        '[class*="price"]',
        'span[class*="amount"]',
        '[data-price]',
        '.money',
        '[class*="money"]',
        'span[class*="cost"]',
        'div[class*="price"]',
        'p[class*="price"]'
    ],
    'product_link': [
        'a[href*="/product"]',
        'a[href*="/p/"]',
        'a[href*="item"]',
        'a.product-link',
        'a[class*="product"]',
        'a'
    ],
    'product_image': [
        'img[src*="product"]',
        'img.product-image',
        'img[class*="product"]',
        'picture img',
        'img[alt]',
        'img'
    ]
}


CATEGORY_KEYWORDS = {
    'genero': {
        'Mujer': [
            'mujer', 'woman', 'women', 'femme', 'donna',
            'damen', 'lady', 'ladies', 'her', 'ella'
        ],
        'Hombre': [
            'hombre', 'man', 'men', 'homme', 'uomo',
            'herren', 'him', 'guy', 'male'
        ],
        'Niños': [
            'niño', 'niña', 'kids', 'children', 'enfant',
            'bambino', 'child', 'junior', 'baby'
        ],
        'Unisex': [
            'unisex', 'all', 'everyone', 'todo'
        ]
    },
    'categoria': {
        'Abrigos': [
            'abrigo', 'chaqueta', 'coat', 'jacket',
            'parka', 'blouson', 'cazadora', 'anorak'
        ],
        'Pantalones': [
            'pantalon', 'pants', 'trousers', 'jeans',
            'jean', 'vaquero', 'leggins', 'short'
        ],
        'Camisetas': [
            'camiseta', 't-shirt', 'tshirt', 'top',
            'shirt', 'blusa', 'polo', 'tank'
        ],
        'Vestidos': [
            'vestido', 'dress', 'robe', 'gown'
        ],
        'Faldas': [
            'falda', 'skirt', 'jupe'
        ],
        'Sudaderas': [
            'sudadera', 'hoodie', 'sweatshirt', 'jersey',
            'pull', 'sweater', 'cardigan'
        ],
        'Zapatos': [
            'zapato', 'shoe', 'sneaker', 'boot',
            'sandal', 'zapatilla', 'deportiva'
        ],
        'Accesorios': [
            'accesorio', 'accessory', 'bolso', 'bag',
            'cinturon', 'belt', 'gorra', 'hat',
            'bufanda', 'scarf'
        ],
        'Ropa Interior': [
            'ropa interior', 'underwear', 'lingerie',
            'sujetador', 'bra', 'calcetines', 'socks'
        ]
    }
}

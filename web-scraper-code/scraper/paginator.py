"""
Este archivo se mantiene por compatibilidad pero su funcionalidad
ahora está integrada en parser.py

Si tienes código que lo usa, puedes mantenerlo,
pero el nuevo sistema no lo necesita.
"""

from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_next_page(html, current_url):
    """
    Encuentra el enlace a la siguiente página
    NOTA: Esta función ya no se usa en el nuevo sistema
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Intentar varios selectores comunes para "siguiente página"
    next_selectors = [
        'a.next',
        'a[rel="next"]',
        'a.pagination-next',
        'button.load-more',
        'a:contains("Siguiente")',
        'a:contains("Next")'
    ]
    
    for selector in next_selectors:
        try:
            next_link = soup.select_one(selector)
            if next_link and next_link.get('href'):
                return urljoin(current_url, next_link['href'])
        except:
            continue
    
    return None
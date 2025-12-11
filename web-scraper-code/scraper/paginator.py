from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .config import BASE_URL

def get_next_page(html, current_url):
    soup = BeautifulSoup(html, "html.parser")
    next_btn = soup.select_one("li.next a")
    
    if not next_btn:
        return None
    
    next_page = next_btn["href"]
    
    if "catalogue" in current_url and not next_page.startswith("catalogue"):
        return urljoin(current_url, next_page)
    
    return current_url.rsplit("/", 1)[0] + "/" + next_page

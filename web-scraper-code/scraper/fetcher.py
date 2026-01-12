from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from scraper.config import TIMEOUT, HEADLESS
from scraper.utils.retry import retry_on_failure, random_delay
from scraper.utils.headers import get_random_user_agent
import logging
import sys

logger = logging.getLogger(__name__)

class PlaywrightFetcher:
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def start(self):
        try:
            if sys.platform == 'win32':
                import asyncio
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                except:
                    pass
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=HEADLESS,
                args=['--disable-blink-features=AutomationControlled']
            )
            self.context = self.browser.new_context(
                user_agent=get_random_user_agent(),
                viewport={'width': 1920, 'height': 1080},
                locale='es-ES'
            )
            self.page = self.context.new_page()
            logger.info("  Playwright iniciado correctamente")
        except Exception as e:
            logger.error(f"Error al iniciar Playwright: {e}")
            raise
    
    @retry_on_failure(max_attempts=3)
    def get_page(self, url):
        if not self.page:
            self.start()
        
        try:
            logger.info(f"  Cargando: {url}")
            self.page.goto(url, wait_until='domcontentloaded', timeout=TIMEOUT)
            
            self.page.wait_for_timeout(2000)
            
            self.page.evaluate("""
                window.scrollTo(0, document.body.scrollHeight / 2);
            """)
            self.page.wait_for_timeout(1000)
            
            html = self.page.content()
            random_delay()
            return html
            
        except PlaywrightTimeoutError:
            logger.error(f"  Timeout al cargar {url}")
            raise
        except Exception as e:
            logger.error(f"  Error al cargar {url}: {e}")
            raise
    
    def click_load_more(self, selector):
        try:
            if self.page.query_selector(selector):
                self.page.click(selector)
                self.page.wait_for_timeout(2000)
                return True
        except:
            pass
        return False
    
    def close(self):
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("  Playwright cerrado")
        except:
            pass

_fetcher = None

def get_fetcher():
    global _fetcher
    if _fetcher is None:
        _fetcher = PlaywrightFetcher()
    return _fetcher

def get_page(url):
    fetcher = get_fetcher()
    return fetcher.get_page(url)

def close_fetcher():
    global _fetcher
    if _fetcher:
        _fetcher.close()
        _fetcher = None
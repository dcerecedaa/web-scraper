import time
import random
from functools import wraps
from scraper.config import MAX_RETRIES, MIN_DELAY, MAX_DELAY

def retry_on_failure(max_attempts=MAX_RETRIES):
    """Decorador para reintentar funciones que fallan"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        print(f"❌ Error después de {max_attempts} intentos: {e}")
                        raise
                    wait_time = random.uniform(MIN_DELAY, MAX_DELAY)
                    print(f"⚠️  Intento {attempt + 1} falló. Reintentando en {wait_time:.1f}s...")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

def random_delay():
    """Espera un tiempo aleatorio para evitar detección"""
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
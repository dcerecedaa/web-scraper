import pandas as pd
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Storage:
    """Maneja el almacenamiento de productos en CSV"""

    def __init__(self):
        self.data_dir = 'data'
        self.raw_dir = os.path.join(self.data_dir, 'raw')
        self.processed_dir = os.path.join(self.data_dir, 'processed')
        self._ensure_directories()

    def _ensure_directories(self):
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def save_raw(self, products, brand_name='unknown'):
        if not products:
            logger.warning("No hay productos para guardar")
            return None

        df = pd.DataFrame(products)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"products_{brand_name}_{timestamp}.csv"
        filepath = os.path.join(self.raw_dir, filename)

        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"Datos crudos guardados: {filepath}")
        return filepath

    def save_processed(self, products):
        if not products:
            logger.warning("No hay productos para guardar")
            return None

        df = pd.DataFrame(products)
        df = self._clean_data(df)

        if df.empty:
            logger.warning("Todos los productos fueron filtrados")
            return None

        main_filepath = os.path.join(self.data_dir, 'products.csv')

        if os.path.exists(main_filepath):
            try:
                if os.path.getsize(main_filepath) > 0:
                    df_existing = pd.read_csv(main_filepath)
                    df = pd.concat([df_existing, df], ignore_index=True)
                    df = df.drop_duplicates(subset=['url'], keep='last')
            except (pd.errors.EmptyDataError, Exception) as e:
                logger.warning(f"CSV existente inválido, creando nuevo: {e}")

        df.to_csv(main_filepath, index=False, encoding='utf-8-sig')
        logger.info(f"Datos procesados guardados: {main_filepath} ({len(df)} productos)")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_filepath = os.path.join(
            self.processed_dir, f'products_{timestamp}.csv'
        )
        df.to_csv(processed_filepath, index=False, encoding='utf-8-sig')

        return main_filepath

    def _clean_data(self, df):
        df = df.dropna(subset=['nombre', 'precio'])

        if 'url' in df.columns:
            df = df.drop_duplicates(subset=['url'], keep='first')

        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
        df = df[df['precio'] > 0]

        columns_order = [
            'marca', 'genero', 'categoria',
            'nombre', 'precio', 'url', 'imagen'
        ]
        existing_columns = [c for c in columns_order if c in df.columns]
        return df[existing_columns]

    def load_products(self):
        filepath = os.path.join(self.data_dir, 'products.csv')
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            try:
                return pd.read_csv(filepath)
            except pd.errors.EmptyDataError:
                return pd.DataFrame()
        return pd.DataFrame()


def save_csv(products, brand_name='unknown'):
    storage = Storage()
    storage.save_raw(products, brand_name)
    return storage.save_processed(products)

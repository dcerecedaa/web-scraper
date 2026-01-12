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
        """Crea los directorios si no existen"""
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def save_raw(self, products, brand_name='unknown'):
        """Guarda datos crudos con timestamp"""
        if not products:
            logger.warning("⚠️  No hay productos para guardar")
            return None
        
        df = pd.DataFrame(products)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"products_{brand_name}_{timestamp}.csv"
        filepath = os.path.join(self.raw_dir, filename)
        
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"💾 Datos crudos guardados: {filepath}")
        return filepath
    
    def save_processed(self, products):
        """Guarda datos procesados (limpios, sin duplicados)"""
        if not products:
            return None
        
        df = pd.DataFrame(products)
        
        # Limpiar datos
        df = self._clean_data(df)
        
        # Guardar en data/products.csv (principal)
        main_filepath = os.path.join(self.data_dir, 'products.csv')
        
        # Si existe, combinar con los datos anteriores
        if os.path.exists(main_filepath):
            df_existing = pd.read_csv(main_filepath)
            df = pd.concat([df_existing, df], ignore_index=True)
            df = df.drop_duplicates(subset=['url'], keep='last')
        
        df.to_csv(main_filepath, index=False, encoding='utf-8-sig')
        logger.info(f"💾 Datos procesados guardados: {main_filepath} ({len(df)} productos)")
        
        # También guardar en processed con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_filepath = os.path.join(self.processed_dir, f'products_{timestamp}.csv')
        df.to_csv(processed_filepath, index=False, encoding='utf-8-sig')
        
        return main_filepath
    
    def _clean_data(self, df):
        """Limpia y normaliza los datos"""
        # Eliminar filas sin nombre o precio
        df = df.dropna(subset=['nombre', 'precio'])
        
        # Eliminar duplicados por URL
        df = df.drop_duplicates(subset=['url'], keep='first')
        
        # Normalizar precios
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
        
        # Ordenar columnas
        columns_order = ['marca', 'genero', 'categoria', 'nombre', 'precio', 'url', 'imagen']
        existing_columns = [col for col in columns_order if col in df.columns]
        df = df[existing_columns]
        
        return df
    
    def load_products(self):
        """Carga los productos del CSV principal"""
        filepath = os.path.join(self.data_dir, 'products.csv')
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        return pd.DataFrame()

def save_csv(products, brand_name='unknown'):
    """Función helper para guardar productos"""
    storage = Storage()
    storage.save_raw(products, brand_name)
    return storage.save_processed(products)
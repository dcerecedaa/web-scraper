# 🛍️ Scraper Universal de Productos

Scraper inteligente y universal que funciona con **cualquier tienda online** (H&M, Zara, Pull&Bear, etc.) utilizando detección automática de categorías y productos.

## ✨ Características

- 🌐 **Universal**: Funciona con la mayoría de tiendas online
- 🤖 **Detección Automática**: Identifica categorías y productos automáticamente
- 🎯 **Configuración Híbrida**: Usa configuraciones específicas cuando están disponibles
- 📊 **Dashboard Interactivo**: Visualiza y analiza los productos scrapeados
- 🔄 **Manejo de JavaScript**: Usa Playwright para sitios dinámicos
- 💾 **Almacenamiento Inteligente**: Guarda datos crudos y procesados
- 🏷️ **Categorización**: Organiza por género (Hombre/Mujer) y categoría (Abrigos, Pantalones, etc.)

## 📁 Estructura del Proyecto

```
web-scraper-code/
├── data/
│   ├── raw/                    # CSVs con timestamp
│   ├── processed/              # Datos limpios
│   └── products.csv            # CSV principal
├── scraper/
│   ├── config.py              # Configuración de marcas
│   ├── fetcher.py             # Fetcher con Playwright
│   ├── parser.py              # Parser universal
│   ├── storage.py             # Almacenamiento
│   └── utils/
│       ├── headers.py         # User-agents
│       └── retry.py           # Reintentos
├── visualization/
│   └── dashboard.py           # Dashboard Streamlit
├── logs/                       # Logs de ejecución
├── main.py                     # Script principal
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone 
cd web-scraper-code
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar navegadores de Playwright

```bash
playwright install chromium
```

## 💻 Uso

### Scraper

Ejecuta el scraper y sigue las instrucciones:

```bash
python main.py
```

El programa te pedirá una URL. Ejemplos:
- `https://www2.hm.com/`
- `https://www.zara.com/es/`
- `https://www.pullandbear.com/es/`

El scraper:
1. Analizará la página principal
2. Detectará automáticamente las categorías
3. Scrapeará todos los productos
4. Los organizará por género y categoría
5. Guardará los resultados en CSV

### Dashboard de Visualización

Para ver el dashboard interactivo:

```bash
streamlit run visualization/dashboard.py
```

Esto abrirá una interfaz web con:
- 📊 Gráficos de distribución de precios
- 📂 Análisis por categorías
- 👥 Comparación por género
- 🔍 Explorador de productos con filtros
- ⚖️ Comparador de precios
- 📥 Exportación de resultados

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Configuración del scraper
MAX_RETRIES=3
TIMEOUT=30000
HEADLESS=true

# Delays para evitar bloqueos
MIN_DELAY=1
MAX_DELAY=3

# Límites
MAX_PRODUCTS_PER_CATEGORY=100
MAX_CATEGORIES=50
```

### Añadir Nuevas Marcas

Edita `scraper/config.py` y añade la configuración de la marca:

```python
BRAND_CONFIGS = {
    'tutienda.com': {
        'name': 'Tu Tienda',
        'categories': {
            'Mujer': ['/mujer/abrigos', '/mujer/pantalones'],
            'Hombre': ['/hombre/abrigos', '/hombre/pantalones']
        },
        'selectors': {
            'product_card': '.product-item',
            'product_name': 'h3.title',
            'product_price': '.price',
            'product_link': 'a.product-link',
            'product_image': 'img.product-img',
        }
    }
}
```

## 📊 Formato del CSV

El CSV generado contiene las siguientes columnas:

| Columna   | Descripción                    | Ejemplo              |
|-----------|--------------------------------|----------------------|
| marca     | Nombre de la marca             | H&M                  |
| genero    | Género del producto            | Mujer                |
| categoria | Categoría del producto         | Abrigos              |
| nombre    | Nombre del producto            | Chaqueta vaquera     |
| precio    | Precio en euros                | 39.99                |
| url       | URL del producto               | https://...          |
| imagen    | URL de la imagen               | https://...          |

## 🛠️ Solución de Problemas

### El scraper no encuentra productos

1. Verifica que la URL sea correcta
2. Algunos sitios bloquean scrapers → cambia `HEADLESS=false` en `.env`
3. Revisa los logs en `logs/scraper_XXXXXX.log`

### Error de Playwright

```bash
# Reinstalar navegadores
playwright install chromium --force
```

### El dashboard no muestra datos

Asegúrate de haber ejecutado el scraper primero:
```bash
python main.py
```

## 🎯 Marcas Soportadas

### Preconfiguradas
- ✅ H&M
- ✅ Zara

### Detección Automática
El scraper intentará detectar automáticamente la estructura de cualquier otra tienda.

## 📝 Logs

Los logs se guardan en `logs/` con el formato:
```
logs/scraper_20260112_143025.log
```

## 🤝 Contribuir

¿Quieres añadir configuración para una nueva marca?

1. Edita `scraper/config.py`
2. Añade los selectores CSS correctos
3. Prueba el scraper
4. Envía un Pull Request

## 🔗 Enlaces Útiles

- [Documentación de Playwright](https://playwright.dev/python/)
- [Documentación de BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Documentación de Streamlit](https://docs.streamlit.io/)

## 🤝 Contribuciones

Este proyecto está abierto a sugerencias y feedback. Si tienes ideas de mejora o encuentras algún bug, no dudes en abrir un issue.

## ⚠️ Disclaimer

Este scraper es para uso educativo. Asegúrate de respetar los términos de servicio de los sitios web que scrapes y el archivo `robots.txt`.

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en GitHub.

---
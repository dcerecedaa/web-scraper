# 🛍️ Scraper Universal de Productos

Scraper inteligente y universal que funciona con **tiendas online** utilizando detección automática de categorías y productos.

> ⚠️ **Nota:** Este proyecto es una demostración de habilidades técnicas y lógica aplicada.  
> No pretende ser un sistema de scraping profesional ni listo para producción.  
> Actualmente sigue en desarrollo y algunas marcas conocidas como H&M o Zara no funcionan debido a protecciones anti-scraping.  
> Funciona mejor con tiendas menos bloqueadas o e-commerce basados en Shopify.

---

## ✨ Características

- 🌐 **Universal**: Funciona con la mayoría de tiendas online, especialmente Shopify y otras tiendas con estructuras simples.
- 🤖 **Detección Automática**: Identifica categorías y productos automáticamente.
- 🎯 **Configuración Híbrida**: Usa configuraciones específicas cuando están disponibles.
- 🔄 **Manejo de JavaScript**: Usa Playwright para sitios dinámicos.
- 💾 **Almacenamiento Inteligente**: Guarda datos crudos y procesados.
- 🏷️ **Categorización**: Organiza por categoría (Abrigos, Pantalones, etc.).
- 📊 **Dashboard Interactivo**: Visualiza y analiza los productos scrapeados.

---

## 📁 Estructura del Proyecto

```
web-scraper-code/
├── data/
│   ├── raw/              # CSVs con timestamp
│   ├── processed/        # Datos limpios
│   └── products.csv      # CSV principal
├── scraper/
│   ├── config.py         # Configuración de marcas
│   ├── fetcher.py        # Fetcher con Playwright
│   ├── paginator.py
│   ├── parser.py         # Parser universal
│   ├── storage.py        # Almacenamiento
│   └── utils/
│       ├── headers.py    # User-agents
│       └── retry.py      # Reintentos
├── visualization/
│   └── dashboard.py      # Dashboard Streamlit
├── main.py               # Script principal
├── requirements.txt
├── .env
└── README.md
```

---

## 💻 Uso

### Scraper

Ejecuta el scraper:

```bash
python main.py
```

**Importante:**

Solo funcionan URLs específicas de secciones o categorías, no la homepage de la tienda.

**Ejemplos de URLs válidas:**
- `https://la-tienda.com/es/collections/new-arrivals-hoodies-sweatshirts`
- `https://la-tienda.com/es/collections/new-arrivals-t-shirts`

**Ejemplos de URLs que no funcionarán:**
- `https://nude-project.com/`
- `https://www.hm.com/` (actualmente H&M y Zara están bloqueados)

El scraper:
1. Analiza la página indicada.
2. Detecta automáticamente categorías.
3. Scrapeará todos los productos.
4. Los organiza por género y categoría.
5. Guarda los resultados en CSV (`data/products.csv`).

### Dashboard de Visualización

Para abrir el dashboard interactivo:

```bash
streamlit run visualization/dashboard.py
```

Permite:
- Análisis de precios y distribución.
- Comparación por categorías y género.
- Explorador de productos con filtros.
- Exportación de resultados.

---

## ⚙️ Configuración

### Variables de Entorno (`.env`)

```env
MAX_RETRIES=3
TIMEOUT=30000
HEADLESS=true
MIN_DELAY=1
MAX_DELAY=3
MAX_PRODUCTS_PER_CATEGORY=100
MAX_CATEGORIES=50
```

---

## 📊 Formato del CSV

| Columna   | Descripción              |
|-----------|--------------------------|
| marca     | Nombre de la marca       |
| genero    | Género del producto      |
| categoria | Categoría del producto   |
| nombre    | Nombre del producto      |
| precio    | Precio en euros          |
| url       | URL del producto         |
| imagen    | URL de la imagen         |

---

## 🛠️ Solución de Problemas

**No se encuentran productos:**
- Verifica que la URL apunte a una sección/categoría específica, por ejemplo, "https://la-tienda.com/collections/pantalones"
- Algunos sitios bloquean scrapers → prueba `HEADLESS=false` en `.env`.
- Revisa los logs en `logs/scraper_XXXXXX.log`.

**Error de Playwright**

```bash
playwright install chromium --force
```

**El dashboard no muestra datos:**

Asegúrate de haber ejecutado el scraper primero:

```bash
python main.py
```

---

## 🎯 Marcas Soportadas

- Funciona principalmente con marcas menos bloqueadas y tiendas Shopify.
- Marcas grandes como H&M o Zara actualmente no funcionan debido a protecciones anti-scraping.
- Detección automática para otras tiendas, con limitaciones según la estructura del sitio.

---

## 📝 Logs

Los logs se guardan en `logs/` con formato:

```bash
logs/scraper_YYYYMMDD_HHMMSS.log
```

---

## 🤝 Contribuciones

Este proyecto está abierto a sugerencias y feedback.
El código sigue recibiendo mejoras y actualizaciones.

---

## 👨‍💻 Autor

**David Cereceda Pérez**  
[GitHub](https://github.com/davidcereceda) | [LinkedIn](https://linkedin.com/in/davidcereceda)

---

⚠️ **Nota final:** Proyecto educativo y demostrativo.  
No está pensado para uso comercial ni producción; incluye limitaciones intencionadas para mostrar lógica técnica.

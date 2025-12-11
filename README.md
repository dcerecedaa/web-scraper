# Web Scraper de Productos

Este proyecto es un **web scraper en Python** que extrae información de productos de sitios web de ejemplo como [Books to Scrape](http://books.toscrape.com/).  
Incluye scraping completo con paginación, parseo de datos, almacenamiento en CSV y un módulo de visualización básica.

---

## 📂 Estructura del proyecto

```
web-scraper/
│
├── scraper/                # Módulo principal de scraping
│   ├── __init__.py
│   ├── fetcher.py          # Descarga de HTML con requests
│   ├── parser.py           # Parseo de HTML con BeautifulSoup
│   ├── paginator.py        # Manejo de paginación
│   ├── storage.py          # Guardado de datos en CSV
│   └── config.py           # Configuración de URLs y selectores
│
├── data/                   # Carpeta donde se guardan los CSV de productos
│   └── products.csv
│
├── visualization/          # Módulo de visualización y análisis
│   ├── __init__.py
│   └── data_analysis.py   # Análisis de datos con pandas y matplotlib/seaborn
│
└── main.py                 # Script principal que ejecuta el scraper
```
---

## 🚀 Uso

### 1. Ejecutar el scraper

```bash
python main.py
```

- Scrapea todos los productos de la web configurada en `scraper/config.py`.
- Guarda los datos en `data/products.csv` con las columnas:

```
title, price, availability, image_url
```

---

### 2. Analizar precios

```bash
python -m visualization.data_analysis
```

- Carga los datos del CSV.
- Muestra estadísticas básicas de precios.
- Genera gráficos:
  - Histograma de distribución de precios
  - Boxplot para detectar valores extremos
  - Grafico de pastel para saber que productos están en stock

---

## 🔧 Personalización

- Cambiar URL base o selectores: `scraper/config.py`
- Guardar datos en otro formato: editar `scraper/storage.py`
- Añadir más análisis: agregar scripts en `visualization/`

---

## 📈 Posibles mejoras

- Soporte para páginas con JavaScript usando Selenium o Playwright.
- Descarga automática de imágenes desde `image_url`.
- Análisis de disponibilidad y categorización de productos.
- Alertas automáticas para productos out-of-stock o con precios altos.
- Visualización avanzada con dashboards (Plotly, Dash, Power BI, Tableau).

---

## 📝 Notas

- Este proyecto se hizo como ejemplo de **web scraping**.
- Está pensado para webs de prueba o sitios donde esté permitido el scraping.
- Evitar usarlo en webs con protecciones fuertes o restricciones legales.

---

## 👤 Autor

David Cereceda Perez


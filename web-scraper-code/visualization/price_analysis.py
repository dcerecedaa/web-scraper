import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def load_products():
    """Carga los productos del CSV principal"""
    csv_path = Path('data/products.csv')
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None

def get_price_statistics(df):
    """Obtiene estadísticas básicas de precios"""
    if df is None or df.empty:
        return None
    
    stats = {
        'count': len(df),
        'mean': df['precio'].mean(),
        'median': df['precio'].median(),
        'min': df['precio'].min(),
        'max': df['precio'].max(),
        'std': df['precio'].std()
    }
    return stats

def plot_price_distribution(df, save_path=None):
    """Genera un histograma de distribución de precios"""
    if df is None or df.empty:
        return None
    
    fig = px.histogram(
        df,
        x='precio',
        nbins=50,
        title='Distribución de Precios',
        labels={'precio': 'Precio (€)', 'count': 'Cantidad'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_layout(
        xaxis_title="Precio (€)",
        yaxis_title="Cantidad de Productos",
        showlegend=False,
        template='plotly_white'
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig

def plot_category_prices(df, save_path=None):
    """Genera un gráfico de precios por categoría"""
    if df is None or df.empty:
        return None
    
    avg_prices = df.groupby('categoria')['precio'].mean().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=avg_prices.values,
        y=avg_prices.index,
        orientation='h',
        title='Precio Promedio por Categoría (Top 10)',
        labels={'x': 'Precio Promedio (€)', 'y': 'Categoría'},
        color=avg_prices.values,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        showlegend=False,
        template='plotly_white',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig

def plot_brand_comparison(df, save_path=None):
    """Compara precios entre marcas"""
    if df is None or df.empty or df['marca'].nunique() <= 1:
        return None
    
    fig = px.box(
        df,
        x='marca',
        y='precio',
        title='Comparación de Precios por Marca',
        labels={'marca': 'Marca', 'precio': 'Precio (€)'},
        color='marca'
    )
    
    fig.update_layout(
        showlegend=False,
        template='plotly_white'
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig

def generate_price_report(output_dir='data/reports'):
    """Genera un reporte completo de análisis de precios"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    df = load_products()
    if df is None:
        print(" No se encontraron datos")
        return
    
    # Estadísticas
    stats = get_price_statistics(df)
    print("\n Estadísticas de Precios:")
    print(f"  Total productos: {stats['count']}")
    print(f"  Precio promedio: €{stats['mean']:.2f}")
    print(f"  Precio mediano: €{stats['median']:.2f}")
    print(f"  Precio mínimo: €{stats['min']:.2f}")
    print(f"  Precio máximo: €{stats['max']:.2f}")
    print(f"  Desviación estándar: €{stats['std']:.2f}")
    
    # Generar gráficos
    plot_price_distribution(df, f"{output_dir}/price_distribution.html")
    plot_category_prices(df, f"{output_dir}/category_prices.html")
    
    if df['marca'].nunique() > 1:
        plot_brand_comparison(df, f"{output_dir}/brand_comparison.html")
    
    print(f"\n Reportes guardados en: {output_dir}/")

if __name__ == "__main__":
    generate_price_report()
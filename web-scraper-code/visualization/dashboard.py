import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Productos",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carga los datos del CSV principal"""
    csv_path = Path('data/products.csv')
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        return df
    return None

def show_metrics(df):
    """Muestra métricas principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Productos", f"{len(df):,}")
    
    with col2:
        avg_price = df['precio'].mean()
        st.metric("Precio Promedio", f"€{avg_price:.2f}")
    
    with col3:
        brands = df['marca'].nunique()
        st.metric("Marcas", brands)
    
    with col4:
        categories = df['categoria'].nunique()
        st.metric("Categorías", categories)

def show_price_distribution(df):
    """Gráfico de distribución de precios"""
    st.subheader(" Distribución de Precios")
    
    fig = px.histogram(
        df, 
        x='precio',
        nbins=50,
        title='Distribución de Precios de Productos',
        labels={'precio': 'Precio (€)', 'count': 'Cantidad'},
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        xaxis_title="Precio (€)",
        yaxis_title="Cantidad de Productos",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def show_category_analysis(df):
    """Análisis por categoría"""
    st.subheader("  Análisis por Categoría")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top categorías por cantidad
        category_counts = df['categoria'].value_counts().head(10)
        fig1 = px.bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            title='Top 10 Categorías (por cantidad)',
            labels={'x': 'Cantidad', 'y': 'Categoría'},
            color=category_counts.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Precio promedio por categoría
        avg_price_by_cat = df.groupby('categoria')['precio'].mean().sort_values(ascending=False).head(10)
        fig2 = px.bar(
            x=avg_price_by_cat.values,
            y=avg_price_by_cat.index,
            orientation='h',
            title='Top 10 Categorías (por precio promedio)',
            labels={'x': 'Precio Promedio (€)', 'y': 'Categoría'},
            color=avg_price_by_cat.values,
            color_continuous_scale='Plasma'
        )
        fig2.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

def show_gender_comparison(df):
    """Comparación por género"""
    if 'genero' in df.columns:
        st.subheader("  Comparación por Género")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de productos por género
            gender_counts = df['genero'].value_counts()
            fig1 = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title='Distribución de Productos por Género',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Precio promedio por género
            avg_by_gender = df.groupby('genero')['precio'].mean().sort_values()
            fig2 = px.bar(
                x=avg_by_gender.index,
                y=avg_by_gender.values,
                title='Precio Promedio por Género',
                labels={'x': 'Género', 'y': 'Precio Promedio (€)'},
                color=avg_by_gender.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig2, use_container_width=True)

def show_brand_analysis(df):
    """Análisis por marca"""
    st.subheader("  Análisis por Marca")
    
    if df['marca'].nunique() > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Productos por marca
            brand_counts = df['marca'].value_counts()
            fig1 = px.bar(
                x=brand_counts.index,
                y=brand_counts.values,
                title='Productos por Marca',
                labels={'x': 'Marca', 'y': 'Cantidad'},
                color=brand_counts.values,
                color_continuous_scale='Teal'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Comparación de precios por marca
            fig2 = px.box(
                df,
                x='marca',
                y='precio',
                title='Distribución de Precios por Marca',
                labels={'marca': 'Marca', 'precio': 'Precio (€)'},
                color='marca'
            )
            st.plotly_chart(fig2, use_container_width=True)

def show_product_table(df):
    """Tabla de productos filtrable"""
    st.subheader("  Explorador de Productos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'genero' in df.columns:
            generos = ['Todos'] + sorted(df['genero'].unique().tolist())
            selected_gender = st.selectbox('Género', generos)
        else:
            selected_gender = 'Todos'
    
    with col2:
        categorias = ['Todas'] + sorted(df['categoria'].unique().tolist())
        selected_category = st.selectbox('Categoría', categorias)
    
    with col3:
        marcas = ['Todas'] + sorted(df['marca'].unique().tolist())
        selected_brand = st.selectbox('Marca', marcas)
    
    # Rango de precios
    min_price, max_price = st.slider(
        'Rango de Precio (€)',
        float(df['precio'].min()),
        float(df['precio'].max()),
        (float(df['precio'].min()), float(df['precio'].max()))
    )
    
    # Búsqueda por nombre
    search_term = st.text_input('  Buscar producto por nombre')
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_gender != 'Todos' and 'genero' in df.columns:
        filtered_df = filtered_df[filtered_df['genero'] == selected_gender]
    
    if selected_category != 'Todas':
        filtered_df = filtered_df[filtered_df['categoria'] == selected_category]
    
    if selected_brand != 'Todas':
        filtered_df = filtered_df[filtered_df['marca'] == selected_brand]
    
    filtered_df = filtered_df[
        (filtered_df['precio'] >= min_price) & 
        (filtered_df['precio'] <= max_price)
    ]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['nombre'].str.contains(search_term, case=False, na=False)
        ]
    
    # Mostrar resultados
    st.write(f"**{len(filtered_df)} productos encontrados**")
    
    # Ordenar por
    sort_by = st.selectbox('Ordenar por', ['Precio (menor a mayor)', 'Precio (mayor a menor)', 'Nombre'])
    
    if sort_by == 'Precio (menor a mayor)':
        filtered_df = filtered_df.sort_values('precio')
    elif sort_by == 'Precio (mayor a menor)':
        filtered_df = filtered_df.sort_values('precio', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('nombre')
    
    # Mostrar tabla con columnas seleccionadas
    display_columns = ['nombre', 'precio', 'marca', 'categoria']
    if 'genero' in filtered_df.columns:
        display_columns.insert(3, 'genero')
    
    # Formatear precio
    filtered_display = filtered_df[display_columns].copy()
    filtered_display['precio'] = filtered_display['precio'].apply(lambda x: f"€{x:.2f}")
    
    st.dataframe(
        filtered_display,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Botón de descarga
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="  Descargar resultados (CSV)",
        data=csv,
        file_name=f"productos_filtrados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

def show_price_comparison(df):
    """Comparador de productos"""
    st.subheader("  Comparador de Precios")
    
    if 'categoria' in df.columns:
        selected_cat = st.selectbox('Selecciona una categoría para comparar', df['categoria'].unique())
        
        cat_df = df[df['categoria'] == selected_cat].nsmallest(20, 'precio')
        
        if not cat_df.empty:
            fig = px.scatter(
                cat_df,
                x='nombre',
                y='precio',
                size='precio',
                color='marca',
                hover_data=['categoria'],
                title=f'Comparación de Precios: {selected_cat}',
                labels={'nombre': 'Producto', 'precio': 'Precio (€)'}
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas de la categoría
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Precio Mínimo", f"€{cat_df['precio'].min():.2f}")
            with col2:
                st.metric("Precio Promedio", f"€{cat_df['precio'].mean():.2f}")
            with col3:
                st.metric("Precio Máximo", f"€{cat_df['precio'].max():.2f}")

def main():
    """Función principal del dashboard"""
    
    # Header
    st.markdown('<h1 class="main-header">  Dashboard de Productos</h1>', unsafe_allow_html=True)
    
    # Cargar datos
    df = load_data()
    
    if df is None or df.empty:
        st.warning("  No se encontraron datos. Ejecuta el scraper primero con `python main.py`")
        st.info("  El scraper guardará los datos en `data/products.csv`")
        return
    
    # Sidebar
    with st.sidebar:
        st.title("  Configuración")
        st.write(f"**Total productos:** {len(df):,}")
        st.write(f"**Última actualización:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        
        # Botón de recarga
        if st.button("  Recargar Datos"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Información")
        st.markdown(f"""
        - **Marcas:** {df['marca'].nunique()}
        - **Categorías:** {df['categoria'].nunique()}
        - **Rango de precios:** €{df['precio'].min():.2f} - €{df['precio'].max():.2f}
        """)
    
    # Métricas principales
    show_metrics(df)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Análisis", "Explorador", "Comparador", "Estadísticas"])
    
    with tab1:
        show_price_distribution(df)
        st.markdown("---")
        show_category_analysis(df)
        st.markdown("---")
        show_gender_comparison(df)
    
    with tab2:
        show_product_table(df)
    
    with tab3:
        show_price_comparison(df)
    
    with tab4:
        show_brand_analysis(df)
        
        st.markdown("---")
        st.subheader(" Resumen Estadístico")
        st.dataframe(df.describe(), use_container_width=True)

if __name__ == "__main__":
    main()
import pandas as pd
import streamlit as st
import altair as alt
import os

st.set_page_config(page_title="Comparativa de Productos", layout="wide")

st.title("Comparativa de Productos entre Tiendas")
st.markdown("Filtra por tienda y categoría para comparar precios y productos")

data_path = "data/products.csv"

if not os.path.exists(data_path):
    st.warning("No se ha encontrado el archivo data/products.csv. Ejecuta primero el scraper.")
else:
    df = pd.read_csv(data_path)

    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df.dropna(subset=['precio'], inplace=True)

    tiendas = st.multiselect("Selecciona tiendas", df['marca'].unique(), default=df['marca'].unique())
    categorias = st.multiselect("Selecciona categorías", df['categoria'].unique(), default=df['categoria'].unique())

    df_filtrado = df[df['marca'].isin(tiendas) & df['categoria'].isin(categorias)]

    st.subheader("Resumen Estadístico de Precios")
    resumen = df_filtrado.groupby(['marca', 'categoria'])['precio'].agg(['count', 'min', 'max', 'mean']).reset_index()
    st.dataframe(resumen.style.format({'min': '{:.2f}', 'max': '{:.2f}', 'mean': '{:.2f}'}))

    st.subheader("Comparación de Precios por Tienda y Categoría")
    chart = alt.Chart(df_filtrado).mark_boxplot().encode(
        x=alt.X('categoria:N', title='Categoría'),
        y=alt.Y('precio:Q', title='Precio (€)'),
        color='marca:N',
        tooltip=['marca', 'categoria', 'nombre', 'precio']
    ).properties(width=800, height=400)
    st.altair_chart(chart, use_container_width=True)

    st.subheader("Distribución de Precios")
    hist = alt.Chart(df_filtrado).mark_bar(opacity=0.7).encode(
        x=alt.X('precio:Q', bin=alt.Bin(maxbins=30), title='Precio (€)'),
        y='count()',
        color='marca:N',
        tooltip=['marca', 'count()']
    ).properties(width=800, height=400)
    st.altair_chart(hist, use_container_width=True)

    st.subheader("Productos Filtrados")
    def make_clickable(url):
        return f'<a href="{url}" target="_blank">{url}</a>'
    
    df_filtrado_display = df_filtrado.copy()
    df_filtrado_display['url'] = df_filtrado_display['url'].apply(make_clickable)
    st.write(df_filtrado_display[['marca', 'categoria', 'nombre', 'precio', 'url']].to_html(escape=False), unsafe_allow_html=True)

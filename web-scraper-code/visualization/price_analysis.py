import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ruta del CSV scrapeado
DATA_FILE = os.path.join("data", "products.csv")

def load_data():
    """Cargar los datos del CSV"""
    df = pd.read_csv(DATA_FILE)
    # Asegurarse de que price es float
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df

def plot_price_distribution(df):
    """Histograma de distribución de precios"""
    plt.figure(figsize=(10,6))
    sns.histplot(df['price'], bins=30, kde=True, color='skyblue')
    plt.title("Distribución de precios de los libros")
    plt.xlabel("Precio (£)")
    plt.ylabel("Cantidad de productos")
    plt.tight_layout()
    plt.show()

def plot_price_boxplot(df):
    """Boxplot para detectar valores extremos"""
    plt.figure(figsize=(8,6))
    sns.boxplot(x=df['price'], color='lightgreen')
    plt.title("Boxplot de precios de los libros")
    plt.xlabel("Precio (£)")
    plt.tight_layout()
    plt.show()

def run_analysis():
    df = load_data()
    print("Estadísticas básicas de precios:\n", df['price'].describe())
    plot_price_distribution(df)
    plot_price_boxplot(df)

if __name__ == "__main__":
    run_analysis()
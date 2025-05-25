import matplotlib.pyplot as plt
import pandas as pd

def plot_histogram(df: pd.DataFrame, column: str, output_path: str):
    plt.figure(figsize=(8, 6))
    data = df[column].dropna()

    if pd.api.types.is_numeric_dtype(data):
        plt.hist(data, bins=20, color="skyblue", edgecolor="black")
        plt.title(f"Распределение значений: {column}")
    else:
        counts = data.value_counts().head(20)  # Только топ 20 категорий
        counts.plot(kind="bar", color="orange", edgecolor="black")
        plt.title(f"Частоты категорий: {column}")
        plt.xticks(rotation=45, ha='right')

    plt.xlabel(column)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

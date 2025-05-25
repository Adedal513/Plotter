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

def get_categorical_stats(series: pd.Series) -> str:
    series = series.dropna()
    freq = series.value_counts()
    desc = {
        "🔼 Встречается наиболее часто:": freq.idxmax(),
        "🔽 Встречается наименее часто:": freq.idxmin()
    }
    stats_text = "**📈 Статистика:**\n\n"
    for label, val in desc.items():
        stats_text += f"{label}: `{val}`\n"
    return stats_text

def get_numeric_stats(series: pd.Series) -> str:
    series = series.dropna()
    desc = {
        "🔽 Мин.": series.min(),
        "🔼 Макс.": series.max(),
        "📉 Среднее": series.mean(),
        "📊 Медиана": series.median(),
        "🔟 Перцентиль 10%": series.quantile(0.1),
        "⏫ Перцентиль 90%": series.quantile(0.9),
    }
    stats_text = "**📈 Статистика:**\n\n"
    for label, val in desc.items():
        stats_text += f"{label}: `{val:.4g}`\n"
    return stats_text


def interpret_stats(series: pd.Series) -> str:
    series = series.dropna()
    if len(series) < 10:
        return "_📌 Недостаточно данных для интерпретации._"

    mean = series.mean()
    median = series.median()
    std = series.std()
    p10 = series.quantile(0.10)
    p70 = series.quantile(0.70)
    p90 = series.quantile(0.90)

    notes = []

    if abs(mean - median) > 0.3 * std:
        notes.append("⚠️ Медиана заметно отличается от среднего — возможна асимметрия или выбросы.")

    if (p90 - mean) > (mean - p70):
        notes.append("↗️ Верхний хвост длиннее нижнего — возможна положительная асимметрия.")

    if (median - p10) < 0.1 * std:
        notes.append("📉 Нижний хвост короткий — много значений выше медианы.")

    if not notes:
        return "_✅ Распределение выглядит сбалансированным._"

    return "\n".join(notes)

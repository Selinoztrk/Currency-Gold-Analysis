import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

def load_and_filter_data(filename, start_date=None, end_date=None):
    df = pd.read_csv(filename, parse_dates=["Timestamp"])

    # Filtering by date (optional)
    if start_date:
        df = df[df["Timestamp"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["Timestamp"] <= pd.to_datetime(end_date)]

    # Numerical transformation
    for col in ["USD", "EUR", "Gram Gold", "Quarter Gold"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(".", "", regex=False)
            df[col] = df[col].str.replace(",", ".", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def plot_exchange_rates(df):
    plt.figure(figsize=(12, 6))
    for col in ["USD", "EUR", "Gram Gold", "Quarter Gold"]:
        if col in df.columns and df[col].notna().any():
            plt.plot(df["Timestamp"], df[col], label=col)

    plt.title("Exchange Rates Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_exchange_ratios(df):
    df = df.copy()
    if "USD" in df.columns and "Gram Gold" in df.columns:
        df["USD/GramGold"] = df["USD"] / df["Gram Gold"]
    if "EUR" in df.columns and "Gram Gold" in df.columns:
        df["EUR/GramGold"] = df["EUR"] / df["Gram Gold"]

    plt.figure(figsize=(10, 6))
    if "USD/GramGold" in df.columns:
        plt.plot(df["Timestamp"], df["USD/GramGold"], label="USD / Gram Gold", color="blue")
    if "EUR/GramGold" in df.columns:
        plt.plot(df["Timestamp"], df["EUR/GramGold"], label="EUR / Gram Gold", color="orange")

    plt.title("Currency to Gold Ratios Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Ratio")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_percentage_changes(df):
    df_pct = df.copy()
    df_pct.set_index("Timestamp", inplace=True)

    for col in ["USD", "EUR", "Gram Gold"]:
        if col in df_pct.columns:
            df_pct[col] = df_pct[col].pct_change() * 100

    plt.figure(figsize=(10, 6))
    for col in ["USD", "EUR", "Gram Gold"]:
        if col in df_pct.columns:
            plt.plot(df_pct.index, df_pct[col], label=col)

    plt.title("Percentage Change in Rates Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("% Change")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_interactive_rates(df):
    fig = go.Figure()

    for col in ["USD", "EUR", "Gram Gold"]:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df["Timestamp"],
                y=df[col],
                mode="lines+markers",
                name=col,
                hovertemplate=f"{col}: %{{y:.2f}}<br>Zaman: %{{x|%Y-%m-%d %H:%M}}"
            ))

    fig.update_layout(
        title="Interactive Exchange Rates",
        xaxis_title="Timestamp",
        yaxis_title="Value",
        hovermode="x unified"
    )

    fig.show()


def summarize_extremes(df):
    print("\n📊 Summary of Highest and Lowest Values:\n")
    for col in ["USD", "EUR", "Gram Gold"]:
        if col in df.columns:
            highest = df.loc[df[col].idxmax()]
            lowest = df.loc[df[col].idxmin()]
            change_pct = ((highest[col] - lowest[col]) / lowest[col]) * 100

            print(f"🔹 {col}")
            print(f"  ⬆️ Highest: {highest[col]:.2f} on {highest['Timestamp'].date()}")
            print(f"  ⬇️ Lowest:  {lowest[col]:.2f} on {lowest['Timestamp'].date()}")
            print(f"  🔁 Change:  {change_pct:.2f}%\n")

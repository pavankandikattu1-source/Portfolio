"""
Geographic & Regional Performance – World Bank Development Indicators.
Fetches GDP, GDP per capita, Urban population; analyzes regional trends and growth.
Run: python scripts/run_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw')
PROCESSED = os.path.join(BASE, 'data', 'processed')
VIZ = os.path.join(BASE, 'visualizations')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(PROCESSED, exist_ok=True)
os.makedirs(RAW, exist_ok=True)

# World Bank indicators
INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP",
    "NY.GDP.PCAP.CD": "GDP_per_capita",
    "SP.URB.TOTL.IN.ZS": "Urban_pop_pct"
}

# Key markets for multinational analysis (ING operates in 40+ countries)
COUNTRIES = ["USA", "DEU", "FRA", "GBR", "NLD", "BRA", "IND", "CHN", "JPN"]
CACHE_PATH = os.path.join(RAW, "wb_indicators.csv")


def fetch_wbdata():
    """Fetch World Bank data via wbdata API."""
    try:
        import wbdata
    except ImportError:
        print("Installing wbdata...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'wbdata'])
        import wbdata

    print("Fetching World Bank data (2008-2023)...")
    df = wbdata.get_dataframe(
        INDICATORS,
        country=COUNTRIES,
        date=("2008", "2023"),
        parse_dates=True
    )
    return df


def load_data():
    """Load data from API or cached CSV."""
    if os.path.exists(CACHE_PATH):
        df = pd.read_csv(CACHE_PATH, index_col=0, parse_dates=True)
        if len(df) > 50:
            print("Using cached data from", CACHE_PATH)
            return df

    try:
        df = fetch_wbdata()
        if df is not None and not df.empty:
            df.to_csv(CACHE_PATH)
            return df
    except Exception as e:
        print("API fetch failed:", e)

    # Fallback: generate synthetic sample
    print("Using synthetic sample data.")
    years = np.arange(2008, 2024)
    np.random.seed(42)
    rows = []
    for c in COUNTRIES:
        base_gdp = np.random.uniform(500e9, 5e12)
        base_pc = np.random.uniform(5000, 60000)
        base_urb = np.random.uniform(50, 90)
        for i, y in enumerate(years):
            g = 1 + 0.02 * i + np.random.randn() * 0.02
            rows.append({
                "country": c, "date": pd.Timestamp(f"{y}-01-01"),
                "GDP": base_gdp * (g ** i), "GDP_per_capita": base_pc * (g ** i),
                "Urban_pop_pct": min(95, base_urb + i * 0.5)
            })
    df = pd.DataFrame(rows).set_index("date")
    return df


def main():
    df = load_data()
    if df is None or df.empty:
        print("No data available.")
        return

    # Flatten MultiIndex if present (wbdata returns country as index level)
    if isinstance(df.index, pd.MultiIndex):
        df = df.reset_index()
    elif "country" not in df.columns and df.index.name != "date":
        df = df.reset_index()

    # Ensure we have country and date
    if "country" not in df.columns:
        df["country"] = df.index.get_level_values("country") if isinstance(df.index, pd.MultiIndex) else "USA"
    if "date" not in df.columns and not isinstance(df.index, pd.DatetimeIndex):
        df["date"] = df.index

    # Normalize column names
    df = df.rename(columns={c: c.replace(" ", "_") for c in df.columns if " " in c})
    numeric_cols = [c for c in ["GDP", "GDP_per_capita", "Urban_pop_pct"] if c in df.columns]
    if not numeric_cols:
        numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns]

    print("Shape:", df.shape, "| Countries:", df["country"].nunique() if "country" in df.columns else "N/A")

    # 1. GDP per capita by country (latest year)
    if "GDP_per_capita" in df.columns and "country" in df.columns:
        latest = df.groupby("country")["GDP_per_capita"].last().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        latest.plot(kind="barh", ax=ax, color="steelblue", edgecolor="navy", alpha=0.8)
        ax.set_xlabel("GDP per Capita (current US$)")
        ax.set_title("GDP per Capita by Country (Latest Year)")
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(VIZ, "gdp_per_capita_by_country.png"), dpi=100)
        plt.close()

    # 2. GDP growth trajectory (top 5 countries)
    if "GDP" in df.columns and "country" in df.columns:
        df_grp = df.groupby(["country", df.index.year if isinstance(df.index, pd.DatetimeIndex) else pd.to_datetime(df["date"]).dt.year])["GDP"].sum().unstack(0)
        if df_grp.shape[1] >= 2:
            top5 = df_grp.iloc[-1].nlargest(5).index.tolist()
            plot_cols = [c for c in top5 if c in df_grp.columns]
            if plot_cols:
                df_grp[plot_cols].plot(figsize=(10, 5), marker="o", markersize=4)
                plt.title("GDP Trajectory – Top 5 Countries")
                plt.ylabel("GDP (current US$)")
                plt.xlabel("Year")
                plt.legend(bbox_to_anchor=(1.02, 1))
                plt.tight_layout()
                plt.savefig(os.path.join(VIZ, "gdp_trajectory.png"), dpi=100)
                plt.close()

    # 3. Urban population % by country (latest)
    if "Urban_pop_pct" in df.columns and "country" in df.columns:
        urb = df.groupby("country")["Urban_pop_pct"].last().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        urb.plot(kind="barh", ax=ax, color="teal", alpha=0.8)
        ax.set_xlabel("Urban Population (% of total)")
        ax.set_title("Urbanization by Country (Latest Year)")
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(VIZ, "urban_population_by_country.png"), dpi=100)
        plt.close()

    # 4. YoY GDP growth by country
    if "GDP" in df.columns and "country" in df.columns:
        df_sorted = df.sort_values(["country", "date"])
        df_sorted["yoy_gdp"] = df_sorted.groupby("country")["GDP"].pct_change() * 100
        yoy_latest = df_sorted.dropna(subset=["yoy_gdp"]).groupby("country")["yoy_gdp"].last().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        yoy_latest.plot(kind="bar", ax=ax, color="coral", edgecolor="darkred", alpha=0.8)
        ax.set_ylabel("YoY GDP Growth (%)")
        ax.set_title("Year-over-Year GDP Growth by Country (Latest)")
        ax.axhline(0, color="black", linestyle="-", linewidth=0.5)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(VIZ, "gdp_yoy_growth.png"), dpi=100)
        plt.close()

    # 5. Correlation: GDP per capita vs Urban %
    if "GDP_per_capita" in df.columns and "Urban_pop_pct" in df.columns:
        pivot = df.pivot_table(values=["GDP_per_capita", "Urban_pop_pct"], index="country", aggfunc="mean")
        if len(pivot) >= 3:
            fig, ax = plt.subplots(figsize=(8, 6))
            for c in pivot.index:
                ax.scatter(pivot.loc[c, "Urban_pop_pct"], pivot.loc[c, "GDP_per_capita"], s=100, label=c)
            ax.set_xlabel("Urban Population (%)")
            ax.set_ylabel("GDP per Capita (US$)")
            ax.set_title("GDP per Capita vs Urbanization by Country")
            ax.legend(bbox_to_anchor=(1.02, 1))
            plt.tight_layout()
            plt.savefig(os.path.join(VIZ, "gdp_vs_urbanization.png"), dpi=100)
            plt.close()

    # Save processed
    df.to_csv(os.path.join(PROCESSED, "regional_indicators.csv"))
    print("Done. Outputs:", VIZ, PROCESSED)


if __name__ == "__main__":
    main()

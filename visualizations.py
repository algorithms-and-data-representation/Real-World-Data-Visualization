"""
Visualizations — Video Game Sales Dataset (VGChartz style)
==========================================================
Dataset: vgsales.csv

Story:
"What drives success in the video game industry?"

Visualizations:
1. Sales by Genre
2. Sales by Platform (Top 10)
3. Sales Trend Over Time
4. Sales Distribution (Power Law)
5. Regional Sales Comparison
6. Top 20 Best-Selling Games
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── setup ─────────────────────────────────────────────────────────────
os.makedirs("plots", exist_ok=True)

CSV = "data/vgsales.csv"
df = pd.read_csv(CSV)

# limpiar nombres
df = df.rename(columns={
    "Name": "title",
    "Genre": "genre",
    "Year": "year",
    "Global_Sales": "global_sales"
})

df = df.dropna(subset=["year"])

# estilo
plt.style.use("dark_background")

def save(name):
    path = f"plots/{name}.png"
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"✅ {path}")

# ═══════════════════════════════════════════════════════════════════════
# 1. Sales by Genre
# ═══════════════════════════════════════════════════════════════════════
print("[1] Sales by Genre")

genre_sales = df.groupby("genre")["global_sales"].sum().sort_values()

plt.figure(figsize=(12,7))
bars = plt.barh(genre_sales.index, genre_sales.values)

plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.title("Total Global Sales by Genre", fontsize=14)

# valores en cada barra
for i, v in enumerate(genre_sales.values):
    plt.text(v + 0.5, i, f"{v:.1f}", va='center')

plt.xlabel("Sales (Millions)")
plt.tight_layout()
save("viz1_genre_sales")

# ═══════════════════════════════════════════════════════════════════════
# 2. Top Platforms
# ═══════════════════════════════════════════════════════════════════════
print("[2] Top Platforms")

platform_sales = df.groupby("Platform")["global_sales"].sum().sort_values().tail(10)

plt.figure(figsize=(12,7))
bars = plt.barh(platform_sales.index, platform_sales.values, color="orange")

plt.grid(axis="x", linestyle="--", alpha=0.6)

for i, v in enumerate(platform_sales.values):
    plt.text(v + 0.5, i, f"{v:.1f}", va='center')

plt.title("Top 10 Platforms by Global Sales", fontsize=14)
plt.xlabel("Sales (Millions)")
plt.tight_layout()
save("viz2_platform_sales")

# ═══════════════════════════════════════════════════════════════════════
# 3. Sales Over Time
# ═══════════════════════════════════════════════════════════════════════
print("[3] Sales Trend")

year_sales = df.groupby("year")["global_sales"].sum()

plt.figure(figsize=(12,6))
plt.plot(year_sales.index, year_sales.values, marker="o")

plt.grid(True, linestyle="--", alpha=0.6)

# etiquetas en puntos clave (cada 2 años)
for i, (x, y) in enumerate(zip(year_sales.index, year_sales.values)):
    if i % 2 == 0:
        plt.text(x, y, f"{y:.0f}", fontsize=8)

plt.title("Global Sales Over Time", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Sales (Millions)")
plt.tight_layout()
save("viz3_sales_trend")

# ═══════════════════════════════════════════════════════════════════════
# 4. Power Law Distribution
# ═══════════════════════════════════════════════════════════════════════
print("[4] Sales Distribution")

sales = df["global_sales"].values

plt.figure(figsize=(12,6))
plt.hist(sales, bins=50)

plt.yscale("log")
plt.grid(True, linestyle="--", alpha=0.6)

plt.title("Sales Distribution (Power Law)", fontsize=14)
plt.xlabel("Sales (Millions)")
plt.ylabel("Frequency (log scale)")
plt.tight_layout()
save("viz4_sales_distribution")

# ═══════════════════════════════════════════════════════════════════════
# 5. Regional Comparison
# ═══════════════════════════════════════════════════════════════════════
print("[5] Regional Sales")

regions = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
region_totals = df[regions].sum()

plt.figure(figsize=(10,6))
bars = plt.bar(region_totals.index, region_totals.values)

plt.grid(axis="y", linestyle="--", alpha=0.6)

# etiquetas encima
for i, v in enumerate(region_totals.values):
    plt.text(i, v + 5, f"{v:.0f}", ha='center')

plt.title("Sales by Region", fontsize=14)
plt.ylabel("Sales (Millions)")
plt.tight_layout()
save("viz5_region_sales")

# ═══════════════════════════════════════════════════════════════════════
# 6. Top Games
# ═══════════════════════════════════════════════════════════════════════
print("[6] Top Games")

top_games = df.sort_values("global_sales", ascending=False).head(20)

plt.figure(figsize=(12,8))
bars = plt.barh(top_games["title"], top_games["global_sales"])

plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.6)

# valores en cada barra
for i, v in enumerate(top_games["global_sales"]):
    plt.text(v + 0.3, i, f"{v:.1f}", va='center')

plt.title("Top 20 Best-Selling Games", fontsize=14)
plt.xlabel("Sales (Millions)")
plt.tight_layout()
save("viz6_top_games")

# ── final ─────────────────────────────────────────────────────────────
print("\n✅ All visualizations saved in /plots")

print("\nStorytelling:")
print("1. Action and Sports dominate global sales")
print("2. PlayStation and Nintendo platforms lead the market")
print("3. Sales peaked around late 2000s")
print("4. Industry follows power-law: few hits dominate")
print("5. North America is the largest market")
print("6. A small number of games generate massive revenue")
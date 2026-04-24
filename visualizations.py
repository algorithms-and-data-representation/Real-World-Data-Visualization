"""
Task C — Real World Data Visualization
=======================================
Dataset : vgsales.csv (VGChartz — 16,598 real game records)
Story   : "What drives success in the video game industry?"

Visualizations
--------------
  1. Heatmap       — Regional sales by Genre (which genres sell where?)
  2. Sales Trend   — Global sales over time (KEPT — best original chart)
  3. Distribution  — Power law of game sales (KEPT — best original chart)
  4. Cluster       — K-Means: 4 market archetypes by regional profile
  5. Genre Sales   — Total sales by genre with market share
"""

import os, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# LOAD & CLEAN
# ─────────────────────────────────────────────────────────────
os.makedirs("plots", exist_ok=True)

df = pd.read_csv("data/vgsales.csv")
df = df.rename(columns={"Name": "title", "Genre": "genre",
                         "Year": "year",  "Global_Sales": "global_sales"})
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

print(f"Dataset: {len(df):,} games | {df['genre'].nunique()} genres | "
      f"{df['year'].min()}–{df['year'].max()}")

# ─────────────────────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────────────────────
BG    = "#0d1117"
PANEL = "#161b22"
GRID  = "#21262d"
TXT   = "#e6edf3"
MUT   = "#8b949e"
ACCENT= "#58a6ff"
GREEN = "#3fb950"
RED   = "#f85149"
GOLD  = "#d29922"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   MUT,
    "text.color":        TXT,
    "xtick.color":       MUT,
    "ytick.color":       MUT,
    "grid.color":        GRID,
    "grid.linestyle":    "--",
    "grid.alpha":        0.4,
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

def save(name):
    path = f"plots/{name}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  ✅  {path}")


# ═════════════════════════════════════════════════════════════
# VIZ 1 — HEATMAP: Regional Sales by Genre
# Story: Japan is its own market — Role-Playing dominates there
#        while Action and Shooter rule everywhere else.
# ═════════════════════════════════════════════════════════════
print("\n[1] Heatmap — Regional Sales by Genre …")

regions       = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
region_labels = ["North America", "Europe", "Japan", "Rest of World"]

pivot     = df.groupby("genre")[regions].sum()
pivot.columns = region_labels
pivot_pct = pivot.div(pivot.sum(axis=0), axis=1) * 100
pivot_pct = pivot_pct.sort_values("North America", ascending=False)

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor(BG)

cmap = sns.color_palette("mako", as_cmap=True)
sns.heatmap(
    pivot_pct,
    annot=True, fmt=".1f",
    annot_kws={"size": 10},
    cmap=cmap,
    linewidths=1,
    linecolor="#0d1117", 
    ax=ax, cbar_kws={"shrink": 0.7}
)

for text in ax.texts:
    val = float(text.get_text().replace("\u2212", "-"))
    text.set_color(TXT if val < 12 else "#0d1117")

ax.tick_params(axis="x", labelsize=10, colors=MUT, rotation=0)
ax.tick_params(axis="y", labelsize=9,  colors=MUT, rotation=0)
ax.collections[0].colorbar.ax.tick_params(colors=MUT)
ax.collections[0].colorbar.set_label("Market share (%)", color=MUT)

fig.suptitle(
    "Regional Market Share by Genre  (% of each region's total sales)\n"
    "Japan is a Role-Playing market  |  Action & Shooter dominate NA and EU",
    color=TXT, fontsize=12, fontweight="bold", y=1.02
)
save("viz1_heatmap_genre_region")


# ═════════════════════════════════════════════════════════════
# VIZ 2 — SALES TREND OVER TIME  ← KEPT (best original chart)
# Story: The industry peaked in 2008 at the height of the Wii/DS
#        era. The drop after 2010 reflects the rise of mobile gaming.
# ═════════════════════════════════════════════════════════════
print("[2] Sales Trend over Time …")

year_sales = df.groupby("year")["global_sales"].sum()
year_sales = year_sales[year_sales.index <= 2016]

genre_year = df[df["year"] <= 2016].groupby(
    ["year", "genre"])["global_sales"].sum().unstack(fill_value=0)

top_genres = df.groupby("genre")["global_sales"].sum() \
               .sort_values(ascending=False).head(5).index.tolist()

GENRE_COLORS = {
    "Action":      "#e74c3c",
    "Sports":      "#f39c12",
    "Shooter":     "#3498db",
    "Role-Playing":"#9b59b6",
    "Platform":    "#2ecc71",
}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), sharex=True,
                                gridspec_kw={"height_ratios": [1.6, 1]})
fig.patch.set_facecolor(BG)

ax1.fill_between(year_sales.index, year_sales.values, color=ACCENT, alpha=0.15)
ax1.plot(year_sales.index, year_sales.values,
         color=ACCENT, lw=2.5, marker="o", ms=5)

peak_year = year_sales.idxmax()
peak_val  = year_sales.max()
ax1.annotate(f"Peak: {peak_val:.0f}M\n({peak_year})",
             xy=(peak_year, peak_val),
             xytext=(peak_year + 1.5, peak_val * 0.88),
             arrowprops=dict(arrowstyle="->", color=GOLD),
             color=GOLD, fontsize=9, fontweight="bold")

ax1.axvspan(2010, 2016, color=RED, alpha=0.07)
ax1.text(2012, year_sales.max() * 0.25, "Mobile era\n(casual shift)",
         color=RED, fontsize=8.5, ha="center", alpha=0.9)
ax1.set_ylabel("Global Sales (Millions)", fontsize=10)
ax1.set_title("Global Video Game Sales Over Time",
              color=TXT, fontsize=11, fontweight="bold")
ax1.grid(axis="y")

bottom = np.zeros(len(genre_year))
for genre in top_genres:
    if genre in genre_year.columns:
        vals = genre_year[genre].values
        ax2.fill_between(genre_year.index, bottom, bottom + vals,
                         color=GENRE_COLORS.get(genre, MUT),
                         alpha=0.75, label=genre)
        bottom += vals

ax2.set_ylabel("Sales by Genre (M)", fontsize=10)
ax2.set_xlabel("Year", fontsize=10)
ax2.legend(fontsize=8, facecolor=PANEL, edgecolor=GRID,
           labelcolor=TXT, loc="upper left", ncol=5)
ax2.grid(axis="y")

fig.suptitle(
    "The Rise and Fall of Console Gaming (1980–2016)\n"
    "Wii + DS era peaked in 2008  |  Mobile gaming disrupted the market after 2010",
    color=TXT, fontsize=13, fontweight="bold"
)
plt.tight_layout()
save("viz2_sales_trend")


# ═════════════════════════════════════════════════════════════
# VIZ 3 — SALES DISTRIBUTION  ← KEPT (required: distribution)
# Story: Video game sales follow a power law — most games sell
#        under 1M units while Wii Sports sold over 80M.
# ═════════════════════════════════════════════════════════════
print("[3] Sales Distribution (Power Law) …")

sales = np.sort(df["global_sales"].values)[::-1]
ccdf  = np.arange(1, len(sales) + 1) / len(sales)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.patch.set_facecolor(BG)

bins = np.logspace(np.log10(sales.min()), np.log10(sales.max()), 45)
ax1.hist(sales, bins=bins, color=ACCENT, alpha=0.8, edgecolor=BG)
ax1.axvline(1, color=GREEN, linestyle="--", alpha=0.6)
ax1.text(1, ax1.get_ylim()[1]*0.5, "1M units", color=GREEN, fontsize=8)
ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlabel("Global Sales (M, log scale)", fontsize=10)
ax1.set_ylabel("Number of Games (log scale)", fontsize=10)
ax1.set_title("Sales Distribution — Log-Log\nStraight line = power-law confirmed",
              color=TXT, fontsize=11, fontweight="bold")
ax1.grid(True)

ax2.loglog(sales, ccdf, color=ACCENT, lw=2.5)
ax2.fill_between(sales, ccdf, alpha=0.12, color=ACCENT)

p10_idx   = int(0.10 * len(sales))
p1_idx    = int(0.01 * len(sales))
top10_pct = sales[:p10_idx].sum() / sales.sum() * 100
top1_pct  = sales[:p1_idx].sum()  / sales.sum() * 100

for idx, color, label in [
    (p10_idx, GREEN,
     f"Top 10%\n>{sales[p10_idx]:.2f}M units\n={top10_pct:.0f}% of sales"),
    (p1_idx, RED,
     f"Top 1%\n>{sales[p1_idx]:.1f}M units\n={top1_pct:.0f}% of sales"),
]:
    ax2.axvline(sales[idx], color=color, lw=1.5, linestyle="--")
    ax2.text(sales[idx] * 1.2, ccdf[idx] * 2.5, label,
             color=color, fontsize=8.5, fontweight="bold",
             bbox=dict(facecolor=PANEL, edgecolor=color,
                       boxstyle="round,pad=0.3", alpha=0.9))

ax2.set_xlabel("Sales (M units, log scale)", fontsize=10)
ax2.set_ylabel("P(Sales > x)  [CCDF]", fontsize=10)
ax2.set_title("Complementary CDF — Long Tail\nA handful of hits generate most revenue",
              color=TXT, fontsize=11, fontweight="bold")
ax2.grid(True)

fig.suptitle(
    f"The Power Law of Video Game Sales  —  "
    f"Top 10% = {top10_pct:.0f}% of total sales  |  "
    f"Top 1% = {top1_pct:.0f}% of total sales",
    color=TXT, fontsize=13, fontweight="bold"
)
save("viz3_sales_distribution")


# ═════════════════════════════════════════════════════════════
# VIZ 4 — K-MEANS CLUSTER: Regional Market Archetypes
# Story: K-Means reveals 4 hidden market archetypes that pure
#        sales totals don't show — Global Hits, NA Dominators,
#        Japan Exclusives, and Niche titles.
# ═════════════════════════════════════════════════════════════
print("[4] K-Means Cluster …")

region_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
df_c = df[region_cols + ["genre", "title", "global_sales"]].copy()
df_c = df_c[df_c["global_sales"] > 0.05]

scaler = StandardScaler()
X      = scaler.fit_transform(df_c[region_cols])
km     = KMeans(n_clusters=4, random_state=42, n_init=15)
df_c["cluster"] = km.fit_predict(X)

centroids   = scaler.inverse_transform(km.cluster_centers_)
centroid_df = pd.DataFrame(centroids, columns=region_cols)
centroid_df["jp_ratio"] = centroid_df["JP_Sales"] / (centroid_df["NA_Sales"] + 0.01)
centroid_df["na_share"] = centroid_df["NA_Sales"] / (centroid_df[region_cols].sum(axis=1) + 0.01)
centroid_df["total"]    = centroid_df[region_cols].sum(axis=1)

jp_cluster    = int(centroid_df["jp_ratio"].idxmax())
hit_cluster   = int(centroid_df["total"].idxmax())
remaining     = [i for i in range(4) if i not in [jp_cluster, hit_cluster]]
na_cluster    = int(centroid_df.loc[remaining, "na_share"].idxmax())
niche_cluster = [i for i in remaining if i != na_cluster][0]

name_map = {
    hit_cluster:   ("Global Hits",      "#f39c12"),
    jp_cluster:    ("Japan Exclusives",  "#9b59b6"),
    na_cluster:    ("NA Dominators",     "#3498db"),
    niche_cluster: ("Niche Titles",      "#2ecc71"),
}
df_c["archetype"] = df_c["cluster"].map(lambda c: name_map[c][0])
arch_colors = {v[0]: v[1] for v in name_map.values()}
archs = ["Global Hits", "NA Dominators", "Japan Exclusives", "Niche Titles"]

fig, (ax_s, ax_b) = plt.subplots(1, 2, figsize=(16, 7),
                                  gridspec_kw={"width_ratios": [1.3, 1]})
fig.patch.set_facecolor(BG)

for arch in archs:
    sub = df_c[df_c["archetype"] == arch]
    sizes = np.clip(sub["global_sales"] * 8, 10, 200)

    ax_s.scatter(sub["NA_Sales"], sub["JP_Sales"],
                color=arch_colors[arch], alpha=0.4,
                s=sizes,
                label=f"{arch} (n={len(sub):,})",
                edgecolors="none")

for c_idx, (arch, color) in name_map.items():
    cx = centroids[c_idx][0]
    cy = centroids[c_idx][2]
    ax_s.scatter(cx, cy, s=220, color=color,
                 edgecolors="white", linewidths=1.5, zorder=5)
    ax_s.annotate(arch, (cx, cy),
                  textcoords="offset points", xytext=(8, 5),
                  fontsize=8.5, color=color, fontweight="bold")

ax_s.set_xscale("log")
ax_s.set_yscale("log")

ax_s.set_xlabel("North America Sales (log scale)", fontsize=10)
ax_s.set_ylabel("Japan Sales (log scale)", fontsize=10)
ax_s.set_title(
    "Regional Market Archetypes (K-Means)\n"
    "Log scale reveals hidden structure — Japan-only vs global hits",
    color=TXT, fontsize=11, fontweight="bold"
)
ax_s.legend(fontsize=8.5, facecolor=PANEL, edgecolor=GRID, labelcolor=TXT)
ax_s.grid(True)

avg = df_c.groupby("archetype")[region_cols].mean().loc[archs]
x   = np.arange(len(region_cols))
w   = 0.2
for i, arch in enumerate(archs):
    ax_b.bar(x + i * w, avg.loc[arch], w,
             color=arch_colors[arch], alpha=0.85, label=arch)

ax_b.set_xticks(x + w * 1.5)
ax_b.set_xticklabels(["NA", "EU", "JP", "Other"], fontsize=10)
ax_b.set_ylabel("Average Sales (M)", fontsize=10)
ax_b.set_title("Regional Sales Profile per Archetype\n"
               "Japan Exclusives barely register outside Japan",
               color=TXT, fontsize=11, fontweight="bold")
ax_b.legend(fontsize=8.5, facecolor=PANEL, edgecolor=GRID, labelcolor=TXT)
ax_b.grid(axis="y")

fig.suptitle(
    "K-Means (k=4) — Regional Market Archetypes\n"
    "Global Hits · NA Dominators · Japan Exclusives · Niche Titles",
    color=TXT, fontsize=13, fontweight="bold"
)
plt.tight_layout()
save("viz4_kmeans_archetypes")


# ═════════════════════════════════════════════════════════════
# VIZ 5 — GENRE SALES with market share + efficiency
# Story: Action leads in total volume, but Platform games have
#        the highest sales-per-title — fewer games, bigger hits.
# ═════════════════════════════════════════════════════════════
print("[5] Genre Sales …")

genre_stats = df.groupby("genre").agg(
    total_sales=("global_sales", "sum"),
    n_games=("title",            "count"),
).reset_index()
genre_stats["sales_per_title"] = genre_stats["total_sales"] / genre_stats["n_games"]
genre_stats["market_share"]    = genre_stats["total_sales"] / genre_stats["total_sales"].sum() * 100
genre_stats = genre_stats.sort_values("total_sales")

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor(BG)

norm   = plt.Normalize(genre_stats["sales_per_title"].min(),
                        genre_stats["sales_per_title"].max())
colors = plt.cm.plasma(norm(genre_stats["sales_per_title"].values))

ax.barh(genre_stats["genre"], genre_stats["total_sales"],
        color=colors, alpha=0.9, height=0.65)

x_max = genre_stats["total_sales"].max()
for i, row in enumerate(genre_stats.itertuples()):
    ax.text(row.total_sales + x_max * 0.01, i,
            f"{row.total_sales:.0f}M  ({row.market_share:.1f}%)",
            va="center", fontsize=8.5, color=TXT)
    ax.text(x_max * 0.98, i,
            f"{row.sales_per_title:.2f}M/game",
            va="center", ha="right", fontsize=7.5, color=MUT)

sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cb = fig.colorbar(sm, ax=ax, shrink=0.6, pad=0.01)
cb.set_label("Sales per Title (M)", color=MUT, fontsize=9)
cb.ax.tick_params(colors=MUT)

ax.set_xlabel("Total Global Sales (Millions)", fontsize=10)
ax.grid(axis="x")

fig.suptitle(
    "Total Sales by Genre  (color = avg sales per title)\n"
    "Action leads in total volume  |  Platform has the highest hit-rate per title",
    color=TXT, fontsize=13, fontweight="bold"
)
save("viz5_genre_sales")

print("\n✅  All 5 visualizations saved to plots/")
print("\nStorytelling summary:")
print("  Viz 1 — Heatmap:   Japan is a Role-Playing market; NA/EU prefer Action & Shooter")
print("  Viz 2 — Trend:     Industry peaked 2008; mobile disrupted it after 2010")
print("  Viz 3 — Distrib:   Power law — top 1% of games = most of all sales")
print("  Viz 4 — Cluster:   4 archetypes: Global Hits, NA Dominators, JP Excl., Niche")
print("  Viz 5 — Genre:     Action leads volume; Platform has best hit-rate per title")

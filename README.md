# Real-World-Data-Visualization

**Dataset:** Video Game Sales — VGChartz (available on Kaggle)
**Story:** *"What drives success in the video game industry?"*

---

## Dataset

**Source:** `vgsales.csv` — VGChartz global video game sales data, available at:
https://www.kaggle.com/datasets/gregorut/videogamesales

**16,327 records** (after removing rows with missing year) across **11 columns:**
`Rank`, `Name`, `Platform`, `Year`, `Genre`, `Publisher`,
`NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales`, `Global_Sales`

---

## Visualizations & Stories

| # | Type | Story |
|---|------|-------|
| 1 | **Heatmap** | Japan is a Role-Playing market — completely different from NA and EU |
| 2 | **Time Series** | Industry peaked in 2008 (Wii/DS era); mobile gaming disrupted it after 2010 |
| 3 | **Distribution** | Power law: top 1% of games account for most of total sales |
| 4 | **K-Means Cluster** | 4 hidden market archetypes: Global Hits, NA Dominators, Japan Exclusives, Niche Titles |
| 5 | **Bar + Colormap** | Action leads in total volume; Platform has the best sales-per-title ratio |

---

## Structure

```
task_c/
├── visualizations.py      ← all 5 plots, run this
├── data/
│   └── vgsales.csv        ← dataset (download from Kaggle link above)
├── plots/                 ← generated automatically on first run
│   ├── viz1_heatmap_genre_region.png
│   ├── viz2_sales_trend.png
│   ├── viz3_sales_distribution.png
│   ├── viz4_kmeans_archetypes.png
│   └── viz5_genre_sales.png
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
# 1. Download the dataset from Kaggle and place it in data/vgsales.csv

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run — generates all 5 plots in plots/
python visualizations.py
```

---

## Key Findings

- **Japan** consumes 27% of its gaming budget on Role-Playing games vs ~10% in NA/EU
- The industry **peaked at 679M units** sold in 2008, then declined with the rise of mobile
- **Top 1%** of games (≈163 titles) generate a disproportionate share of all sales — a classic power law
- K-Means on regional sales recovers **4 natural market segments** without any labels
- **Platform games** (Mario, Sonic) have the highest average sales per title despite fewer releases

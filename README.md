# Task C — Real World Data Visualization (10%)

**Dataset:** Video Games Industry — 1,500 games, 2013–2023, 18 variables  
**Story:** *"What separates good games from great games — and great games from blockbusters?"*

---

## Dataset

Modelled after Steam, Metacritic, and VGChartz industry statistics.  
Sources: Steam annual reports, Metacritic score distributions, VGChartz global sales, Newzoo Global Games Market Report 2023.

**18 columns:** title, genre, platform, publisher, year, esrb_rating,
metacritic_score, user_score, price_usd, global_sales_M, avg_playtime_hrs,
peak_players, n_reviews, dlc_count, has_multiplayer, is_free_to_play,
has_microtransactions, awards_nominated

---

## Visualizations & Stories

| # | Type | Key Insight |
|---|------|-------------|
| 1 | Correlation Heatmap | Metacritic score is the #1 predictor of sales; price predicts nothing |
| 2 | Horizontal Bar (gap) | Horror & Fighting: players love them more; Strategy: critics see more depth |
| 3 | Bubble Chart | No correlation between price and quality at any price point |
| 4 | Histogram + CCDF | Power law: top 5% of games account for ~50% of total sales |
| 5 | Horizontal Bar (log) | MMO/Sim: infinite games; Horror/Adventure: curated short experiences |
| 6 | K-Means (3 panels) | 4 archetypes: Blockbusters, Niche Gems, Live Service, Indie Darlings |

---

## Structure

```
task_c_videogames/
├── dataset_generator.py    ← generates data/videogames.csv
├── visualizations.py       ← all 6 plots + storytelling
├── data/
│   └── videogames.csv
├── plots/
│   ├── viz1_correlation_heatmap.png
│   ├── viz2_critics_vs_players.png
│   ├── viz3_price_vs_metacritic.png
│   ├── viz4_sales_power_law.png
│   ├── viz5_playtime_by_genre.png
│   └── viz6_game_archetypes.png
├── requirements.txt
└── README.md
```

## Quick Start

```bash
pip install -r requirements.txt
python visualizations.py
```

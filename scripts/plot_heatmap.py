import json
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# Základní cesta k souborům
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tvoje_mama_combined.json")

# Načtení dat
with open(DATA_PATH, "r", encoding="utf-8") as f:
    all_data = json.load(f)

# Sběr dat
heatmap_data = {}

for season in all_data:
    sezona = season["season"]
    for player in season.get("statistiky_hracu", []):
        jmeno = player["hráč"]
        goly = player["gólů"]

        if jmeno not in heatmap_data:
            heatmap_data[jmeno] = {}
        heatmap_data[jmeno][sezona] = goly

# Vytvoření DataFrame a doplnění nul
df = pd.DataFrame(heatmap_data).T.fillna(0)

# Seřadit sezóny správně
def sezona_sort_key(s):
    year, part = s.split()
    return (int(year), 0 if part == "jaro" else 1)

sorted_columns = sorted(df.columns, key=sezona_sort_key)
df = df[sorted_columns]

# Vykreslení heatmapy
plt.figure(figsize=(18, 8))
sns.set(style="whitegrid")

ax = sns.heatmap(df, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.3, linecolor='gray',
                 cbar_kws={'label': 'Počet gólů'}, annot_kws={"size": 7})

plt.title("Heatmapa gólů hráčů podle sezón", fontsize=16, pad=15)
plt.xlabel("Sezóna", fontsize=12)
plt.ylabel("Hráč", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.show()

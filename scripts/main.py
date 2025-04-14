import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

filename = "data/tvoje_mama_combined.json"
print(f"📂 Načítám {filename}")
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)


hrac_stats = defaultdict(lambda: defaultdict(lambda: {"góly": 0, "zápasy": 0}))
team_season_points = []


for season_data in data:
    sezona = season_data.get("season", "neznámá")
    statistiky = season_data.get("statistiky_hracu", [])
    for player in statistiky:
        jmeno = player.get("hráč") or player.get("Hráč")
        goly = player.get("gólů") or player.get("Gólů") or 0
        zapasy = player.get("zápasů") or player.get("Zápasů") or 0
        if jmeno:
            try:
                hrac_stats[jmeno][sezona]["góly"] += int(goly)
            except:
                pass
            try:
                hrac_stats[jmeno][sezona]["zápasy"] += int(zapasy)
            except:
                pass

    
    tabulka = season_data.get("tabulka", [])
    for row in tabulka:
        if row["tým"] == "Tvoje máma FC":
            body = row.get("body") or row.get("Počet bodů")
            if body is not None:
                try:
                    team_season_points.append({"sezona": sezona, "body": int(body)})
                except:
                    pass
            break


rows = []
for hrac, sezony in hrac_stats.items():
    for sezona, stats in sezony.items():
        rows.append({
            "hráč": hrac,
            "sezona": sezona,
            "góly": stats["góly"],
            "zápasy": stats["zápasy"]
        })
df_hraci = pd.DataFrame(rows)


df_sum = df_hraci.groupby("hráč").sum(numeric_only=True).reset_index()
df_sum = df_sum.sort_values("góly", ascending=False)
df_top = df_sum.head(10)  # Top 10 hráčů podle gólů

df_body = pd.DataFrame(team_season_points)
df_body = df_body.sort_values("sezona")
x_labels = df_body["sezona"]
y_values = df_body["body"]
x_positions = list(range(len(x_labels)))

# === 📊 GRAF ===
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
fig.subplots_adjust(wspace=0.4)

# 🎯 Hráči: sloupce
bar_width = 0.4
x = range(len(df_top))

bars1 = ax1.barh([i - bar_width/2 for i in x], df_top["góly"], height=bar_width, label="Góly", color="crimson")
bars2 = ax1.barh([i + bar_width/2 for i in x], df_top["zápasy"], height=bar_width, label="Zápasy", color="seagreen")

ax1.set_yticks(x)
ax1.set_yticklabels(df_top["hráč"])
ax1.set_xlabel("Počet")
ax1.set_title("🎯 Góly a zápasy hráčů (TOP 10 - podle počtů gólů)")
ax1.legend()
ax1.invert_yaxis()

# 🏷️ Přidání textu
for bar in bars1:
    width = bar.get_width()
    ax1.text(width + 0.5, bar.get_y() + bar.get_height() / 2, str(int(width)), va="center", fontsize=8)

for bar in bars2:
    width = bar.get_width()
    ax1.text(width + 0.5, bar.get_y() + bar.get_height() / 2, str(int(width)), va="center", fontsize=8)

# 📈 Body týmu
ax2.plot(x_positions, y_values, marker="o", color="dodgerblue", linewidth=2, label="Body týmu")
ax2.set_title("📈 Vývoj bodů týmu v sezónách")
ax2.set_xticks(x_positions)
ax2.set_xticklabels(x_labels, rotation=45, ha="right")
ax2.set_xlabel("Sezóna")
ax2.set_ylabel("Body")
ax2.grid(True)

# 🏷️ Hodnoty bodů
for x, y in zip(x_positions, y_values):
    ax2.text(x, y + 0.5, str(y), ha='center', fontsize=9)

plt.tight_layout()
plt.show()

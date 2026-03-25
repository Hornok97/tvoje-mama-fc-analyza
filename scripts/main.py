import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tvoje_mama_combined.json")


def load_data(path):
    print(f"📂 Načítám {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_player_stats(data):
    hrac_stats = defaultdict(lambda: defaultdict(lambda: {"góly": 0, "zápasy": 0}))
    team_season_points = []

    for season_data in data:
        sezona = season_data.get("season", "neznámá")

        for player in season_data.get("statistiky_hracu", []):
            jmeno = player.get("hráč", player.get("Hráč"))
            goly = player.get("gólů", player.get("Gólů", 0))
            zapasy = player.get("zápasů", player.get("Zápasů", 0))
            if not jmeno:
                continue
            try:
                hrac_stats[jmeno][sezona]["góly"] += int(goly)
            except (ValueError, TypeError):
                pass
            try:
                hrac_stats[jmeno][sezona]["zápasy"] += int(zapasy)
            except (ValueError, TypeError):
                pass

        for row in season_data.get("tabulka", []):
            if row["tým"] == "Tvoje máma FC":
                body = row.get("body", row.get("Počet bodů"))
                if body is not None:
                    try:
                        team_season_points.append({"sezona": sezona, "body": int(body)})
                    except (ValueError, TypeError):
                        pass
                break

    return hrac_stats, team_season_points


def build_dataframes(hrac_stats, team_season_points):
    rows = [
        {"hráč": hrac, "sezona": sezona, "góly": stats["góly"], "zápasy": stats["zápasy"]}
        for hrac, sezony in hrac_stats.items()
        for sezona, stats in sezony.items()
    ]
    df_hraci = pd.DataFrame(rows)
    df_sum = (
        df_hraci.groupby("hráč")
        .sum(numeric_only=True)
        .reset_index()
        .sort_values("góly", ascending=False)
    )
    df_top = df_sum.head(10)

    df_body = pd.DataFrame(team_season_points).sort_values("sezona")
    return df_top, df_body


def plot(df_top, df_body):
    x_labels = df_body["sezona"]
    y_values = df_body["body"]
    x_positions = list(range(len(x_labels)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
    fig.subplots_adjust(wspace=0.4)

    bar_width = 0.4
    bar_indices = range(len(df_top))

    bars1 = ax1.barh([i - bar_width / 2 for i in bar_indices], df_top["góly"], height=bar_width, label="Góly", color="crimson")
    bars2 = ax1.barh([i + bar_width / 2 for i in bar_indices], df_top["zápasy"], height=bar_width, label="Zápasy", color="seagreen")

    ax1.set_yticks(bar_indices)
    ax1.set_yticklabels(df_top["hráč"])
    ax1.set_xlabel("Počet")
    ax1.set_title("Góly a zápasy hráčů (TOP 10 - podle počtů gólů)")
    ax1.legend()
    ax1.invert_yaxis()

    for bar in [*bars1, *bars2]:
        width = bar.get_width()
        ax1.text(width + 0.5, bar.get_y() + bar.get_height() / 2, str(int(width)), va="center", fontsize=8)

    ax2.plot(x_positions, y_values, marker="o", color="dodgerblue", linewidth=2, label="Body týmu")
    ax2.set_title("Vývoj bodů týmu v sezónách")
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(x_labels, rotation=45, ha="right")
    ax2.set_xlabel("Sezóna")
    ax2.set_ylabel("Body")
    ax2.grid(True)

    for pos, body in zip(x_positions, y_values):
        ax2.text(pos, body + 0.5, str(body), ha="center", fontsize=9)

    plt.tight_layout()
    plt.show()


def main():
    data = load_data(DATA_PATH)
    hrac_stats, team_season_points = build_player_stats(data)
    df_top, df_body = build_dataframes(hrac_stats, team_season_points)
    plot(df_top, df_body)


if __name__ == "__main__":
    main()

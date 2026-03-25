import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tvoje_mama_combined.json")


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_heatmap_data(all_data):
    heatmap_data = {}

    for season in all_data:
        sezona = season["season"]

        for player in season.get("statistiky_hracu", []):
            jmeno = player["hráč"]
            goly = player["gólů"]

            if jmeno not in heatmap_data:
                heatmap_data[jmeno] = {}

            heatmap_data[jmeno][sezona] = goly

    return heatmap_data


def sezona_sort_key(s):
    year, part = s.split()
    return int(year), 0 if part == "jaro" else 1


def create_dataframe(data):
    df = pd.DataFrame(data).T.fillna(0)
    sorted_columns = sorted(df.columns, key=sezona_sort_key)
    return df[sorted_columns]


def plot_heatmap(df):
    plt.figure(figsize=(18, 8))
    sns.set(style="whitegrid")

    sns.heatmap(
        df,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.3,
        linecolor="gray",
        cbar_kws={"label": "Počet gólů"},
        annot_kws={"size": 7},
    )

    plt.title("Heatmapa gólů hráčů podle sezón", fontsize=16, pad=15)
    plt.xlabel("Sezóna")
    plt.ylabel("Hráč")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()


def main():
    data = load_data(DATA_PATH)
    heatmap_data = build_heatmap_data(data)
    df = create_dataframe(heatmap_data)
    plot_heatmap(df)


if __name__ == "__main__":
    main()
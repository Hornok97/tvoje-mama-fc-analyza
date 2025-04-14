import os
import json

def combine_json_files(directory=".", output_file="tvoje_mama_combined.json"):
    all_data = []

    for filename in os.listdir(directory):
        if filename.startswith("tvoje_mama_") and filename.endswith(".json") and filename != output_file:
            filepath = os.path.join(directory, filename)
            print(f"📂 Načítám {filename}")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.append(data)
            except Exception as e:
                print(f"❌ Chyba při čtení {filename}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Všechna data sloučena do {output_file} ({len(all_data)} sezón)")

if __name__ == "__main__":
    combine_json_files()

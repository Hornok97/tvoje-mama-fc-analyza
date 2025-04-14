# Analýza výkonu týmu Tvoje máma FC (Malý fotbal, Hanspaulská liga)

Tento projekt slouží k analýze výkonu amatérského fotbalového týmu "Tvoje máma FC", který se účastní pražské **Hanspaulské ligy**. Projekt zahrnuje **web scraping** historických dat (2015–2024), jejich **čištění**, **vizualizaci**, a přípravu datasetu vhodného pro analýzu.

---

## Obsah Projektu

```
.
├── data/                  # JSON soubory se sezónními statistikami
│   └── tvoje_mama_combined.json
├── scripts/
│   ├── finale.py          # Hlavní scraper pro sezóny 2015–2024
│   ├── Test_2018.py       # Speciální řešení pro problémovou sezónu 2018 jaro
│   ├── combine_jsons.py   # Spojení jednotlivých JSONů do jednoho
│   ├── main.py            # Analýza a vizualizace (grafy, heatmapy)
│   └── plot_heatmap.py    # Vizuální analýza hráčské aktivity
├── README.md              # Tento soubor
├── requirements.txt       # Závislosti projektu
```

---

## ⚙️ Instalace

1. **Naklonuj repozitář**
```bash
git clone https://github.com/uzivatel/tvoje-mama-fc-analyza.git
cd tvoje-mama-fc-analyza
```

2. **Nainstaluj závislosti**
```bash
pip install -r requirements.txt
```

---

## Co skripty dělají?

### 1. `finale.py`  
Hlavní scraper:
- Prochází oficiální stránku [psmf.cz/souteze](https://www.psmf.cz/souteze/)
- Hledá odkazy pro sezóny 2015–2024
- Vyhledá tým **"Tvoje máma FC"** pouze ve 6.–8. lize
- Stáhne detailní stránku týmu
- Extrahuje data: zápasy, tabulky, statistiky
- Uloží jako `tvoje_mama_{rok}_{sezona}.json`

### 2. `Test_2018.py`  
Speciální skript vytvořený kvůli chybě ve struktuře webu v sezóně **2018 jaro**, kdy hlavní scraper nemohl najít správnou URL. Nakonec vyřešeno dynamickým nalezením URL podle atributu `title="Tvoje máma FC"`.

### 3. `combine_jsons.py`  
Spojuje všechny jednotlivé JSONy do jednoho: 
📄 `tvoje_mama_combined.json`

### 4. `main.py`  
Spouští analýzu:
- Vytváří přehledný dataset hráčů (zápasy + góly)
- Vypočítá týmové body v každé sezóně
- Vykreslí přehledné grafy pomocí `matplotlib`

### 5. `plot_heatmap.py`  
Rozšířená vizualizace:
- Heatmapa gólů podle sezón a hráčů - barevné rozlišení pro nejlepší výkony
- Pomáhá najít výkonnostní trendy
- Možnost dalšího rozšíření na analýzu a porovnání hráčů

---

## Výstupy

- 📁 `data/tvoje_mama_combined.json` — hlavní datový soubor - obsahuje kompletní json sezón 2015-2024
> 🗣️ *„Čím víc gólů dáme, tím víc bodů máme.“* — Ludvík Hovorka, Okresní přebor

## Možnosti rozšíření

- Automatické generování PDF reportů
- Nasazení do webového dashboardu (např. pomocí Streamlit)

---

## 🧩 Autor

Projekt vytvořen jako praktická ukázka **data scrapingu, zpracování a vizualizace dat**.
Vhodné do portfolia a pro inspiraci dalším sportovním týmům 🟢⚽

import requests
from bs4 import BeautifulSoup
import re
import json

BASE_URL = "https://www.psmf.cz"
LIST_URL = f"{BASE_URL}/souteze/"
TEAM_NAME = "Tvoje máma FC"
TEAM_SLUG = "tvoje-mama-fc"
HEADERS = {"User-Agent": "Mozilla/5.0"}

year_pattern = re.compile(r"/souteze/(\d{4})-hanspaulska-liga")

def fetch_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"⚠️ Chyba při načítání {url}: {e}")
    return None

def parse_table(section, expected_cols):
    rows = section.find_all("tr")
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) == expected_cols:
            data.append([c.get_text(strip=True) for c in cols])
    return data

def split_match_teams(text):
    if TEAM_NAME in text:
        if text.startswith(TEAM_NAME):
            return TEAM_NAME, text.replace(TEAM_NAME, "").strip()
        else:
            return text.replace(TEAM_NAME, "").strip(), TEAM_NAME
    return "", text

def parse_vysledky(soup):
    for section in soup.find_all("div", class_="component__wrap"):
        if "Výsledky" in section.text:
            table = parse_table(section, 6)
            vysledky = []
            for r in table:
                domaci, hoste = split_match_teams(r[3])
                vysledky.append({
                    "datum": r[0],
                    "čas": r[1],
                    "hřiště": r[2],
                    "domácí": domaci,
                    "hosté": hoste,
                    "kolo": r[4].replace(".", ""),
                    "výsledek": r[5]
                })
            return vysledky
    return []

def parse_tabulka(soup):
    tabulka = []
    for container in soup.select(".container"):
        if "Tabulky" in container.get_text():
            rows = container.select("tr")
            for row in rows:
                cols = row.select("td")
                if len(cols) == 8:
                    tabulka.append({
                        "pořadí": cols[0].text.strip().replace(".", ""),
                        "tým": cols[1].text.strip(),
                        "zápasy": int(cols[2].text.strip()),
                        "výhry": int(cols[3].text.strip()),
                        "remízy": int(cols[4].text.strip()),
                        "prohry": int(cols[5].text.strip()),
                        "skóre": cols[6].text.strip(),
                        "body": int(cols[7].text.strip())
                    })
            break
    return tabulka

def parse_statistiky(soup):
    for section in soup.find_all("div", class_="component__wrap"):
        if "Statistiky" in section.text:
            table = parse_table(section, 3)
            return [
                {
                    "hráč": row[0],
                    "zápasů": int(row[1]),
                    "gólů": int(row[2])
                }
                for row in table
            ]
    return []

def parse_team_details(url, season_label):
    soup = fetch_soup(url)
    if not soup:
        return None

    zapasy = parse_vysledky(soup)
    tabulka = parse_tabulka(soup)
    statistiky = parse_statistiky(soup)

    if not zapasy:
        print("   ⚠️ Výsledky nebyly nalezeny.")
    if not tabulka:
        print("   ⚠️ Tabulka nebyla nalezena.")
    if not statistiky:
        print("   ⚠️ Statistiky nebyly nalezeny.")

    return {
        "team_name": TEAM_NAME,
        "team_url": url,
        "season": season_label,
        "zapasy": zapasy,
        "tabulka": tabulka,
        "statistiky_hracu": statistiky
    }

def process_season(season_url, season_year, season_name):
    print(f"\n🌐 Sezóna {season_year} {season_name}: {season_url}")
    soup = fetch_soup(season_url)
    if not soup:
        print("❌ Nelze načíst sezónu.")
        return

    hrefs = []
    for block in soup.select(".component__list a[href]"):
        href = block.get("href")
        if re.search(r'/souteze/\d{4}-hanspaulska-liga.*[876]-[a-z]+/', href):
            full_url = f"{BASE_URL}{href}"
            hrefs.append(full_url)

    for href in hrefs:
        soup = fetch_soup(href)
        if not soup:
            continue
        team_link = soup.find("a", href=re.compile(fr"{TEAM_SLUG}/?$"))
        if team_link:
            team_url = f"{BASE_URL}{team_link['href']}"
            print(f"✅ Nalezen tým: {TEAM_NAME} -> {team_url}")
            print("   🔍 Zpracovávám detail týmu...")
            data = parse_team_details(team_url, f"{season_year} {season_name}")
            if data:
                file_name = f"tvoje_mama_{season_year}_{season_name}.json".replace(" ", "_")
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"💾 Uloženo: {file_name}")
            return  # Neprocházej dál, tým už jsme našli

def main():
    soup = fetch_soup(LIST_URL)
    if not soup:
        print("❌ Nelze načíst hlavní stránku.")
        return

    components = [c for c in soup.select(".component__wrap") if "Hanspaulská liga" in c.get_text()]
    competition_links = []

    for comp in components:
        for link in comp.find_all("a", href=True):
            href = link["href"]
            match = year_pattern.search(href)
            if match:
                year = int(match.group(1))
                if 2015 <= year <= 2024:
                    full_url = f"{BASE_URL}{href}"
                    season_name = "jaro" if "jaro" in href else "podzim"
                    competition_links.append((full_url, year, season_name))

    for url, year, name in competition_links:
        process_season(url, year, name)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import re
import json

BASE_URL = "https://www.psmf.cz"
TEAM_NAME = "Tvoje máma FC"
TEAM_SLUG = "tvoje-mama-fc"
HEADERS = {"User-Agent": "Mozilla/5.0"}

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
    return {
        "team_name": TEAM_NAME,
        "team_url": url,
        "season": season_label,
        "zapasy": parse_vysledky(soup),
        "tabulka": parse_tabulka(soup),
        "statistiky_hracu": parse_statistiky(soup)
    }

def test_2018_jaro():
    season_url = f"{BASE_URL}/souteze/2018-hanspaulska-liga-jaro/"
    print(f"\n🌐 Test sezóny: {season_url}")
    soup = fetch_soup(season_url)
    if not soup:
        print("❌ Nelze načíst stránku sezóny.")
        return

    
    group_links = [
        a['href'] for a in soup.select('.component__list a[href]')
        if re.search(r'/souteze/2018-hanspaulska-liga-jaro/[876]-[a-z]+/', a['href'])
    ]

    for relative_url in group_links:
        group_url = f"{BASE_URL}{relative_url}"
        group_soup = fetch_soup(group_url)
        if not group_soup:
            continue

        
        team_link = group_soup.find("a", href=re.compile(fr"{TEAM_SLUG}/?$"))
        if team_link and team_link.has_attr("href"):
            team_url = f"{BASE_URL}{team_link['href']}"
            print(f"✅ Nalezen tým: {team_url}")
            data = parse_team_details(team_url, "2018 jaro")
            if data:
                file_name = "tvoje_mama_2018_jaro_test.json"
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"💾 Uloženo: {file_name}")
            else:
                print("⚠️ Detailní data nebyla načtena.")
            break
    else:
        print("❌ Tým nebyl nalezen v žádné skupině.")

if __name__ == "__main__":
    test_2018_jaro()

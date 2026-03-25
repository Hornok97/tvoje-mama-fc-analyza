import json
import re

from finale import BASE_URL, TEAM_SLUG, TEAM_NAME, fetch_soup, parse_team_details


def test_2018_jaro():
    season_url = f"{BASE_URL}/souteze/2018-hanspaulska-liga-jaro/"
    print(f"\n🌐 Test sezóny: {season_url}")
    soup = fetch_soup(season_url)
    if not soup:
        print("Nelze načíst stránku sezóny.")
        return

    group_links = [
        a["href"] for a in soup.select(".component__list a[href]")
        if re.search(r"/souteze/2018-hanspaulska-liga-jaro/[876]-[a-z]+/", a["href"])
    ]

    for relative_url in group_links:
        group_url = f"{BASE_URL}{relative_url}"
        group_soup = fetch_soup(group_url)
        if not group_soup:
            continue

        team_link = group_soup.find("a", href=re.compile(fr"{TEAM_SLUG}/?$"))
        if team_link and team_link.has_attr("href"):
            team_url = f"{BASE_URL}{team_link['href']}"
            print(f"Nalezen tým: {team_url}")
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
        print("Tým nebyl nalezen v žádné skupině.")


if __name__ == "__main__":
    test_2018_jaro()

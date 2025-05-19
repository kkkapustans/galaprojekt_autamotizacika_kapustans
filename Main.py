import requests
import sys
import xml.etree.ElementTree as ET
from openpyxl import Workbook

def fetch_and_parse_rss(rss_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(rss_url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"HTTP kļūda, lejupielādējot RSS: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"XML parsēšanas kļūda: {e}", file=sys.stderr)
        sys.exit(1)

    items = root.findall(".//item")
    if not items:
        print("RSS tika lejupielādēts, bet tajā nav neviena <item>.", file=sys.stderr)
        sys.exit(1)

    return items

def print_top_items(items, n):
    print(f"Atrasti {len(items)} ziņu ieraksti. Izdrukājam pirmās {n}:")
    print("=" * 60)
    for i, item in enumerate(items[:n], 1):
        title = item.findtext("title", default="(bez virsraksta)").strip()
        link  = item.findtext("link",  default="(bez saites)").strip()
        date  = item.findtext("pubDate", default="(bez datuma)").strip()
        desc  = item.findtext("description", default="").replace("\n", " ").strip()
        snippet = desc[:200] + ("…" if len(desc) > 200 else "")

        print(f"\nZiņa #{i}")
        print(f"  Virsraksts: {title}")
        print(f"  Datums:     {date}")
        print(f"  Saite:      {link}")
        if snippet:
            print(f"  Apraksts:   {snippet}")

def write_to_excel(items, filename="rss_news.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "RSS News"

    # Header row
    ws.append(["#", "Virsraksts", "Datums", "Saite", "Apraksts (fragment)"])

    for i, item in enumerate(items, 1):
        title = item.findtext("title", default="(bez virsraksta)").strip()
        link  = item.findtext("link",  default="(bez saites)").strip()
        date  = item.findtext("pubDate", default="(bez datuma)").strip()
        desc  = item.findtext("description", default="").replace("\n", " ").strip()
        snippet = desc[:200] + ("…" if len(desc) > 200 else "")

        ws.append([i, title, date, link, snippet])

    try:
        wb.save(filename)
        print(f"\nDati tika veiksmīgi ierakstīti failā: {filename}")
    except Exception as e:
        print(f"Kļūda, saglabājot Excel failu: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        k = int(input("Ievadi, cik ziņu virsrakstu gribēsi redzēt (1–30): "))
    except ValueError:
        print("Kļūda: ievade nav skaitlis.", file=sys.stderr)
        sys.exit(1)

    if not (1 <= k <= 30):
        print("Kļūda: lūdzu ievadi skaitli no 1 līdz 30.", file=sys.stderr)
        sys.exit(1)

    RSS_URL = "https://www.lsm.lv/rss/?lang=lv&catid=14"
    items = fetch_and_parse_rss(RSS_URL)
    print_top_items(items, n=k)
    write_to_excel(items[:k])

#!/usr/bin/env python3
"""Rebuild the "open in winter 2026/27" and "closed" lists from api/bars.json.
Writes between <!-- winter-list:start --> / <!-- winter-list:end --> markers in
open-in-winter/index.html and christmas-new-year/index.html.
Run after editing js/bars-data.js and tools/build-agent-files.py (which regenerates api/bars.json)."""
import json, pathlib, html, re, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.artonbar.com"
bars = json.loads((ROOT / "api" / "bars.json").read_text())["bars"]
TOWNS = ["Lagos","Albufeira","Vilamoura","Faro","Tavira","Carvoeiro","Portimão","Quarteira","Sagres","Olhão"]
slug = {"Lagos":"lagos","Albufeira":"albufeira","Vilamoura":"vilamoura","Faro":"faro","Tavira":"tavira","Carvoeiro":"carvoeiro","Portimão":"portimao","Quarteira":"quarteira","Sagres":"sagres","Olhão":"olhao"}
open_w = [b for b in bars if b["open_in_winter"] and b.get("status") != "closed"]
seasonal = [b for b in bars if not b["open_in_winter"] and b.get("status") != "closed"]
closed = [b for b in bars if b.get("status") == "closed"]
def item(b):
    rel = b["url"].replace(SITE, "")
    return f'            <li><a href="{rel}" style="color:var(--cream);">{html.escape(b["name"])}</a> · {b["price_tier"]} · {", ".join(b["vibes"])}. {html.escape(b["desc"])}</li>'
blocks = []
for t in TOWNS:
    bs = sorted([b for b in open_w if b["town"] == t], key=lambda x: -x["rating"])
    if not bs: continue
    blocks.append(f'        <h3>{html.escape(t)} <a href="/{slug[t]}/" style="font-size:.7em;color:var(--cyan);font-family:var(--font-mono);letter-spacing:.08em;text-transform:uppercase;">town guide →</a></h3>\n          <ul>\n' + "\n".join(item(b) for b in bs) + "\n          </ul>")
lines = [f'            <li>❄️ <a href="{b["url"].replace(SITE,"")}" style="color:var(--cream);">{html.escape(b["name"])}</a>, {html.escape(b["town"])}: closed for winter 2026/27, seasonal, usually back in spring.</li>' for b in seasonal]
lines += [f'            <li>⛔ <a href="{b["url"].replace(SITE,"")}" style="color:var(--cream);">{html.escape(b["name"])}</a>, {html.escape(b["town"])}: reported closed (winter 2026). Review kept for reference.</li>' for b in closed]
closed_block = '        <h3>Closed for winter 2026/27</h3>\n          <ul>\n' + "\n".join(lines) + "\n          </ul>"
generated = (f'<!-- winter-list:start -->\n        <p style="font-size:.8rem;color:var(--muted-2);">Generated from the bar data on {datetime.date.today().isoformat()}: {len(open_w)} of {len(bars)} bars open in winter 2026/27, {len(seasonal)} seasonal, {len(closed)} reported closed. Winter hours shrink; check the bar\'s Instagram the day you go.</p>\n'
             + "\n".join(blocks) + "\n" + closed_block + "\n        <!-- winter-list:end -->")
for f in [ROOT / "open-in-winter" / "index.html", ROOT / "christmas-new-year" / "index.html"]:
    s = f.read_text()
    s2, k = re.subn(r"<!-- winter-list:start -->.*?<!-- winter-list:end -->", lambda m: generated, s, flags=re.S)
    assert k == 1, f
    f.write_text(s2)
print(f"winter list: {len(open_w)} open, {len(seasonal)} seasonal, {len(closed)} closed")

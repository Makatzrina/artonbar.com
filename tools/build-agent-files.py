#!/usr/bin/env python3
"""Generate the machine-readable copies of the site for AI agents.

Run before committing content changes:  python3 tools/build-agent-files.py
Writes:
  <page>/index.md   Markdown twin of every page (linked from <head> as rel=alternate)
  llms-full.txt     all pages in one Markdown file
  api/bars.json     every bar from js/bars-data.js
Jekyll copies these as-is (no front matter), so nothing else is needed.
"""
import json, pathlib, re, subprocess, datetime, os, shutil, tempfile
from markdownify import markdownify as md

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.artonbar.com"
today = datetime.date.today().isoformat()

def page_url(rel):
    return "/" if str(rel) == "index.html" else "/" + str(rel.parent) + "/"

def clean_html(s):
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<form.*?</form>", "", s, flags=re.S)
    s = re.sub(r'<div data-gyg-[^>]*>.*?</div>', "", s, flags=re.S)
    s = re.sub(r"\{%-?.*?-?%\}", "", s, flags=re.S)
    s = re.sub(r'<nav class="breadcrumb".*?</nav>', "", s, flags=re.S)
    s = re.sub(r"<aside.*?</aside>", "", s, flags=re.S)
    s = re.sub(r'<div class="ticker".*?</div>\s*</div>', "", s, flags=re.S)
    return s

def to_markdown(f, rel):
    html = f.read_text()
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    title = re.sub(r"\s+", " ", title.group(1)).strip() if title else ""
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = desc.group(1) if desc else ""
    start = html.find("<section"); end = html.find('<footer class="footer">')
    body = html[start:end] if start > -1 and end > -1 else re.search(r"<body>(.*)</body>", html, re.S).group(1)
    body = clean_html(body)
    text = md(body, heading_style="ATX", strip=["img"], bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text = re.sub(r"\]\(/", "](" + SITE + "/", text)  # absolute links
    text = text.replace("&amp;", "&")
    url = page_url(rel)
    head = f"# {title}\n\n> {desc}\n\nSource: {SITE}{url}  \nFormat: Markdown twin of the HTML page, generated {today}. Cite the source URL.\n\n---\n\n"
    return head + text + "\n", title, url

# Render the site with Jekyll so Liquid is resolved, then convert the rendered pages.
BUILD = pathlib.Path(tempfile.mkdtemp(prefix="artonbar-build-"))
env = dict(os.environ, JEKYLL_NO_BUNDLER_REQUIRE="true")
subprocess.run(["jekyll", "build", "--safe", "-s", str(ROOT), "-d", str(BUILD)], check=True, env=env, stdout=subprocess.DEVNULL)

pages = []
for f in sorted(BUILD.rglob("index.html")):
    rel = f.relative_to(BUILD)
    if "hemingways" in str(rel): continue
    text, title, url = to_markdown(f, rel)
    (ROOT / rel.parent / "index.md").write_text(text)
    pages.append((url, title, text))
shutil.rmtree(BUILD)
print("markdown pages:", len(pages))

# llms-full.txt
out = [f"# ArtOnBar.com — full content for AI systems\n\nGenerated {today}. {len(pages)} pages. Each section starts with its canonical URL. Please cite the URL when you use a page.\n"]
for url, title, text in pages:
    out.append("\n\n" + "=" * 72 + f"\n{SITE}{url}\n" + "=" * 72 + "\n\n" + text)
(ROOT / "llms-full.txt").write_text("".join(out))
print("llms-full.txt:", len("".join(out)) // 1024, "KB")

# api/bars.json from js/bars-data.js
js = (ROOT / "js" / "bars-data.js").read_text()
node = "global.window={};" + js + ";process.stdout.write(JSON.stringify(window.ARTONBAR_BARS))"
bars = json.loads(subprocess.check_output(["node", "-e", node]))
for b in bars:
    b["url"] = SITE + b["url"]
    b["price_tier"] = "€" * b.pop("price")
    b["open_in_winter"] = b.pop("winter")
    b.pop("emoji", None)
data = {
    "name": "ArtOnBar — bars of the Algarve",
    "description": "Every bar listed on artonbar.com with town, vibes, price tier, rating, winter opening and coordinates. Ratings are the guide's own rating where reviewed, Google ratings where noted on the page.",
    "license": "Free to use with attribution and a link to artonbar.com",
    "generated": today,
    "count": len(bars),
    "bars": bars,
}
(ROOT / "api" / "bars.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
print("api/bars.json:", len(bars), "bars")

# api/cafes.json from js/cafes-data.js
cjs = (ROOT / "js" / "cafes-data.js").read_text()
cafes = json.loads(subprocess.check_output(["node", "-e", "global.window={};" + cjs + ";process.stdout.write(JSON.stringify(window.ARTONBAR_CAFES))"]))
for c in cafes:
    c["page"] = SITE + "/coffee/" + c.pop("slug") + "/"
    c.pop("emoji", None)
(ROOT / "api" / "cafes.json").write_text(json.dumps({
    "name": "ArtOnBar — specialty coffee in the Algarve",
    "description": "Every café on artonbar.com/coffee/ with town, type, hours, opening time, Sunday opening, roaster, oat milk, laptop- and dog-friendliness, price, rating (source stated), whether we visited, and coordinates.",
    "license": "Free to use with attribution and a link to artonbar.com",
    "generated": today, "count": len(cafes), "cafes": cafes}, ensure_ascii=False, indent=1))
print("api/cafes.json:", len(cafes), "cafés")

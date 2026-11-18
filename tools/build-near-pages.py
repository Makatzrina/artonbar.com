#!/usr/bin/env python3
"""Generate the "bars near <landmark>" pages from api/bars.json.

Run:  python3 tools/build-near-pages.py   (then commit the generated near/ pages)
Distances are straight-line from the landmark coordinates; walking minutes assume
80 m/min plus 25% for streets. Every page says so.
"""
import json, math, pathlib, html, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.artonbar.com"
today = datetime.date.today().isoformat()
bars = json.loads((ROOT / "api" / "bars.json").read_text())["bars"]

LANDMARKS = [
 # slug, name, town, lat, lng, what it is (one line), who searches it
 ("praia-dona-ana", "Praia Dona Ana", "Lagos", 37.0912, -8.6700, "the postcard cliff beach south of Lagos old town", "You're on the beach, the sun is going, and the old town is a 15-minute walk uphill."),
 ("lagos-marina", "Lagos Marina", "Lagos", 37.1047, -8.6750, "the marina on the east side of the river, where most of the boat trips leave", "Cross the footbridge and you're in the old town in five minutes."),
 ("meia-praia", "Meia Praia", "Lagos", 37.1090, -8.6600, "the long beach east of the marina with the big hotels", "Everything worth drinking in is back across the marina."),
 ("vilamoura-marina", "Vilamoura Marina", "Vilamoura", 37.0720, -8.1225, "the marina boardwalk, where almost every bar in Vilamoura is", "If you're staying at a marina hotel, you don't need a taxi."),
 ("praia-da-rocha", "Praia da Rocha", "Portimão", 37.1190, -8.5380, "Portimão's big beach and the strip above it", "The strip is loud; the good bars are at either end of it."),
 ("albufeira-old-town", "Albufeira Old Town", "Albufeira", 37.0875, -8.2530, "the old centre around Praça Miguel Bombarda and the tunnel to the beach", "The strip is a 25-minute walk east; the old town has the better drinks."),
 ("albufeira-strip", "The Strip (Praia da Oura), Albufeira", "Albufeira", 37.0890, -8.2310, "Avenida Sá Carneiro, the bar strip above Praia da Oura", "Plenty of bars; this page is about the ones we'd actually send you to."),
 ("faro-old-town", "Faro Old Town", "Faro", 37.0135, -7.9350, "the walled Cidade Velha and the streets around the marina", "Faro's bar scene is small, walkable and cheaper than the coast."),
 ("faro-airport", "Faro Airport", "Faro", 37.0164, -7.9700, "the airport, 4 km west of the city as the crow flies and a 10–15 minute taxi around the lagoon", "Nothing worth drinking in is walkable from the terminal."),
 ("tavira-square", "Praça da República, Tavira", "Tavira", 37.1270, -7.6500, "Tavira's main square by the Roman bridge", "The best cocktail bar in the east is on this square."),
 ("carvoeiro-beach", "Carvoeiro Beach", "Carvoeiro", 37.0970, -8.4710, "the small town beach and the square above it", "Everything in Carvoeiro is within ten minutes of the sand."),
 ("quarteira-promenade", "Quarteira Promenade", "Quarteira", 37.0660, -8.1010, "the calçadão along the seafront", "Cheaper than Vilamoura, ten minutes away, and the sunset is the same."),
 ("olhao-market", "Olhão Market Halls", "Olhão", 37.0237, -7.8410, "the red-brick market halls on the Ria Formosa waterfront", "Golden hour on the waterfront is the reason to come."),
 ("cabo-sao-vicente", "Cabo de São Vicente", "Sagres", 37.0235, -8.9960, "the lighthouse at the south-western tip of Europe", "Watch the sunset here, then drive the ten minutes back into Sagres."),
]

def dist_km(a, b, c, d):
    R = 6371; p1, p2 = math.radians(a), math.radians(c); dp = math.radians(c - a); dl = math.radians(d - b)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def walk_min(km): return max(1, round(km * 1000 * 1.25 / 80))

def page(slug, name, town, lat, lng, what, line):
    rows = sorted(((dist_km(lat, lng, b["lat"], b["lng"]), b) for b in bars), key=lambda x: x[0])
    near = [(d, b) for d, b in rows if d <= 3.0]
    mode = "walk"
    if len(near) < 3:
        near = [(d, b) for d, b in rows if d <= 12.0][:8]; mode = "drive"
    near = near[:10]
    items = []
    for i, (d, b) in enumerate(near, 1):
        rel = b["url"].replace(SITE, "")
        if mode == "walk":
            how = f"{walk_min(d)} min on foot" if d <= 2.2 else f"{d:.1f} km, {walk_min(d)} min on foot or a short taxi"
        else:
            how = f"{d:.1f} km, about {max(10, round(d*3))} min by taxi"
        winter = "open in winter" if b["open_in_winter"] else "seasonal"
        items.append(f'''          <a href="{rel}" class="bar-list-item">
            <div class="bar-list-item__rank">{i}</div>
            <div>
              <div class="bar-list-item__name">{html.escape(b["name"])}</div>
              <div class="bar-list-item__sub">{how} · {html.escape(b["town"])} · {", ".join(b["vibes"])} · {winter}</div>
              <p class="bar-list-item__desc">{html.escape(b["desc"])}</p>
            </div>
            <div class="bar-list-item__meta">
              <span class="price-badge">{b["price_tier"]}</span>
              <span class="rating-badge">⭐ {b["rating"]:.1f}</span>
            </div>
          </a>''')
    closest = near[0][1]; cd = near[0][0]
    title = f"Bars near {name}: {len(near)} picks, by distance"
    if len(title) > 60: title = f"Bars near {name.split(',')[0]} ({town}) by distance"
    desc = f"The best bars near {name}, {town}, sorted by distance: {closest['name']} is the closest at {walk_min(cd) if mode=='walk' else round(cd*2)} min. Prices, ratings and what each one is for."
    desc = desc[:158]
    faq = [
      (f"Which bar is closest to {name}?", f"{closest['name']}, about {cd:.1f} km away ({(str(walk_min(cd)) + ' minutes on foot') if mode == 'walk' else (str(max(10, round(cd*3))) + ' minutes by taxi')}). {closest['desc']}"),
      (f"Can I walk to a bar from {name}?", ("Yes. " + ", ".join(b["name"] for d, b in near[:3]) + " are all within " + f"{near[min(2,len(near)-1)][0]:.1f} km.") if mode == "walk" else f"Not really. The nearest bar we'd recommend is {cd:.1f} km away; take a taxi or a Bolt."),
      ("Are these distances exact?", "They are straight-line distances from the landmark to the bar, with 25% added for streets. Real routes vary, so treat the minutes as a guide, not a promise."),
    ]
    ld = {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "ArtOnBar", "item": f"{SITE}/"},
          {"@type": "ListItem", "position": 2, "name": "Bars near", "item": f"{SITE}/near/"},
          {"@type": "ListItem", "position": 3, "name": name, "item": f"{SITE}/near/{slug}/"}]},
        {"@type": "ItemList", "name": f"Bars near {name}", "numberOfItems": len(near), "itemListOrder": "https://schema.org/ItemListOrderAscending",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": b["name"], "url": b["url"]} for i, (d, b) in enumerate(near, 1)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
      ]}
    faq_html = "\n".join(f'          <div class="faq__item"><div class="faq__q">{html.escape(q)}</div><div class="faq__a">{html.escape(a)}</div></div>' for q, a in faq)
    return f'''---
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{SITE}/near/{slug}/">
  <link rel="alternate" type="text/markdown" href="/near/{slug}/index.md" title="This page as Markdown">
  <link rel="alternate" type="application/json" href="/api/bars.json" title="All bars (JSON)">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/near/{slug}/">
  <meta property="og:site_name" content="ArtOnBar">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/og-image.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
  {json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-K767LQ3EEK"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-K767LQ3EEK');
  </script>
</head>
<body>

{{% include nav.html %}}

<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">ArtOnBar</a><span class="breadcrumb__sep">›</span><a href="/near/">Bars near</a><span class="breadcrumb__sep">›</span><span>{html.escape(name)}</span>
    </nav>
    <div class="page-hero__label">{html.escape(town)} · Sorted by distance</div>
    <h1>Bars near {html.escape(name)}</h1>
    <p class="page-hero__sub">{html.escape(name)} is {html.escape(what)}. {html.escape(line)} Below: every bar on this site within {"3 km" if mode == "walk" else "a short drive"}, closest first, with how long it takes to get there.</p>
    <p style="font-size:.8rem;color:var(--muted-2);margin-top:1rem;">Distances are straight-line from the landmark, with 25% added for streets. Generated from the bar coordinates on {today}.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="layout-sidebar">
      <div>
        <div class="section-header">
          <div class="section-header__label">Closest first</div>
          <h2>{len(near)} bars near {html.escape(name)}</h2>
        </div>
        <div class="bar-list">
{chr(10).join(items)}
        </div>

        <div class="article" style="margin-top:2rem;">
          <h2>FAQ</h2>
          <div class="faq">
{faq_html}
          </div>
        </div>
      </div>
      <aside class="layout-sidebar__sidebar">
        <div class="info-box" style="margin-bottom:1.5rem;">
          <h3>{html.escape(name)}</h3>
          <div class="info-box__row"><span class="info-box__label">Town</span><span class="info-box__val"><a href="/{town.lower().replace('ã','a').replace('ó','o')}/" style="color:var(--cyan);">{html.escape(town)}</a></span></div>
          <div class="info-box__row"><span class="info-box__label">Closest bar</span><span class="info-box__val">{html.escape(closest['name'])}</span></div>
          <div class="info-box__row"><span class="info-box__label">On foot</span><span class="info-box__val">{walk_min(cd)} min</span></div>
          <div class="info-box__row"><span class="info-box__label">Bars within reach</span><span class="info-box__val">{len(near)}</span></div>
        </div>
        <div class="info-box">
          <h3>See them on the map</h3>
          <div class="affiliate-links">
            <a href="/map/" class="affiliate-link"><span>🗺️ All bars on the map</span><span class="affiliate-link__label">Map</span></a>
            <a href="/bar-finder/?q={html.escape(town)}" class="affiliate-link"><span>🔍 Filter {html.escape(town)} bars</span><span class="affiliate-link__label">Bar Finder</span></a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>

{{% include footer.html %}}
<script src="/js/main.js"></script>
</body>
</html>
'''

for lm in LANDMARKS:
    out = ROOT / "near" / lm[0] / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(*lm))
print("near pages:", len(LANDMARKS))

# index page
cards = "\n".join(f'      <a href="/near/{s}/" class="town-tile"><div class="town-tile__emoji">📍</div><div class="town-tile__name">{html.escape(n)}</div><div class="town-tile__desc">{html.escape(t)} · {html.escape(w)}</div></a>' for s, n, t, la, lo, w, l in LANDMARKS)
(ROOT / "near" / "index.html").write_text(f'''---
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bars Near Me in the Algarve: Beaches, Marinas &amp; Squares</title>
  <meta name="description" content="Pick where you are (Praia Dona Ana, Lagos Marina, Vilamoura Marina, Praia da Rocha, Faro Old Town, Faro Airport and more) and get the closest bars we'd actually send you to, with walking times.">
  <link rel="canonical" href="{SITE}/near/">
  <link rel="alternate" type="text/markdown" href="/near/index.md" title="This page as Markdown">
  <meta property="og:title" content="Bars Near Me in the Algarve: Beaches, Marinas &amp; Squares">
  <meta property="og:description" content="Pick where you are and get the closest bars we'd actually send you to, with walking times.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE}/near/">
  <meta property="og:site_name" content="ArtOnBar">
  <meta property="og:image" content="{SITE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/og-image.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Bars near Algarve landmarks", "url": "{SITE}/near/", "isPartOf": {{"@type": "WebSite", "name": "ArtOnBar", "url": "{SITE}/"}}}}
  </script>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-K767LQ3EEK"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-K767LQ3EEK');
  </script>
</head>
<body>

{{% include nav.html %}}

<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">ArtOnBar</a><span class="breadcrumb__sep">›</span><span>Bars near</span>
    </nav>
    <div class="page-hero__label">Where are you right now?</div>
    <h1>Bars near you, by landmark</h1>
    <p class="page-hero__sub">"Bars near me" only works if we know where you are. Pick the beach, marina or square you're standing at and you get the closest bars we'd send you to, sorted by walking time.</p>
  </div>
</section>

<section class="section" id="landmarks">
  <div class="container">
    <div class="town-grid">
{cards}
    </div>
  </div>
</section>

{{% include footer.html %}}
<script src="/js/main.js"></script>
</body>
</html>
''')
print("near index written")

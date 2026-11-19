#!/usr/bin/env python3
"""Generate the Coffee section from js/cafes-data.js:
  coffee/index.html            hub (owner's intro + towns + finder link)
  coffee/<town>/index.html     one page per town (ranked list, honest alternatives, FAQ, schema)
  coffee/finder/index.html     Coffee Finder (filters by town / laptop / Sunday / early / roaster / oat / dogs)
Run after editing js/cafes-data.js. Then tools/build-agent-files.py (api/cafes.json, Markdown twins).
"""
import json, pathlib, subprocess, html, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.artonbar.com"
today = datetime.date.today().isoformat()
js = (ROOT / "js" / "cafes-data.js").read_text()
cafes = json.loads(subprocess.check_output(["node", "-e", "global.window={};" + js + ";process.stdout.write(JSON.stringify(window.ARTONBAR_CAFES))"]))

BARS_LINK = {"faro": ("/faro/", "Bars in Faro"), "olhao": ("/olhao/", "Bars in Olhão"), "tavira": ("/tavira/", "Bars in Tavira"), "loule": ("/quarteira/", "Bars in Quarteira & Vilamoura, the nearest"), "lagos": ("/lagos/", "Bars in Lagos"), "portimao": ("/portimao/", "Bars in Portimão")}
TOWNS = {
 "faro":    ("Faro", "Faro", "Faro has the most serious coffee in the east: two specialty bars, one of them roasting its own beans, plus the pastelarias where the city has breakfast standing at the counter."),
 "olhao":   ("Olhão", "Olhão", "Olhão has exactly one specialty coffee bar, and it's a good one. The rest is traditional, and some of that is excellent too, so the list is short and honest."),
 "tavira":  ("Tavira", "Tavira", "Tavira is the one town in the eastern Algarve where you can reliably get a properly made flat white. Three specialty bars, none of them open before nine, two of them only part of the week. Plan around the day."),
 "loule":   ("Loulé & Almancil", "Loulé", "In Loulé there are only two places with proper coffee: bean17 inside the market, open until about one in the afternoon, and Mellow, which has good coffee, good cakes, a nice room and cocktails later on. Everywhere else the coffee tastes burnt. In Almancil, The Showroom."),
 "lagos":   ("Lagos", "Lagos", "Lagos is the Algarve's coffee capital by a distance: roasters, laptop-friendly rooms, brunch queues. The problem isn't finding a flat white, it's choosing."),
 "portimao":("Portimão & Alvor", "Portimão", "Portimão's coffee lives in Praia da Rocha and Alvor rather than the city centre. Short list, but a real roaster is in it."),
}
INTRO = ("Good coffee is one of my hobbies, the kind I like to nurture, and I'm always glad to find a place that does a “proper” cup. "
         "In the eastern Algarve that's a bit of a gap, but here's what I found. Where a town has one real specialty bar, I say so, and I list the best traditional pastelarias as the honest alternative rather than padding the page. "
         "Hours are checked against the café's own listing on the date shown; winter hours shrink, so look at their Instagram before you drive.")

def feats(c):
    f = []
    if c.get("laptop"): f.append("💻 laptop ok")
    if c.get("sunday"): f.append("sun open")
    if c.get("opens") and c["opens"] <= "08:00": f.append(f"opens {c['opens']}")
    if c.get("roaster") or c.get("type") == "roaster": f.append("roasts own beans")
    if c.get("oat"): f.append("oat milk")
    if c.get("dog"): f.append("dogs ok")
    return f

def card(i, c):
    rating = f"⭐ {c['rating']:.1f}" if c.get("rating") else ("✔ visited" if c.get("visited") else "")
    tags = " ".join(f'<span class="on">{html.escape(x)}</span>' for x in feats(c))
    vis = '<span class="visited-tag">Visited</span> ' if c.get("visited") else ""
    sub = " · ".join(x for x in [c.get("address") or "", c.get("hours") or "", ("€" + str(c["price"]) if c.get("price") else "")] if x)
    link = c.get("website") or (f"https://www.instagram.com/{c['instagram'].lstrip('@')}/" if c.get("instagram") else "")
    name = f'<a href="{html.escape(link)}" target="_blank" rel="noopener" style="color:inherit;">{html.escape(c["name"])} ↗</a>' if link else html.escape(c["name"])
    return f'''          <div class="bar-list-item">
            <div class="bar-list-item__rank">{i}</div>
            <div>
              <div class="bar-list-item__name">{vis}{name}</div>
              <div class="bar-list-item__sub">{html.escape(sub)}</div>
              <p class="bar-list-item__desc">{html.escape(c["desc"])}</p>
              <div class="cafe-feats">{tags}</div>
            </div>
            <div class="bar-list-item__meta">
              <span class="rating-badge">{rating}</span>
            </div>
          </div>'''

HEAD = '''---
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{SITE}{url}">
  <link rel="alternate" type="text/markdown" href="{url}index.md" title="This page as Markdown">
  <link rel="alternate" type="application/json" href="/api/cafes.json" title="All cafés (JSON)">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}{url}">
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
  {ld}
  </script>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-K767LQ3EEK"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-K767LQ3EEK');
  </script>
</head>
<body>

{% include nav.html %}
'''
FOOT = '''
{% include footer.html %}
<script src="/js/main.js"></script>
</body>
</html>
'''
def head(title, desc, url, ld):
    return HEAD.replace("{title}", html.escape(title)).replace("{desc}", html.escape(desc)).replace("{SITE}", SITE).replace("{url}", url).replace("{ld}", json.dumps(ld, ensure_ascii=False, indent=2))

# ---------- town pages ----------
for slug, (label, main_town, intro) in TOWNS.items():
    cs = [c for c in cafes if c["slug"] == slug]
    spec = sorted([c for c in cs if c["type"] != "traditional"], key=lambda c: (not c.get("visited"), -(c.get("rating") or 0)))
    trad = sorted([c for c in cs if c["type"] == "traditional"], key=lambda c: -(c.get("rating") or 0))
    url = f"/coffee/{slug}/"
    title = f"Specialty Coffee in {label}: Where the Flat White Is Real"
    if len(title) > 60: title = f"Best Coffee in {label}: Specialty Cafés &amp; Honest Picks".replace("&amp;", "&")
    desc = (f"The specialty coffee in {label}, Algarve: {len(spec)} place{'s' if len(spec)!=1 else ''} that do a proper flat white, with hours, laptop and Sunday notes, and the best traditional pastelarias as the honest alternative.")[:158]
    laptop = [c for c in spec if c.get("laptop")]; sunday = [c for c in spec if c.get("sunday")]
    early = sorted([c for c in spec if c.get("opens")], key=lambda c: c["opens"])
    faq = [
      (f"Is there specialty coffee in {label}?", (f"Yes: " + ", ".join(c["name"] for c in spec) + ".") if spec else "Not that we could verify. The traditional pastelarias below are the honest alternative."),
      (f"Which café in {label} is good for working on a laptop?", (", ".join(c["name"] for c in laptop) + ".") if laptop else "None of them advertise it, and the specialty rooms are small. Treat a laptop session as a short one."),
      (f"Which cafés in {label} are open on Sunday?", (", ".join(c["name"] for c in sunday) + ".") if sunday else "The specialty bars we list are closed or unconfirmed on Sunday; the market and the pastelarias are your Sunday coffee."),
      (f"What time do the specialty cafés in {label} open?", (f"The earliest is {early[0]['name']} at {early[0]['opens']}." + (" Most open at nine or later." if len(early) > 1 else "")) if early else "Nine or later, as a rule. For a seven o'clock coffee, go to a pastelaria."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
      {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ArtOnBar", "item": f"{SITE}/"}, {"@type": "ListItem", "position": 2, "name": "Coffee", "item": f"{SITE}/coffee/"}, {"@type": "ListItem", "position": 3, "name": label, "item": f"{SITE}{url}"}]},
      {"@type": "ItemList", "name": f"Specialty coffee in {label}", "numberOfItems": len(spec), "itemListElement": [{"@type": "ListItem", "position": i, "item": {"@type": "CafeOrCoffeeShop", "name": c["name"], "address": {"@type": "PostalAddress", "streetAddress": c.get("address") or "", "addressLocality": c["town"], "addressCountry": "PT"}, **({"geo": {"@type": "GeoCoordinates", "latitude": c["lat"], "longitude": c["lng"]}} if c.get("lat") else {}), **({"url": c["website"]} if c.get("website") else {}), **({"aggregateRating": {"@type": "AggregateRating", "ratingValue": c["rating"], "bestRating": 5}} if c.get("rating") and c.get("rating_src") == "google" else {})}} for i, c in enumerate(spec, 1)]},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">ArtOnBar</a><span class="breadcrumb__sep">›</span><a href="/coffee/">Coffee</a><span class="breadcrumb__sep">›</span><span>{html.escape(label)}</span>
    </nav>
    <div class="page-hero__label">☕ Coffee · {html.escape(label)}</div>
    <h1>Specialty coffee in {html.escape(label)}</h1>
    <p class="page-hero__sub">{html.escape(intro)}</p>
    <p style="font-size:.8rem;color:var(--muted-2);margin-top:1rem;">Hours checked {today}. <span class="visited-tag">Visited</span> means we've had the coffee ourselves; the rest is from the cafés' own listings and recent reviews, with Google ratings where shown.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="layout-sidebar">
      <div>
        {{% include featured-slot.html town="{html.escape(label)}" kind="cafe" %}}
        <div class="section-header">
          <div class="section-header__label">The real thing</div>
          <h2>{len(spec)} place{'s' if len(spec)!=1 else ''} that make coffee properly</h2>
        </div>
        <div class="bar-list">
{chr(10).join(card(i, c) for i, c in enumerate(spec, 1)) if spec else '          <p class="finder-empty">Nothing verified yet for this town. Research in progress.</p>'}
        </div>
'''
    if trad:
        body += f'''
        <div class="section-header" style="margin-top:3rem;">
          <div class="section-header__label">The honest alternative</div>
          <h2>Traditional, and good at it</h2>
          <p>Not specialty, and not pretending to be. These open early, serve a decent bica and the pastries the town actually eats.</p>
        </div>
        <div class="bar-list">
{chr(10).join(card(i, c) for i, c in enumerate(trad, 1))}
        </div>
'''
    body += f'''
        <div class="article" style="margin-top:2rem;">
          <h2>FAQ</h2>
          <div class="faq">
{chr(10).join(f'            <div class="faq__item"><div class="faq__q">{html.escape(q)}</div><div class="faq__a">{html.escape(a)}</div></div>' for q, a in faq)}
          </div>
        </div>
      </div>
      <aside class="layout-sidebar__sidebar">
        <div class="info-box" style="margin-bottom:1.5rem;">
          <h3>{html.escape(label)} coffee, in short</h3>
          <div class="info-box__row"><span class="info-box__label">Specialty</span><span class="info-box__val">{len(spec)}</span></div>
          <div class="info-box__row"><span class="info-box__label">Earliest</span><span class="info-box__val">{html.escape(early[0]['opens'] + ' · ' + early[0]['name']) if early else '-'}</span></div>
          <div class="info-box__row"><span class="info-box__label">Sunday</span><span class="info-box__val">{html.escape(', '.join(c['name'] for c in sunday)) if sunday else 'see pastelarias'}</span></div>
          <div class="info-box__row"><span class="info-box__label">Laptop</span><span class="info-box__val">{html.escape(', '.join(c['name'] for c in laptop)) if laptop else '-'}</span></div>
        </div>
        <div class="info-box" style="margin-bottom:1.5rem;">
          <h3>And tonight</h3>
          <div class="affiliate-links">
            <a href="{BARS_LINK[slug][0]}" class="affiliate-link"><span>🍸 {html.escape(BARS_LINK[slug][1])}</span><span class="affiliate-link__label">Guide</span></a>
            <a href="/coffee/finder/?town={html.escape(main_town)}" class="affiliate-link"><span>🔍 Filter these cafés</span><span class="affiliate-link__label">Coffee Finder</span></a>
            <a href="/map/#coffee" class="affiliate-link"><span>🗺️ On the map</span><span class="affiliate-link__label">Map</span></a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>
'''
    out = ROOT / "coffee" / slug / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(title, desc, url, ld) + body + FOOT)

# ---------- hub ----------
spec_all = [c for c in cafes if c["type"] != "traditional"]
tiles = "\n".join(f'      <a href="/coffee/{slug}/" class="town-tile"><div class="town-tile__emoji">☕</div><div class="town-tile__name">{html.escape(label)}</div><div class="town-tile__desc">{len([c for c in spec_all if c["slug"]==slug])} specialty · {len([c for c in cafes if c["slug"]==slug and c["type"]=="traditional"])} traditional</div></a>' for slug, (label, mt, intro) in TOWNS.items())
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ArtOnBar", "item": f"{SITE}/"}, {"@type": "ListItem", "position": 2, "name": "Coffee", "item": f"{SITE}/coffee/"}]},
  {"@type": "CollectionPage", "name": "Specialty coffee in the Algarve", "url": f"{SITE}/coffee/", "description": "Where the coffee is made properly in the Algarve, town by town, with the eastern Algarve covered honestly.", "isPartOf": {"@type": "WebSite", "name": "ArtOnBar", "url": f"{SITE}/"}},
  {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "Where is the best specialty coffee in the Algarve?", "acceptedAnswer": {"@type": "Answer", "text": "Lagos has the most choice, with roasters and laptop-friendly cafés. In the east, Faro has two specialty bars, Tavira three, Olhão one, and Loulé two (bean17 in the market and Mellow). Vila Real de Santo António has none we could verify."}},
    {"@type": "Question", "name": "Is there good coffee in the eastern Algarve?", "acceptedAnswer": {"@type": "Answer", "text": "Some, and it is worth knowing where. Faro, Tavira, Olhão and Loulé each have at least one place that makes a proper flat white; most of them open at nine or later and several close early or part of the week."}},
  ]}]}
hub = head("Specialty Coffee in the Algarve: Town by Town, Honestly", "Where the coffee is made properly in the Algarve: Lagos, Faro, Olhão, Tavira, Loulé, Almancil and Portimão. Specialty bars, roasters, laptop-friendly rooms, Sunday openers, and the honest alternative where there is none.", "/coffee/", ld) + f'''
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">ArtOnBar</a><span class="breadcrumb__sep">›</span><span>Coffee</span>
    </nav>
    <div class="page-hero__label">☕ Bars by night, coffee by day</div>
    <h1>Specialty coffee in the Algarve,<br>town by town</h1>
    <p class="page-hero__sub">{html.escape(INTRO)}</p>
    <div class="hero__btns" style="margin-top:1.5rem;">
      <a href="/coffee/finder/" class="btn btn--primary">🔍 Coffee Finder</a>
      <a href="/map/#coffee" class="btn btn--outline">🗺️ Cafés on the map</a>
    </div>
  </div>
</section>

<section class="section" id="towns">
  <div class="container">
    <div class="section-header">
      <div class="section-header__label">By town</div>
      <h2>Where do you want your coffee?</h2>
    </div>
    <div class="town-grid">
{tiles}
    </div>
  </div>
</section>

<section class="section--sm">
  <div class="container">
    <div class="how-strip">
      <div class="how-strip__item"><h3>Proper means proper.</h3><p>Fresh beans, a machine someone cleans, milk that's steamed rather than boiled. If a town has one place like that, the page says one.</p></div>
      <div class="how-strip__item"><h3>Hours matter more than hype.</h3><p>Half the good cafés in the east open at nine and close by two, or trade three days a week. Every listing shows when, and when it was checked.</p></div>
      <div class="how-strip__item"><h3>Winter is coffee season.</h3><p>The bars go quiet from November, the cafés don't. This section is for the people who live here, work here, or ride here when it's 17 degrees and sunny.</p></div>
    </div>
  </div>
</section>
''' + FOOT
(ROOT / "coffee" / "index.html").write_text(hub)

# ---------- finder ----------
finder = head("Coffee Finder: Specialty Cafés in the Algarve, Filtered", "Filter every café on ArtOnBar by town, laptop-friendly, open on Sunday, opens before 8, roasts its own beans, oat milk or dog-friendly.", "/coffee/finder/", {"@context": "https://schema.org", "@type": "WebPage", "name": "Coffee Finder", "url": f"{SITE}/coffee/finder/", "isPartOf": {"@type": "WebSite", "name": "ArtOnBar", "url": f"{SITE}/"}}) + '''
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">ArtOnBar</a><span class="breadcrumb__sep">›</span><a href="/coffee/">Coffee</a><span class="breadcrumb__sep">›</span><span>Coffee Finder</span>
    </nav>
    <div class="page-hero__label">☕ Every café on the site, one screen</div>
    <h1>Coffee Finder</h1>
    <p class="page-hero__sub">Pick a town, say what you need (a laptop seat, a Sunday opener, a seven o'clock start, a roaster), and get the shortlist.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="finder-filters">
      <h3>Search</h3>
      <input type="search" id="f-search" class="finder-search" placeholder="Café name, town, or thing — roaster, laptop, Faro…" aria-label="Search cafés">
      <h3>Town</h3><div id="f-towns"></div>
      <h3>I need</h3><div id="f-feats"></div>
      <h3>Type</h3><div id="f-type"></div>
    </div>
    <div class="finder-count" id="f-count"></div>
    <div id="f-results"></div>
  </div>
</section>

<script src="/js/cafes-data.js"></script>
<script>
(function(){
  var cafes = window.ARTONBAR_CAFES;
  var FEATS = {laptop:'💻 Laptop-friendly', sunday:'Open Sunday', early:'Opens before 8', roaster:'Roasts own beans', oat:'Oat milk', dog:'Dog-friendly', visited:'✔ We visited'};
  var state = {town:null, type:null, feats:{}, q:''};
  var params = new URLSearchParams(location.search);
  var searchEl = document.getElementById('f-search');
  if (params.get('q')) { state.q = params.get('q').toLowerCase(); searchEl.value = params.get('q'); }
  if (params.get('town')) state.town = params.get('town');
  searchEl.addEventListener('input', function(){ state.q = this.value.toLowerCase().trim(); render(); });
  var towns = []; cafes.forEach(function(c){ if(towns.indexOf(c.town)<0) towns.push(c.town); }); towns.sort();
  function chip(label, group, value){ var el=document.createElement('button'); el.className='finder-chip'; el.textContent=label; el.dataset.group=group; el.dataset.value=value;
    el.onclick=function(){ if(group==='feats'){ state.feats[value]=!state.feats[value]; } else { state[group]=(state[group]===value)?null:value; } render(); }; return el; }
  var tEl=document.getElementById('f-towns'); tEl.appendChild(chip('All towns','town','__all')); towns.forEach(function(t){ tEl.appendChild(chip(t,'town',t)); });
  var fEl=document.getElementById('f-feats'); Object.keys(FEATS).forEach(function(k){ fEl.appendChild(chip(FEATS[k],'feats',k)); });
  var yEl=document.getElementById('f-type'); yEl.appendChild(chip('Any','type','__all')); [['specialty','Specialty'],['roaster','Roaster'],['traditional','Traditional pastelaria']].forEach(function(p){ yEl.appendChild(chip(p[1],'type',p[0])); });
  function has(c,k){ if(k==='early') return !!c.opens && c.opens <= '08:00'; if(k==='roaster') return c.roaster===true || c.type==='roaster'; return c[k]===true; }
  function render(){
    document.querySelectorAll('.finder-chip').forEach(function(el){ var g=el.dataset.group, v=el.dataset.value;
      if(g==='feats'){ el.classList.toggle('active', !!state.feats[v]); }
      else if(v==='__all'){ el.classList.toggle('active', state[g]===null||state[g]==='__all'); if(state[g]==='__all') state[g]=null; }
      else { el.classList.toggle('active', state[g]===v); } });
    var out = cafes.filter(function(c){
      if(state.q){ var hay=(c.name+' '+c.town+' '+c.desc+' '+c.type).toLowerCase(); if(hay.indexOf(state.q)<0) return false; }
      if(state.town && c.town!==state.town) return false;
      if(state.type && c.type!==state.type) return false;
      for(var k in state.feats){ if(state.feats[k] && !has(c,k)) return false; }
      return true;
    }).sort(function(a,b){ if(!!a.visited!==!!b.visited) return a.visited?-1:1; return (b.rating||0)-(a.rating||0); });
    document.getElementById('f-count').textContent = out.length+' caf'+(out.length===1?'é':'és')+' found';
    var res=document.getElementById('f-results'); res.innerHTML='';
    if(!out.length){ res.innerHTML='<div class="finder-empty">Nothing matches. Remove a filter, or tell us about a café we missed.</div>'; return; }
    out.forEach(function(c){
      var tags = Object.keys(FEATS).filter(function(k){ return k!=='visited' && has(c,k); }).map(function(k){ return '<span class="on">'+FEATS[k]+'</span>'; }).join('');
      var a=document.createElement('a'); a.className='finder-card'; a.href='/coffee/'+c.slug+'/';
      a.innerHTML='<div class="finder-card__emoji">'+c.emoji+'</div><div><div class="finder-card__name">'+(c.visited?'<span class="visited-tag">Visited</span> ':'')+c.name+'</div>'+
        '<div class="finder-card__meta">📍 '+c.town+(c.hours?' · '+c.hours:'')+(c.price?' · €'+c.price:'')+' · '+(c.type==='traditional'?'traditional':'specialty')+'</div>'+
        '<p class="finder-card__desc">'+c.desc+'</p><div class="cafe-feats">'+tags+'</div></div>'+
        '<div class="finder-card__badges">'+(c.rating?'⭐ '+c.rating.toFixed(1):'')+'</div>';
      res.appendChild(a);
    });
  }
  render();
})();
</script>
''' + FOOT
(ROOT / "coffee" / "finder").mkdir(parents=True, exist_ok=True)
(ROOT / "coffee" / "finder" / "index.html").write_text(finder)
print("coffee pages:", len(TOWNS), "towns + hub + finder;", len(cafes), "cafés in data")

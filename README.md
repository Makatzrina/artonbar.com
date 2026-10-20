# artonbar.com

Static site (GitHub Pages, custom domain via `CNAME`). No build step: every page is a hand-editable `index.html`.

## What's where
- `index.html` — homepage. Town tiles are grouped west → central → east.
- `/<town>/index.html` — 19 town hubs (`/towns/` lists them all). Bar review pages live under their town, e.g. `/lagos/forbidden-door/`.
- `/sunset-bars/`, `/rooftop-bars/`, … — vibe guides.
- `/bar-finder/`, `/map/` — interactive tools, driven by **`js/bars-data.js`** (one line per bar).
- `js/config.js` — **the only file to edit to turn on revenue** (affiliate IDs, AdSense).
- `js/monetise.js` — rewrites Booking/GetYourGuide links with your IDs, adds `rel="sponsored"`, sends a GA4 `affiliate_click` event, loads AdSense into `.ad-slot` placeholders when configured.
- `llms.txt`, `llms-full.txt` — AI-readable site summary and full dataset (what ChatGPT/Claude/Perplexity crawlers read first).
- `sitemap.xml`, `feed.xml`, `robots.txt` — regenerate the first two when you add pages (see below).

## Adding a bar (5 minutes)
1. Add a line to `js/bars-data.js` (copy a neighbour; keep `town` identical to the town page's name). The finder and map pick it up automatically.
2. Add the bar to the ranked list on the town page, and to any vibe guide it fits.
3. Add a line for it in `llms-full.txt` under the town, and bump the `lastmod` for the town page in `sitemap.xml`.

## Adding a town
Copy `/alvor/index.html`, change the title/description/canonical/H1/intro/bars/FAQ, keep the JSON-LD in sync, add a tile on the homepage and `/towns/`, add the link to the footer on all pages, add it to `sitemap.xml`, `feed.xml` and `llms.txt`.

## Revenue setup (do these in order)
1. **GetYourGuide** — the site has used two partner-ID spellings (`EAQF7O2` and `EAQF702`). Log in to partner.getyourguide.com, copy the real one, set it in `js/config.js`. Everything is rewritten to match at page load.
2. **Booking.com Affiliate Partner** — apply at booking.com/affiliate-program. When approved, put your `aid` number in `js/config.js`. Every Booking link on the site (hotels per town) then earns.
3. **Google AdSense** — apply with the site (it now has the privacy policy, disclosure page and contact page AdSense requires). When approved: set `adsense_client` in `js/config.js`, create `/ads.txt` with the line AdSense gives you (`google.com, pub-XXXX, DIRECT, f08c47fec0942fa0`), optionally create two ad units and put their slot IDs in `config.js`. Ad slots exist in every sidebar and before the FAQ on hub pages; they stay hidden until configured.
4. **Direct sales** — `/advertise/` lists Featured Listing (€49/mo), Featured + Review (€149 + €49/mo) and Sponsored Post (€99). Change prices there. Enquiries arrive via the existing FormSubmit forms.
5. **Newsletter** — the form posts to FormSubmit. For a real list, swap the form action for Mailchimp/Beehiiv in `js/main.js`.

## Tracking what earns
GA4 → Reports → Engagement → Events → `affiliate_click` (dimensions: `link_domain`, `page_path`). Compare with your partner dashboards monthly.

## The AI-powered recommendations
The site's AI-powered recommendations run on a token-based AI model provided by [antseed](https://antseed.com/), which handles the natural language processing behind the search and suggestion features.

// ArtOnBar — affiliate link decoration, outbound click tracking and ad-slot loader. Config lives in /js/config.js.
(function(){
  var cfg = window.ARTONBAR_CONFIG || {}, aff = cfg.affiliates || {}, ads = cfg.ads || {};
  function setParam(url, k, v){ try { var u = new URL(url, location.href); u.searchParams.set(k, v); return u.toString(); } catch (e) { return url; } }
  function markSponsored(a){
    var r = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
    ['sponsored','noopener'].forEach(function(x){ if (r.indexOf(x) < 0) r.push(x); });
    a.setAttribute('rel', r.join(' '));
    if (!a.getAttribute('target')) a.setAttribute('target', '_blank');
  }
  var AFFILIATE = /(^|\.)(booking\.com|getyourguide\.com|amazon\.[a-z.]+)$/i;
  Array.prototype.forEach.call(document.querySelectorAll('a[href]'), function(a){
    var host; try { host = new URL(a.href, location.href).hostname; } catch (e) { return; }
    if (!AFFILIATE.test(host)) return;
    var h = a.href;
    if (/booking\.com$/i.test(host)) {
      if (aff.booking_aid) { h = setParam(h, 'aid', aff.booking_aid); if (aff.booking_label) h = setParam(h, 'label', aff.booking_label); }
    } else if (/getyourguide\.com$/i.test(host)) {
      if (aff.getyourguide_partner_id) { h = setParam(h, 'partner_id', aff.getyourguide_partner_id); h = setParam(h, 'utm_medium', 'online_publisher'); }
    } else if (aff.amazon_tag) { h = setParam(h, 'tag', aff.amazon_tag); }
    a.href = h; markSponsored(a);
  });
  // Outbound affiliate clicks → GA4 event "affiliate_click" (see Reports → Engagement → Events).
  document.addEventListener('click', function(e){
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null; if (!a) return;
    var host; try { host = new URL(a.href, location.href).hostname; } catch (err) { return; }
    if (AFFILIATE.test(host) && typeof gtag === 'function') {
      gtag('event', 'affiliate_click', { link_url: a.href, link_domain: host, page_path: location.pathname, link_text: (a.textContent || '').trim().slice(0, 80) });
    }
  }, true);
  // Ads: only when a publisher ID is configured. Slots are hidden by CSS otherwise, so nothing shifts.
  var slots = document.querySelectorAll('.ad-slot');
  if (ads.adsense_client && slots.length) {
    document.documentElement.classList.add('ads-on');
    var s = document.createElement('script'); s.async = true; s.crossOrigin = 'anonymous';
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(ads.adsense_client);
    document.head.appendChild(s);
    Array.prototype.forEach.call(slots, function(el){
      var name = el.getAttribute('data-ad') || 'sidebar';
      var ins = document.createElement('ins'); ins.className = 'adsbygoogle'; ins.style.display = 'block';
      ins.setAttribute('data-ad-client', ads.adsense_client);
      var slot = (ads.slots || {})[name]; if (slot) ins.setAttribute('data-ad-slot', slot);
      if (name === 'in-article') { ins.setAttribute('data-ad-format', 'fluid'); ins.setAttribute('data-ad-layout', 'in-article'); }
      else { ins.setAttribute('data-ad-format', 'auto'); ins.setAttribute('data-full-width-responsive', 'true'); }
      el.appendChild(ins);
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }
})();

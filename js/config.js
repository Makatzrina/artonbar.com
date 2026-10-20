// ArtOnBar — site configuration. This is the ONLY file you need to edit to switch on revenue.
// It is loaded on every page before /js/monetise.js.
window.ARTONBAR_CONFIG = {
  affiliates: {
    // GetYourGuide partner ID. Check it in partner.getyourguide.com → "Partner ID".
    // NOTE: the site previously used two spellings (EAQF7O2 with a letter O, and EAQF702 with a zero).
    // Only one earns commission. Confirm which and set it here; every GYG link on the site is rewritten to match.
    getyourguide_partner_id: "EAQF7O2",
    // Booking.com Affiliate Partner ID (the number after aid= in your tracking links). Empty = plain links, no commission.
    // Apply at https://www.booking.com/affiliate-program/v2/index.html (approval usually takes a few days).
    booking_aid: "",
    booking_label: "artonbar",
    // Amazon Associates tag (e.g. "artonbar-21" for amazon.es/.co.uk). Only used if you add Amazon links.
    amazon_tag: ""
  },
  // Direct sales. Create Stripe Payment Links (dashboard.stripe.com → Payment links) or PayPal.me links and paste them here.
  // When a link is set, the matching button on /advertise/ goes straight to checkout instead of the enquiry form.
  payment_links: {
    "featured": "",          // €49 / month recurring
    "featured-review": "",   // €149 one-off (set up the €49/mo as a second link or an invoice)
    "sponsored-post": "",    // €99 one-off
    "event": ""              // €29 one-off
  },
  sales_email: "makatzrina@gmail.com",
  ads: {
    // Google AdSense publisher ID, e.g. "ca-pub-1234567890123456". Empty = ad slots stay hidden (no layout shift, nothing loads).
    // Once approved: (1) set this, (2) create /ads.txt with the line AdSense gives you, (3) optionally add slot IDs below.
    adsense_client: "",
    slots: { "sidebar": "", "in-article": "" }
  }
};

// ArtOnBar.com — Main JS

// Mobile nav toggle
const hamburger = document.querySelector('.nav__hamburger');
const navLinks  = document.querySelector('.nav__links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const open = navLinks.classList.contains('open');
    hamburger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  // Close on link click
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navLinks.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

// Newsletter form (no backend — shows confirmation message)
const newsletterForm = document.querySelector('.newsletter__form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', e => {
    e.preventDefault();
    const email = newsletterForm.querySelector('input[type="email"]').value;
    if (email) {
      newsletterForm.innerHTML = '<p style="color:var(--pink);font-weight:600;font-size:1rem;font-family:var(--font-mono);letter-spacing:.06em;text-transform:uppercase;">✓ You\'re in. See you next month.</p>';
    }
  });
}

// Contact / submit form
const contactForm = document.querySelector('.js-contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', e => {
    e.preventDefault();
    contactForm.innerHTML = '<p style="color:var(--pink);font-weight:600;font-size:1rem;font-family:var(--font-mono);letter-spacing:.06em;text-transform:uppercase;padding:2rem 0;">✓ Got it — I\'ll reply within 48 hours.</p>';
  });
}

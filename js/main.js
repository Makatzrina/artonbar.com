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
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navLinks.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

const FORMSUBMIT_URL = 'https://formsubmit.co/ajax/makatzrina@gmail.com';

// Newsletter form
const newsletterForm = document.querySelector('.newsletter__form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async e => {
    e.preventDefault();
    const emailInput = newsletterForm.querySelector('input[type="email"]');
    if (!emailInput.value) return;

    const btn = newsletterForm.querySelector('button');
    btn.disabled = true;
    btn.textContent = 'Subscribing...';

    try {
      await fetch(FORMSUBMIT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ email: emailInput.value, _subject: 'ArtOnBar Newsletter Signup' })
      });
    } catch (_) {}

    newsletterForm.innerHTML = '<p style="color:var(--pink);font-weight:600;font-size:1rem;font-family:var(--font-mono);letter-spacing:.06em;text-transform:uppercase;">&#x2713; You\'re in. See you next month.</p>';
  });
}

// Contact / submit-a-bar forms
document.querySelectorAll('.js-contact-form').forEach(form => {
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const btn = form.querySelector('[type="submit"]');
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Sending...';

    const subject = form.dataset.formSubject || 'ArtOnBar Enquiry';
    const data = Object.fromEntries(new FormData(form));
    data._subject = subject;

    try {
      const res = await fetch(FORMSUBMIT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        form.innerHTML = '<p style="color:var(--pink);font-weight:600;font-size:1rem;font-family:var(--font-mono);letter-spacing:.06em;text-transform:uppercase;padding:2rem 0;">&#x2713; Got it — I\'ll reply within 48 hours.</p>';
      } else {
        throw new Error('Network response not ok');
      }
    } catch (_) {
      btn.disabled = false;
      btn.textContent = originalText;
      const err = document.createElement('p');
      err.style.cssText = 'color:var(--pink);margin-top:.75rem;font-size:.9rem;';
      err.textContent = 'Something went wrong — please try again or email makatzrina@gmail.com directly.';
      btn.parentElement.after(err);
    }
  });
});

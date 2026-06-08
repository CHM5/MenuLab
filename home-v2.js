document.addEventListener('DOMContentLoaded', () => {
  // CTA tracking hooks (simple + static friendly)
  document.querySelectorAll('[data-cta="demo"]').forEach((el) => {
    el.addEventListener('click', () => {
      try {
        if (window.gtag) {
          window.gtag('event', 'click_solicitar_demo', { location: el.dataset.location || 'unknown' });
        }
      } catch (_) {
        // no-op
      }
    });
  });
});

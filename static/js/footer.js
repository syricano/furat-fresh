// Smooth scroll to top + show button after scroll + footer progress
(() => {
  const btn = document.querySelector('[data-scroll-top]');
  const bar = document.querySelector('.footer-progress .bar');

  const onScroll = () => {
    const y = window.scrollY || document.documentElement.scrollTop || 0;
    if (btn) btn.hidden = y < 160;
    if (bar) {
      const doc = document.documentElement;
      const max = (doc.scrollHeight - doc.clientHeight) || 1;
      const pct = Math.min(100, Math.max(0, (y / max) * 100));
      bar.style.width = pct + '%';
    }
  };

  btn?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();


// Smooth scroll to top + show button after scroll
(() => {
  const btn = document.querySelector('[data-scroll-top]');
  const onScroll = () => { if (btn) btn.hidden = (window.scrollY || 0) < 160; };
  btn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
})();

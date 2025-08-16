// Parallax the page background and stage hero in smoothly
document.addEventListener('DOMContentLoaded', () => {
  // Parallax body background (subtle)
  const onScroll = () => {
    const y = Math.max(0, window.scrollY);
    document.body.style.backgroundPosition = `center ${-y * 0.12}px`;
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Stagger title and button entrance
  const title = document.querySelector('main .display-4.logo-font');
  const cta = document.querySelector('.shop-now-button');
  if (title) title.style.animationDelay = '80ms';
  if (cta) {
    cta.style.animation = 'rise .5s ease-out both';
    cta.style.animationDelay = '140ms';
    // Keyboard activation polish
    cta.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cta.click(); }
    });
  }
});

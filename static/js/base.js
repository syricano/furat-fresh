// Effects for navbar + global helpers
(() => {
  // Header elevation without changing layout
  const header = document.querySelector('header');
  const setHdr = () => header?.toggleAttribute('data-elevated', window.scrollY > 2);
  setHdr(); window.addEventListener('scroll', setHdr, { passive: true });


  // Ripple for all .btn
  document.addEventListener('click', e => {
    const btn = e.target.closest('.btn');
    if (!btn) return;
    const r = document.createElement('span');
    const rect = btn.getBoundingClientRect();
    const s = Math.max(rect.width, rect.height);
    Object.assign(r.style, {
      position:'absolute', left:`${e.clientX - rect.left - s/2}px`, top:`${e.clientY - rect.top - s/2}px`,
      width:`${s}px`, height:`${s}px`, borderRadius:'50%', background:'rgba(255,255,255,.25)',
      transform:'scale(0)', transition:'transform 300ms ease, opacity 500ms ease', pointerEvents:'none'
    });
    if (!/relative|absolute|fixed/.test(getComputedStyle(btn).position)) btn.style.position = 'relative';
    btn.appendChild(r);
    requestAnimationFrame(()=>{ r.style.transform='scale(1)'; r.style.opacity='0'; });
    setTimeout(()=> r.remove(), 500);
  });

  // Fallback: mark current path active if server didn’t
  const cur = location.pathname.replace(/\/+$/,'') || '/';
  document.querySelectorAll('.navbar .nav-link[href]').forEach(a => {
    try {
      const href = new URL(a.href, location.origin).pathname.replace(/\/+$/,'') || '/';
      if (href === cur) a.classList.add('active');
    } catch(_) {}
  });
})();

// Ripple on .btn-black
document.addEventListener('click', e => {
  const btn = e.target.closest('.btn-black');
  if (!btn) return;
  const ripple = document.createElement('span');
  const rect = btn.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  ripple.style.position = 'absolute';
  ripple.style.left = `${e.clientX - rect.left - size/2}px`;
  ripple.style.top = `${e.clientY - rect.top - size/2}px`;
  ripple.style.width = ripple.style.height = `${size}px`;
  ripple.style.borderRadius = '50%';
  ripple.style.background = 'rgba(255,255,255,.25)';
  ripple.style.pointerEvents = 'none';
  ripple.style.transform = 'scale(0)';
  ripple.style.transition = 'transform 300ms ease, opacity 500ms ease';
  btn.appendChild(ripple);
  requestAnimationFrame(() => { ripple.style.transform = 'scale(1)'; ripple.style.opacity = '0'; });
  setTimeout(() => ripple.remove(), 500);
});

// Mark submit as dirty when any field changes
(() => {
  const form = document.getElementById('profile-update-form');
  if (!form) return;
  const submit = form.querySelector('button[type="submit"]');
  if (!submit) return;
  const markDirty = () => submit.classList.add('dirty');
  form.addEventListener('input', markDirty, { once: true });
})();

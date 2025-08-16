(function(){
  const stack = document.getElementById('toast-stack');
  if (!stack) return;

  const payloadEl = document.getElementById('django-messages');
  let msgs = [];
  if (payloadEl && payloadEl.textContent.trim()) {
    try { msgs = JSON.parse(payloadEl.textContent); } catch(_) { msgs = []; }
  }

  function spawnToast(obj){
    const tag = (obj.tag || 'info').toString();
    const el = document.createElement('div');
    el.className = 'toast ' + (tag.includes('success')?'success':tag.includes('error')?'error':tag.includes('warning')?'warning':'info');
    el.innerHTML = '<button class="close" aria-label="Close" title="Close">&times;</button><div>'+obj.text+'</div>';
    stack.appendChild(el);
    requestAnimationFrame(()=>el.classList.add('show'));

    let timer = setTimeout(dismiss, 4000);
    function dismiss(){ el.classList.remove('show'); setTimeout(()=>el.remove(), 200); }
    el.querySelector('.close').addEventListener('click', ()=>{ clearTimeout(timer); dismiss(); });
    el.addEventListener('mouseenter', ()=>clearTimeout(timer));
    el.addEventListener('mouseleave', ()=>timer=setTimeout(dismiss, 1500));
  }

  msgs.forEach(spawnToast);
})();

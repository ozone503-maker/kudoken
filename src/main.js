// Copy buttons, a self-updating day counter, and lazy loading for the wallet demo and the coin video.
// The only network calls are the wallet's own reads of the Base Sepolia test network, after it loads.
document.querySelectorAll('[data-copy]').forEach(function (btn) {
  var label = btn.textContent;
  btn.addEventListener('click', function () {
    var text = btn.getAttribute('data-copy');
    var done = function () { btn.textContent = 'Copied'; btn.classList.add('done'); setTimeout(function () { btn.textContent = label; btn.classList.remove('done'); }, 1800); };
    var fallback = function () {
      var t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); done(); } catch (e) { btn.textContent = 'Select and copy'; }
      document.body.removeChild(t);
    };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
  });
});
(function () {
  var el = document.getElementById('days'); if (!el) return;
  var d = Math.floor((Date.now() - Date.UTC(2021, 9, 21)) / 864e5);
  if (d > 0) el.textContent = d.toLocaleString('en-US');
})();
(function () {
  var slot = document.getElementById('kdu-wallet');
  var vids = document.querySelectorAll('video.lazyvid');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var loadWallet = function () {
    if (window.__kduWallet) return; window.__kduWallet = 1;
    var s = document.createElement('script'); s.src = 'js/kudoken-wallet.js'; s.defer = true; document.body.appendChild(s);
  };
  var playVid = function (v) {
    if (reduce) return;
    var src = v.querySelector('source[data-src]');
    if (src) { src.src = src.getAttribute('data-src'); src.removeAttribute('data-src'); v.load(); }
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  };
  if (!('IntersectionObserver' in window)) { loadWallet(); vids.forEach(playVid); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) { if (e.target.tagName === 'VIDEO') e.target.pause(); return; }
      if (e.target === slot) { loadWallet(); io.unobserve(slot); } else playVid(e.target);
    });
  }, { rootMargin: '600px 0px' });
  if (slot) io.observe(slot);
  vids.forEach(function (v) { io.observe(v); });
})();

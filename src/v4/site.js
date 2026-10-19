// Kudoken v4: copy buttons, the days counter, the mobile menu and the fireball. No trackers, no cookies.
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
  var m = document.querySelector('.menu'); if (!m) return;
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && m.open) { m.open = false; m.querySelector('summary').focus(); } });
  window.addEventListener('resize', function () { if (window.innerWidth >= 900) m.open = false; });
})();
(function () {
  var fbs = document.querySelectorAll('.fb');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('off', !e.isIntersecting); }); });
    fbs.forEach(function (f) { io.observe(f); });
  }
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('.brand, .fb-hero').forEach(function (el) {
    el.addEventListener('pointerdown', function () {
      var f = el.querySelector('.fb'); if (!f) return;
      f.classList.remove('burst-now'); void f.getBoundingClientRect(); f.classList.add('burst-now');
      setTimeout(function () { f.classList.remove('burst-now'); }, 650);
    });
  });
})();

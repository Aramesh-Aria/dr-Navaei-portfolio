// PROTOTYPE (Stage 2, throwaway). Shared by a.html, b.html, c.html.
// 1. Credential flip: hover (fine pointers), keyboard focus, and tap all turn a card.
// 2. A floating variant switcher (not part of any design): ← → or the arrows cycle A/B/C.
(function () {
  // ---- flip cards -------------------------------------------------------
  document.querySelectorAll('[data-flip]').forEach(function (card) {
    var lastPointer = '';
    card.addEventListener('pointerdown', function (e) { lastPointer = e.pointerType; });
    card.addEventListener('click', function () {
      // A mouse already turns the card on hover; a click must not leave it stuck.
      if (lastPointer === 'mouse') { lastPointer = ''; return; }
      var on = card.getAttribute('aria-pressed') === 'true';
      card.setAttribute('aria-pressed', on ? 'false' : 'true');
      lastPointer = '';
    });
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') card.setAttribute('aria-pressed', 'false');
    });
  });

  // ---- floating call tab: hidden while the first screen's own call button is in view ----
  var tab = document.querySelector('.calltab');
  var heroCall = document.querySelector('main a[href^="tel:"], .sheet a[href^="tel:"]');
  if (tab && heroCall && 'IntersectionObserver' in window) {
    tab.classList.add('is-hidden');
    new IntersectionObserver(function (es) {
      tab.classList.toggle('is-hidden', es[0].isIntersecting || es[0].boundingClientRect.top > 0);
    }).observe(heroCall);
  }

  // ---- variant switcher (prototype chrome) --------------------------------
  if (new URLSearchParams(location.search).has('clean')) return; // screenshots
  var variants = [
    ['a.html', 'A · چادرشب'],
    ['b.html', 'B · سربرگ'],
    ['c.html', 'C · استاندارد'],
  ];
  var here = location.pathname.split('/').pop() || 'a.html';
  var i = Math.max(0, variants.findIndex(function (v) { return v[0] === here; }));
  function go(d) { location.href = variants[(i + d + variants.length) % variants.length][0]; }
  var bar = document.createElement('div');
  bar.setAttribute('aria-label', 'Prototype variant switcher');
  bar.style.cssText = 'position:fixed;left:50%;transform:translateX(-50%);bottom:84px;z-index:99;display:flex;gap:4px;align-items:center;padding:4px;border-radius:999px;background:#111;color:#fff;font:600 13px/1 system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.35);direction:ltr';
  function btn(t, d) {
    var b = document.createElement('button');
    b.textContent = t;
    b.style.cssText = 'all:unset;cursor:pointer;padding:8px 12px;border-radius:999px';
    b.onclick = function () { go(d); };
    return b;
  }
  var label = document.createElement('span');
  label.textContent = variants[i][1];
  label.style.cssText = 'padding:0 6px;direction:rtl';
  bar.append(btn('←', -1), label, btn('→', 1));
  document.body.appendChild(bar);
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t.isContentEditable || /INPUT|TEXTAREA|SELECT/.test(t.tagName)) return;
    if (e.key === 'ArrowLeft') go(-1);
    if (e.key === 'ArrowRight') go(1);
  });
})();

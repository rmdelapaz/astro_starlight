/* nav.js — prev/next page navigation.
 *
 * Add your pages to PAGES below in the order learners should read them.
 * Pages NOT listed in PAGES still render; they just won't show prev/next.
 *
 * Each entry: { href: 'filename.html', title: 'Lesson Title' }
 */
(function () {
  var PAGES = [
    // { href: 'index.html',   title: 'Home' },
    // { href: 'lesson-01.html', title: 'Lesson 1: Intro to Astro' },
    // { href: 'lesson-02.html', title: 'Lesson 2: Components & Layouts' },
    // ...
  ];

  function currentHref() {
    var parts = window.location.pathname.split('/');
    var leaf = parts[parts.length - 1];
    return leaf || 'index.html';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var container = document.getElementById('page-nav');
    if (!container || PAGES.length === 0) return;

    var here = currentHref();
    var idx = -1;
    for (var i = 0; i < PAGES.length; i++) {
      if (PAGES[i].href === here) { idx = i; break; }
    }
    if (idx === -1) return;

    container.innerHTML = '';

    if (idx > 0) {
      var prev = PAGES[idx - 1];
      var a = document.createElement('a');
      a.href = prev.href;
      a.textContent = '\u2190 ' + prev.title;
      container.appendChild(a);
    } else {
      var sp = document.createElement('span');
      sp.className = 'page-nav__spacer';
      container.appendChild(sp);
    }

    if (idx < PAGES.length - 1) {
      var next = PAGES[idx + 1];
      var b = document.createElement('a');
      b.href = next.href;
      b.textContent = next.title + ' \u2192';
      container.appendChild(b);
    } else {
      var sp2 = document.createElement('span');
      sp2.className = 'page-nav__spacer';
      container.appendChild(sp2);
    }
  });
})();

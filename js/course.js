(function () {
  'use strict';
  var root = document.documentElement;
  var key = 'astro-course-theme';
  var saved;
  try { saved = localStorage.getItem(key); } catch (_) {}
  root.dataset.theme = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  document.addEventListener('DOMContentLoaded', function () {
    var theme = document.getElementById('theme-toggle');
    var menu = document.getElementById('mobile-menu-toggle');
    var links = document.getElementById('nav-links');

    function paintTheme() {
      var dark = root.dataset.theme === 'dark';
      if (theme) {
        theme.textContent = dark ? '☀️' : '🌙';
        theme.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      }
    }
    paintTheme();
    if (theme) theme.addEventListener('click', function () {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(key, root.dataset.theme); } catch (_) {}
      paintTheme();
    });

    if (menu && links) {
      menu.addEventListener('click', function () {
        var open = links.classList.toggle('open');
        menu.setAttribute('aria-expanded', String(open));
        menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      });
      links.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () { links.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); });
      });
    }

    document.querySelectorAll('pre').forEach(function (pre) {
      if (!pre.querySelector('code') || pre.querySelector('.copy-button')) return;
      var button = document.createElement('button');
      button.type = 'button'; button.className = 'copy-button'; button.textContent = 'Copy';
      button.addEventListener('click', function () {
        navigator.clipboard.writeText(pre.querySelector('code').innerText).then(function () {
          button.textContent = 'Copied'; button.classList.add('copied');
          setTimeout(function () { button.textContent = 'Copy'; button.classList.remove('copied'); }, 1600);
        });
      });
      pre.appendChild(button);
    });

    var print = document.getElementById('print-button');
    if (print) print.addEventListener('click', function () { window.print(); });
  });
})();

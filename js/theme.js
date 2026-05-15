/* theme.js — light/dark toggle, persisted in localStorage.
 * Reads system preference if no saved value. Applies before paint
 * by running synchronously from <head>.
 */
(function () {
  var STORAGE_KEY = 'astro-course-theme';
  var saved = null;
  try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
  var prefersDark = window.matchMedia &&
                    window.matchMedia('(prefers-color-scheme: dark)').matches;
  var initial = saved || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', initial);

  function icon(theme) { return theme === 'dark' ? '\u2600\ufe0f' : '\ud83c\udf19'; }
  function label(theme) {
    return 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var current = document.documentElement.getAttribute('data-theme');
    btn.textContent = icon(current);
    btn.setAttribute('aria-label', label(current));

    btn.addEventListener('click', function () {
      var now = document.documentElement.getAttribute('data-theme');
      var next = now === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem(STORAGE_KEY, next); } catch (e) {}
      btn.textContent = icon(next);
      btn.setAttribute('aria-label', label(next));
    });
  });
})();

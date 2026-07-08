// theme-toggle.js — Light/Dark theme toggle for AnaReports books
(function() {
  'use strict';

  var STORAGE_KEY = 'ana-theme';

  function getPreferredTheme() {
    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  function toggle() {
    var current = document.documentElement.getAttribute('data-theme') || 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Initialize on load
  setTheme(getPreferredTheme());

  window.AnaTheme = { toggle: toggle, setTheme: setTheme, getPreferredTheme: getPreferredTheme };
})();

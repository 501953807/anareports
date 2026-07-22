// toc-generator.js — Dynamically generates sidebar from JSON TOC config
(function() {
  'use strict';

  function generateSidebar(tocData) {
    var aside = document.createElement('aside');
    aside.className = 'sidebar';

    var html = '<h3><i class="fas fa-list"></i> 目录</h3>';
    html += '<ul class="toc-list">';

    for (var i = 0; i < tocData.length; i++) {
      var item = tocData[i];
      if (item.type === 'chapter') {
        html += '<li class="toc-chapter">' + item.title + '</li>';
      } else if (item.type === 'divider') {
        html += '<li class="toc-divider"></li>';
      } else if (item.type === 'link') {
        html += '<li><a href="' + item.href + '">' + item.title + '</a></li>';
      }
    }

    html += '</ul>';
    aside.innerHTML = html;
    return aside;
  }

  function initTOCGenerator() {
    var body = document.body;
    var tocPath = body.getAttribute('data-toc');
    if (!tocPath) return; // backward compat: no data-toc = keep hardcoded sidebar

    var xhr = new XMLHttpRequest();
    xhr.open('GET', tocPath, true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var tocData = JSON.parse(xhr.responseText);
          var aside = generateSidebar(tocData);

          // Remove any existing hardcoded sidebar
          var oldSidebar = document.querySelector('.sidebar');
          if (oldSidebar) oldSidebar.remove();

          // Insert before main content
          var main = document.querySelector('.content');
          if (main) {
            main.parentNode.insertBefore(aside, main);
          }

          // Highlight current chapter
          if (window.AnaNav && AnaNav.highlightCurrentChapter) {
            AnaNav.highlightCurrentChapter();
          }
        } catch (e) {
          console.error('TOC Generator: failed to parse JSON:', e);
        }
      }
    };
    xhr.send();
  }

  // Auto-init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTOCGenerator);
  } else {
    initTOCGenerator();
  }

  window.AnaTOC = { generateSidebar: generateSidebar };
})();

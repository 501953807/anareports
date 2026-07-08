// navigation.js - Unified navigation for AnaReports books
(function() {
  'use strict';

  // Toggle sidebar
  function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.toggle('open');
  }

  // Highlight current chapter in TOC
  function highlightCurrentChapter() {
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    var links = document.querySelectorAll('.toc-list a');
    links.forEach(function(link) {
      var href = link.getAttribute('href');
      if (href === currentPage || href === 'index.html' && currentPage === 'index.html') {
        link.classList.add('active');
      }
    });
  }

  // Auto-generate TOC from chapter metadata
  function generateTOC(chapters) {
    var tocList = document.querySelector('.toc-list');
    if (!tocList) return;
    tocList.innerHTML = '';
    chapters.forEach(function(ch) {
      var li = document.createElement('li');
      if (ch.type === 'chapter') {
        li.className = 'toc-chapter';
        li.textContent = ch.title;
      } else {
        var a = document.createElement('a');
        a.href = ch.href;
        a.textContent = ch.title;
        li.appendChild(a);
      }
      tocList.appendChild(li);
    });
  }

  // Setup prev/next navigation
  function setupPrevNext(currentIndex, chapters) {
    var prevBtn = document.getElementById('nav-prev');
    var nextBtn = document.getElementById('nav-next');
    if (prevBtn && currentIndex > 0) {
      prevBtn.href = chapters[currentIndex - 1].href;
    }
    if (nextBtn && currentIndex < chapters.length - 1) {
      nextBtn.href = chapters[currentIndex + 1].href;
    }
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', function() {
    highlightCurrentChapter();

    // Mobile: close sidebar when clicking content
    var content = document.querySelector('.content');
    if (content && window.innerWidth <= 768) {
      content.addEventListener('click', function() {
        var sidebar = document.querySelector('.sidebar');
        if (sidebar && sidebar.classList.contains('open')) {
          sidebar.classList.remove('open');
        }
      });
    }
  });

  // Expose globals
  window.AnaNav = { toggleSidebar, highlightCurrentChapter, generateTOC, setupPrevNext };
})();

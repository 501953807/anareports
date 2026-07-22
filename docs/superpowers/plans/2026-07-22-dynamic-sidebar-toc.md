# Dynamic Sidebar TOC Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace hardcoded duplicate sidebar HTML across all 12 book projects with a dynamic JS generator that reads per-book `toc.json` configs.

**Architecture:** A new `common/js/toc-generator.js` module fetches a JSON TOC config (referenced via `<body data-toc="...">` attribute), generates the exact same sidebar HTML structure that existing hardcoded sidebars produce, and hooks into the existing `AnaNav.highlightCurrentChapter()` function. Fully backward compatible — pages without `data-toc` keep working.

**Tech Stack:** Vanilla JavaScript (ES5, no dependencies), existing CSS classes, JSON config files. Zero build step.

## Global Constraints

- Zero build dependencies — pure static HTML + JS
- Generated HTML must use identical class names (`.toc-list`, `.toc-chapter`, `.toc-divider`)
- Backward compatible — pages without `data-toc` keep working unchanged
- No server required — works with `file://` protocol via relative path fetch
- Mobile responsive — CSS breakpoints unchanged
- ES5 compatible — no arrow functions, no const/let in generated code (existing navigation.js uses var/function)

---

### Task 1: Write `common/js/toc-generator.js`

**Files:**
- Create: `common/js/toc-generator.js`

**Interfaces:**
- Consumes: `<body data-toc="books/<book>/toc.json">` attribute
- Produces: `<aside class="sidebar">` DOM element injected before `<main class="content">`

**Step 1: Write the toc-generator module**

```javascript
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
```

**Step 2: Verify the module loads without errors**
- Open any page with `data-toc` pointing to a valid toc.json
- Check browser console for errors
- Verify sidebar renders identically to hardcoded version

**Step 3: Commit**
```bash
git add common/js/toc-generator.js
git commit -m "feat: add dynamic sidebar TOC generator module"
```

---

### Task 2: NO CHANGE — navigation.js is compatible as-is

**No action needed.** The `toc-generator.js` module internally calls `AnaNav.highlightCurrentChapter()` after generating the sidebar. The existing `highlightCurrentChapter()` queries `.toc-list a` which exists in both hardcoded and dynamically-generated sidebars. No modifications to `navigation.js` required.

---

### Task 3: Convert ALL 12 books TOC to JSON

**Files:**
- Create: `books/<name>/toc.json` for all 12 books

**Interfaces:**
- Consumes: sidebar HTML from each book's index.html
- Produces: flat JSON array matching the TOC JSON format spec

**Step 1: Identify which books need migration**

| Book | Dir | Sidebar? | Action |
|------|-----|----------|--------|
| smart-devices | `smart-devices/` | Yes (aside) | Migrate — has worst bugs |
| china-japan | `china-japan/` | Yes (aside) | Migrate |
| chongqing | `chongqing/` | **NO** (inline grid) | SKIP — no sidebar to fix |
| creators-ai | `creators-ai/` | Yes (aside + custom header) | Migrate (handle custom header) |
| creators | `creators/` | Yes (aside) | Migrate |
| ev-motorcycle | `ev-motorcycle/` | Yes (aside) | Migrate — has worst bugs |
| guangzhou | `guangzhou/` | Yes (aside, uses toc-part) | Migrate |
| last-mile-commerce | `last-mile-commerce/` | Yes (aside) | Migrate |
| money-laundering | `money-laundering/` | Yes (aside) | Migrate |
| pharma | `pharma/` | Yes (aside) | Migrate |
| ai-visual-production | `ai-visual-production/` | Yes (aside) | Migrate |
| traditional-academics | `traditional-academics/` | **NO** (inline grid) | SKIP — no sidebar to fix |

**Result**: 10 books need migration, 2 books (chongqing, traditional-academics) have no sidebar and are skipped.

**Step 2: Extract sidebar from each book's index.html and convert to toc.json**

For each book, read lines containing `<aside class="sidebar">` through `</aside>` from index.html. Parse the HTML:
- `<li class="toc-chapter">...</li>` → `{"type": "chapter", "title": "..."}`
- `<li><a href="...">...</a></li>` → `{"type": "link", "href": "...", "title": "..."}`
- `<li class="toc-divider"></li>` → `{"type": "divider"}`

Special handling:
- `creators-ai`: sidebar has extra `<div class="sidebar-header">` wrapper — strip it, keep only `.toc-list` content
- `guangzhou`: uses `<li class="toc-part">` instead of `<li class="toc-chapter">` — normalize to `"chapter"` type
- `last-mile-commerce`: has TWO cross-book links — include both as separate link items after divider
- `money-laundering`: some lines have multiple `<li>...</li><li>...</li>` compacted — split into separate entries

**Step 3: Write each toc.json file**

Create directory structure:
```
books/
  smart-devices/toc.json
  china-japan/toc.json
  creators-ai/toc.json
  creators/toc.json
  ev-motorcycle/toc.json
  guangzhou/toc.json
  last-mile-commerce/toc.json
  money-laundering/toc.json
  pharma/toc.json
  ai-visual-production/toc.json
```

**Step 4: Validate all JSON files**
```bash
for f in books/*/toc.json; do python3 -c "import json; json.load(open('$f'))" && echo "OK: $f" || echo "FAIL: $f"; done
```

**Step 5: Commit**
```bash
git add books/*/toc.json
git commit -m "docs: add TOC configs for 10 books (chongqing & traditional-academics have no sidebar)"
```

---

### Task 4: Migrate smart-devices to dynamic sidebar (pilot book)

**Files:**
- Modify: All 32 HTML files in `smart-devices/` (index.html + 31 content pages)

**Step 1: Write the migration script**

Create `scripts/migrate-book.js`:
```javascript
// migrate-book.js — Remove hardcoded sidebar from all HTML files in a directory
// Usage: node scripts/migrate-book.js <directory> <toc-relative-path>
var fs = require('fs');
var path = require('path');

var dir = path.resolve(process.argv[2] || '.');
var tocPath = process.argv[3] || '../books/smart-devices/toc.json';

var files = fs.readdirSync(dir).filter(function(f) { return f.endsWith('.html'); });

files.forEach(function(file) {
  var filePath = path.join(dir, file);
  var html = fs.readFileSync(filePath, 'utf8');
  
  // Remove hardcoded sidebar block
  var newHtml = html.replace(/<aside class="sidebar">[\s\S]*?<\/aside>/g, '');
  
  if (newHtml === html) {
    console.log('SKIP (no sidebar): ' + file);
    return;
  }
  
  // Add data-toc attribute to <body> tag
  newHtml = newHtml.replace(/<body>/, '<body data-toc="' + tocPath + '">');
  
  fs.writeFileSync(filePath, newHtml, 'utf8');
  console.log('MIGRATED: ' + file);
});

console.log('Done. Migrated ' + files.filter(function(f) {
  var h = fs.readFileSync(path.join(dir, f), 'utf8');
  return h.indexOf('<aside class="sidebar">') !== -1;
}).length + ' of ' + files.length + ' files.');
```

**Step 2: Run the migration script on smart-devives/**

```bash
node scripts/migrate-book.js smart-devices/ "../books/smart-devices/toc.json"
```

Expected output: "MIGRATED: *.html" for each of the 32 files.

**Step 3: Test in browser**
- Open `smart-devices/index.html` in Chrome
- Verify sidebar renders correctly with all 31 chapters
- Click each link to verify navigation works
- Verify active chapter highlighting
- Resize browser to test mobile toggle
- Test a sub-chapter page like `smart-devices/11-heart-monitor-depth.html`

**Step 4: If OK, commit**
```bash
git add smart-devices/*.html common/js/toc-generator.js scripts/migrate-book.js
git commit -m "feat: migrate smart-devices to dynamic sidebar TOC (pilot book)"
```

**Step 5: If NOT OK, debug and fix**
- Common issues: regex doesn't match sidebar block, data-toc path wrong, sidebar not rendering
- Fix the issue, retest, then commit

---

### Task 5: Migrate remaining 9 books with sidebar

**Files:**
- Modify: All content page HTMLs in 9 remaining books (~310 files total)

**Books to migrate** (from survey, excluding chongqing & traditional-academics which have no sidebar):
1. china-japan (31 pages) — cross-book link: `../pharma/index.html`
2. creators-ai (32 pages) — custom sidebar header, needs special handling
3. creators (32 pages)
4. ev-motorcycle (30 pages) — cross-book link: `../money-laundering/index.html`
5. guangzhou (36 pages) — uses `toc-part` class instead of `toc-chapter`, cross-book link: `../creators/index.html`
6. last-mile-commerce (63 pages) — TWO cross-book links
7. money-laundering (31 pages)
8. pharma (31 pages) — cross-book link: `../money-laundering/index.html`
9. ai-visual-production (26 pages)

**Step 1: For each book, run the migration script**

```bash
node scripts/migrate-book.js china-japan/ "../books/china-japan/toc.json"
node scripts/migrate-book.js creators-ai/ "../books/creators-ai/toc.json"
node scripts/migrate-book.js creators/ "../books/creators/toc.json"
node scripts/migrate-book.js ev-motorcycle/ "../books/ev-motorcycle/toc.json"
node scripts/migrate-book.js guangzhou/ "../books/guangzhou/toc.json"
node scripts/migrate-book.js last-mile-commerce/ "../books/last-mile-commerce/toc.json"
node scripts/migrate-book.js money-laundering/ "../books/money-laundering/toc.json"
node scripts/migrate-book.js pharma/ "../books/pharma/toc.json"
node scripts/migrate-book.js ai-visual-production/ "../books/ai-visual-production/toc.json"
```

**Step 2: Spot-check each book in browser**
- Pick 2-3 random pages per book
- Verify sidebar renders correctly
- Verify navigation works
- Verify active highlighting

**Step 3: Final commit**
```bash
git add -A
git commit -m "feat: migrate remaining 9 books to dynamic sidebar TOC"
```

---

### Task 6: Cleanup and verification

**Files:**
- Delete: `scripts/migrate-book.js` (temporary)

**Step 1: Delete temporary migration script**
```bash
rm scripts/migrate-book.js
rmdir scripts 2>/dev/null || true
```

**Step 2: Final audit**
- Verify all toc.json files exist: `ls books/*/toc.json` should show 10 files
- Verify no hardcoded sidebars remain in content pages: grep for `aside class="sidebar"` — should only appear in index.html files (which we migrated too) or not at all

**Step 3: Final commit**
```bash
git add -A
git commit -m "chore: cleanup dynamic sidebar TOC implementation"
```

---

Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

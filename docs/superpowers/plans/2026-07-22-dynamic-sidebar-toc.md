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

### Task 2: Update `common/js/navigation.js` to call initTOCGenerator

**Files:**
- Modify: `common/js/navigation.js`

**Step 1: Add init call**

Read the existing `navigation.js` DOMContentLoaded handler (line 56-69). Add a call to `initTOCGenerator()` inside it:

```javascript
document.addEventListener('DOMContentLoaded', function() {
  highlightCurrentChapter();
  // Initialize dynamic TOC if data-toc is set
  if (window.AnaTOC && AnaTOC.init) {
    AnaTOC.init();
  }
  // ... existing mobile sidebar close logic ...
});
```

Wait — actually, `toc-generator.js` already calls `initTOCGenerator()` on its own DOMContentLoaded. The only addition needed is to ensure `highlightCurrentChapter()` runs AFTER the dynamic sidebar is generated. So we need to move the highlight call in navigation.js to run after TOC generation, OR have toc-generator.js call it internally (which it already does on line ~42 of the code above).

**Revised approach**: No change needed to navigation.js. The toc-generator.js already calls `AnaNav.highlightCurrentChapter()` after generating the sidebar. The existing `highlightCurrentChapter()` in navigation.js handles both hardcoded and dynamically-generated sidebars because it queries `.toc-list a` which exists in both cases.

**Step 2: Verify no regression**
- Confirm pages WITHOUT `data-toc` still work (hardcoded sidebar + highlighting)
- Confirm pages WITH `data-toc` get dynamic sidebar + highlighting

**Step 3: Commit**
```bash
git add common/js/navigation.js
git commit -m "chore: verify navigation.js compatibility with dynamic TOC (no changes needed)"
```

Actually, skip this commit — no changes are needed to navigation.js. Move to next task.

---

### Task 3: Convert smart-devices TOC to JSON

**Files:**
- Create: `books/smart-devices/toc.json`

**Interfaces:**
- Consumes: sidebar HTML from `smart-devices/index.html`
- Produces: flat JSON array matching the TOC JSON format spec

**Step 1: Extract sidebar from smart-devices/index.html**

The correct sidebar structure is in `smart-devices/index.html` lines 16-60. It contains:
- 10 `toc-chapter` headers (第一章 through 第三十一章, but chapters 11-31 have NO chapter headers — they're bare links)
- 31 chapter links (01-market-overview through 31-medical-wristband-regulatory)
- 1 divider + 1 cross-book link ("返回中日经济书")

Convert to JSON:
```json
[
  {"type": "chapter", "title": "第一章：市场环境"},
  {"type": "link", "href": "01-market-overview.html", "title": "第一章：全球与中国智能穿戴市场"},
  {"type": "chapter", "title": "第二章：用户画像"},
  {"type": "link", "href": "02-user-profile.html", "title": "第二章：用户画像与应用场景"},
  ...
  {"type": "link", "href": "11-heart-monitor-depth.html", "title": "第十一章：心率/ECG监测深度技术"},
  {"type": "link", "href": "12-sleep-tracking-depth.html", "title": "第十二章：睡眠追踪深度技术"},
  {"type": "link", "href": "13-gps-tracker-depth.html", "title": "第十三章：GPS定位深度技术"},
  ...
  {"type": "link", "href": "31-medical-wristband-regulatory.html", "title": "第三十一章：医用电子腕带监管闭环"},
  {"type": "divider"},
  {"type": "link", "href": "../china-japan/index.html", "title": "返回中日经济书"}
]
```

**Step 2: Write the file**

Use Read tool on `smart-devices/index.html` lines 16-60 to extract exact sidebar HTML, then convert to JSON format.

**Step 3: Validate JSON**
```bash
python3 -c "import json; json.load(open('books/smart-devices/toc.json'))" && echo "Valid JSON"
```

**Step 4: Commit**
```bash
git add books/smart-devices/toc.json
git commit -m "docs: add TOC config for smart-devices book"
```

---

### Task 4: Migrate smart-devives to dynamic sidebar (pilot book)

**Files:**
- Modify: `smart-devices/index.html` (add data-toc, remove hardcoded sidebar)
- Modify: All 31 content pages in `smart-devices/` (remove hardcoded sidebar, add data-toc)

**Step 1: Write a conversion script**

Create a temporary Node.js script `scripts/migrate-sidebar.js` that:
1. Takes a directory path as argument
2. Reads each `.html` file
3. Finds the `<aside class="sidebar">...</aside>` block
4. Removes it
5. Adds `data-toc="../books/smart-devices/toc.json"` to the `<body>` tag
6. Writes the modified HTML back

The script should use regex or a simple HTML parser to find and remove the sidebar block. Since these are well-formed HTML files, a regex like `<aside class="sidebar">.*?</aside>` with `s` flag will work.

**Step 2: Run the script on smart-devices/**

```bash
node scripts/migrate-sidebar.js smart-devices/
```

**Step 3: Test in browser**
- Open `smart-devices/index.html` in Chrome
- Verify sidebar renders correctly with all 31 chapters
- Click each link to verify navigation works
- Verify active chapter highlighting
- Resize browser to test mobile toggle

**Step 4: If OK, commit**
```bash
git add smart-devices/*.html
git add common/js/toc-generator.js
git commit -m "feat: migrate smart-devices to dynamic sidebar TOC (pilot book)"
```

**Step 5: If NOT OK, debug and fix**
- Common issues: regex doesn't match sidebar block, data-toc path wrong, sidebar not rendering
- Fix the issue, retest, then commit

---

### Task 5: Survey remaining 11 books' sidebar structures

**Files:**
- Read: Each book's `index.html` sidebar section
- Create: `books/<name>/toc.json` for each of the 11 remaining books

**Interfaces:**
- Consumes: sidebar HTML from each book's index.html
- Produces: toc.json for each book

**Step 1: For each remaining book, extract sidebar from index.html and convert to toc.json**

Books to process:
1. china-japan (31 pages) — has correct sidebar in index.html
2. chongqing (40 pages) — may use different layout, verify
3. creators-ai (32 pages)
4. creators (32 pages)
5. ev-motorcycle (30 pages)
6. guangzhou (36 pages) — may use different layout, verify
7. last-mile-commerce (63 pages)
8. money-laundering (31 pages)
9. pharma (31 pages)
10. traditional-academics (32 pages) — may use different layout, verify
11. ai-visual-production (26 pages)

**Step 2: Write each toc.json**
- Use the same flat array format
- Ensure cross-book links use correct relative paths
- Validate each JSON file

**Step 3: Commit all toc.json files**
```bash
git add books/*/toc.json
git commit -m "docs: add TOC configs for remaining 11 books"
```

---

### Task 6: Migrate all remaining books

**Files:**
- Modify: All content page HTMLs in 11 remaining books (~340 files total)

**Step 1: Run the migration script on each book directory**

```bash
for dir in china-japan chongqing creators-ai creators ev-motorcycle guangzhou last-mile-commerce money-laundering pharma traditional-academics ai-visual-production; do
  node scripts/migrate-sidebar.js "$dir/"
done
```

**Step 2: Spot-check each book in browser**
- Pick 2-3 random pages per book
- Verify sidebar renders correctly
- Verify navigation works
- Verify active highlighting

**Step 3: Final commit**
```bash
git add -A
git commit -m "feat: migrate all 12 books to dynamic sidebar TOC"
```

---

### Task 7: Cleanup and verification

**Files:**
- Delete: `scripts/migrate-sidebar.js` (temporary)
- Verify: All 12 books render correctly

**Step 1: Delete temporary migration script**
```bash
rm scripts/migrate-sidebar.js
```

**Step 2: Final audit**
- grep for remaining hardcoded sidebars: `grep -rl 'aside class="sidebar"' */*.html | wc -l`
- Should be 0 (or only index.html files if we migrated those too)
- Verify all toc.json files exist: `ls books/*/toc.json | wc -l` should be 12

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

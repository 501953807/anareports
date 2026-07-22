# Dynamic Sidebar TOC Generator Design

> Date: 2026-07-22
> Status: Approved

## Goal

Eliminate hardcoded duplicate sidebar HTML across all 12 book projects by generating the sidebar dynamically from a single JSON config per book.

## Architecture

### New Files

1. **`common/js/toc-generator.js`** — Core module (~80 lines)
   - Reads `data-toc` attribute from `<body>` tag
   - Fetches the JSON TOC config
   - Generates `<aside class="sidebar">` HTML with exact same structure as existing hardcoded sidebars
   - Uses existing CSS classes: `.toc-list`, `.toc-chapter`, `.toc-divider`
   - Calls `AnaNav.highlightCurrentChapter()` after rendering
   - Backward compatible: if no `data-toc`, does nothing (existing hardcoded sidebar stays)

2. **`books/<book-name>/toc.json`** — One per book (12 files total)
   - Flat array of items
   - Item types:
     - `{"type": "chapter", "title": "第一部分：xxx"}` → renders as `<li class="toc-chapter">title</li>`
     - `{"type": "link", "href": "...", "title": "..."}` → renders as `<li><a href="...">title</a></li>`
     - `{"type": "divider"}` → renders as `<li class="toc-divider"></li>`
   - Cross-book links use relative paths (e.g., `"../pharma/index.html"`)

### Existing Files Modified

3. **`common/js/navigation.js`** — Minor update
   - Add `initTOCGenerator()` call at end of DOMContentLoaded
   - No other changes needed

4. **All content page HTMLs** (~350 files)
   - Remove hardcoded `<aside class="sidebar">...</aside>` block
   - Add `data-toc="../books/<book-name>/toc.json"` to `<body>` tag
   - Keep everything else unchanged (top-nav, main content, footer, echarts, etc.)

5. **Book index.html files** (~12 files)
   - Option A: Also migrate to use `data-toc` (cleanest)
   - Option B: Keep existing hardcoded sidebar (it's already correct)
   - Recommendation: Option A for consistency

### Data Flow

```
<body data-toc="books/china-japan/toc.json">
  ↓
toc-generator.js fetches toc.json
  ↓
Generates: <aside class="sidebar"><ul class="toc-list">...</ul></aside>
  ↓
AnaNav.highlightCurrentChapter() marks active link
```

### TOC JSON Format Example

```json
[
  {"type": "chapter", "title": "第一部分：中国现状诊断"},
  {"type": "link", "href": "01-china-diagnosis.html", "title": "第一章：中国经济现状深度诊断"},
  {"type": "link", "href": "09-demographics-depth.html", "title": "1.1 人口结构深度"},
  {"type": "chapter", "title": "第二部分：日本失去的三十年"},
  {"type": "link", "href": "02-japan-lost-decades.html", "title": "第二章：日本泡沫破裂到失去的三十年"},
  ...
  {"type": "divider"},
  {"type": "link", "href": "../pharma/index.html", "title": "返回医药产业书"}
]
```

## Migration Strategy

**Per-book migration** (lowest risk):

1. Pick one book (start with smart-devices — most bugs confirmed)
2. Extract sidebar from that book's `index.html` → convert to `toc.json`
3. Write `toc-generator.js`
4. Update `navigation.js` to call it
5. Replace sidebar in ALL content pages of that book
6. Test in browser
7. If OK, repeat for next book

**Conversion script**: A small Node/Python script can auto-convert hardcoded sidebar HTML → `toc.json` format. This avoids manual transcription for 350+ pages.

## Constraints

- Zero build dependencies — pure static HTML + JS
- CSS unchanged — generated HTML uses identical class names
- Backward compatible — pages without `data-toc` keep working
- No server required — works with `file://` protocol (JSON fetched via relative path)
- Mobile responsive — CSS breakpoints unchanged

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| JSON fetch fails on `file://` protocol | Use synchronous fallback or note that a local server is needed for testing |
| Large JSON files for big books (last-mile-commerce has 63 pages) | Still tiny — ~5KB max. No performance concern. |
| Breaking existing navigation | Backward compat: only pages with `data-toc` are affected |
| Cross-book links break | toc.json stores relative paths; verify during per-book migration |

## Success Criteria

- [ ] All 12 books have `toc.json` files
- [ ] All ~350 content pages render sidebar identically to before
- [ ] Clicking any sidebar link navigates correctly (no chapter jumping)
- [ ] Active chapter highlighting works
- [ ] Mobile toggle sidebar works
- [ ] Zero hardcoded sidebars remain in content pages

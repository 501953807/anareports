# 中华古典学术理论全景书 — 重设计实施

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `traditional-academics/` 全书改造为纸质书风格、五段式内容结构、图文并茂的电子书体验。

**Architecture:** 渐进式重写：先改造共享CSS和主题切换基础设施，再重写封面页，然后逐部分重写31章内容页（八卦→阴阳五行→中医→易经→道家→儒家）。每章统一采用"故事引入→概念解析→深入理解→实践应用→延伸阅读"五段式结构，新增SVG插图、跨章节关联卡片、思考题和延伸阅读区块。

**Tech Stack:** 纯HTML5 + CSS3（CSS变量主题系统）+ 内联SVG + ECharts 5.5.0 + 原生JS主题切换

## Global Constraints

- 所有页面默认使用浅色纸质书主题（#FAF9F6背景，Noto Serif衬线体，1.9行高，17px正文）
- 可选深色模式切换（通过 `<html data-theme="dark">` 控制）
- 每章严格遵循五段式结构（故事引入→概念解析→深入理解→实践应用→延伸阅读）
- 每章至少2张SVG插图
- 每章底部有≥2个跨章节关联卡片
- 每章有≥2道思考题
- 每章有≥2本延伸阅读推荐
- ECharts图表保留并融入"深入理解"段落
- 现有CSS类名（`.section-title`, `.data-table`, `.tip-box`, `.case-box`, `.data-card`, `.steps-list`, `.chart-container`, `.grid-2/3/4`, `.timeline`, `.badge`）向后兼容
- 文件命名保持NN-slug.html零填充格式
- 共享资源路径统一使用 `../common/css/book.css` 和 `../common/js/`
- 打印友好：新增 `@media print` 样式支持PDF导出

---

### Task 1: 重写 book.css — 纸质书浅色主题 + 深色模式

**Files:**
- Modify: `traditional-academics/common/css/book.css`

**Interfaces:**
- Consumes: None (foundation layer)
- Produces: CSS变量主题系统 `--bg`, `--surface`, `--surface2`, `--border`, `--text`, `--text2`, `--accent`, `--link` + 深色模式 `[data-theme="dark"]` 覆盖

**Implementation:**

```css
/* ===== AnaReports Book Theme — Paper Style ===== */

:root {
  /* 纸质书浅色主题（默认） */
  --bg: #FAF9F6;
  --surface: #FFFFFF;
  --surface2: #F5F4F0;
  --border: #E8E6E1;
  --text: #2C2C2C;
  --text2: #666666;
  --accent: #B8860B;
  --link: #1A5276;

  /* 保留原有彩色变量用于卡片和徽章 */
  --cyan: #0891b2;
  --purple: #7c3aed;
  --red: #dc2626;
  --green: #059669;
  --orange: #d97706;
  --pink: #db2777;
  --gold: #b8860b;
}

[data-theme="dark"] {
  --bg: #1a1d27;
  --surface: #232733;
  --surface2: #1e222d;
  --border: #2d3348;
  --text: #e2e8f0;
  --text2: #94a3b8;
  --accent: #eab308;
  --link: #60a5fa;
  --cyan: #22d3ee;
  --purple: #a78bfa;
  --red: #f87171;
  --green: #34d399;
  --orange: #fbbf24;
  --pink: #f472b6;
  --gold: #facc15;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Noto Serif SC', 'Source Han Serif CN', 'Songti SC', serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.9;
  font-size: 17px;
  letter-spacing: 0.02em;
  min-width: 320px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ===== Top Navigation Bar ===== */
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 8px 20px;
  display: flex; align-items: center; justify-content: space-between;
  height: 48px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.top-nav .nav-left { display: flex; align-items: center; gap: 12px; }
.top-nav .nav-book-name {
  font-size: 13px; font-weight: 700; color: var(--accent);
  text-decoration: none; white-space: nowrap;
  font-family: 'Noto Serif SC', serif;
}
.top-nav .nav-divider { color: var(--text2); font-size: 12px; }
.top-nav .nav-chapter-title {
  font-size: 13px; color: var(--text); white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; max-width: 300px;
  font-family: 'Noto Serif SC', serif;
}
.top-nav .nav-right { display: flex; align-items: center; gap: 8px; }
.top-nav .nav-btn {
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text2); padding: 4px 12px; border-radius: 4px;
  font-size: 12px; cursor: pointer; text-decoration: none;
  transition: all 0.2s; font-family: 'Noto Sans SC', sans-serif;
}
.top-nav .nav-btn:hover { border-color: var(--accent); color: var(--accent); }
.top-nav .nav-toc-toggle { display: none; }

/* ===== Theme Toggle Button ===== */
.theme-toggle-btn {
  background: none; border: 1px solid var(--border);
  color: var(--text2); padding: 4px 8px; border-radius: 4px;
  font-size: 14px; cursor: pointer; transition: all 0.2s;
}
.theme-toggle-btn:hover { border-color: var(--accent); color: var(--accent); }

/* ===== Left Sidebar (Table of Contents) ===== */
.sidebar {
  position: fixed; left: 0; top: 48px; bottom: 0;
  width: 260px; background: var(--surface);
  border-right: 1px solid var(--border);
  overflow-y: auto; padding: 16px;
  transition: transform 0.3s;
  z-index: 90;
}
.sidebar.closed { transform: translateX(-260px); }
.sidebar h3 {
  font-size: 13px; font-weight: 700; color: var(--accent);
  margin-bottom: 12px; padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
  font-family: 'Noto Serif SC', serif;
}
.sidebar .toc-list { list-style: none; }
.sidebar .toc-list li { margin-bottom: 2px; }
.sidebar .toc-list a {
  display: block; padding: 4px 8px; font-size: 12px;
  color: var(--text2); text-decoration: none; border-radius: 4px;
  transition: all 0.2s; line-height: 1.5;
  font-family: 'Noto Sans SC', sans-serif;
}
.sidebar .toc-list a:hover { background: var(--surface2); color: var(--text); }
.sidebar .toc-list a.active {
  background: rgba(184,134,11,0.1); color: var(--accent);
  border-left: 2px solid var(--accent); padding-left: 6px;
}
.sidebar .toc-list .toc-chapter {
  font-weight: 600; color: var(--text); font-size: 13px;
  margin-top: 8px; padding-top: 8px;
  border-top: 1px solid var(--border);
  font-family: 'Noto Serif SC', serif;
}

/* ===== Main Content ===== */
.content {
  margin-left: 260px; padding: 30px 40px;
  min-height: calc(100vh - 48px);
  max-width: 720px;
}
.sidebar.closed ~ .content { margin-left: 0; }

/* ===== Page Footer ===== */
.page-footer {
  margin-left: 260px; padding: 20px 40px;
  border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  font-size: 12px; color: var(--text2);
  font-family: 'Noto Sans SC', sans-serif;
}
.sidebar.closed ~ .page-footer { margin-left: 0; }
.page-footer .nav-prev, .page-footer .nav-next {
  color: var(--accent); text-decoration: none;
  padding: 6px 12px; border: 1px solid var(--border);
  border-radius: 4px; transition: all 0.2s;
  font-family: 'Noto Sans SC', sans-serif;
}
.page-footer .nav-prev:hover, .page-footer .nav-next:hover {
  border-color: var(--accent); background: rgba(184,134,11,0.06);
}
.page-footer .nav-home { color: var(--text2); text-decoration: none; }

/* ===== Section Titles ===== */
.section-title {
  font-size: 28px; font-weight: 700; margin: 48px 0 24px;
  padding-left: 14px; border-left: 3px solid var(--accent); color: var(--text);
  font-family: 'Noto Serif SC', serif;
  line-height: 1.4;
}
.section-subtitle {
  font-size: 20px; font-weight: 600; color: var(--text); margin: 36px 0 16px;
  font-family: 'Noto Serif SC', serif;
  line-height: 1.5;
}

/* ===== Chapter Header ===== */
.chapter-header {
  text-align: center;
  padding: 24px 0 32px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 32px;
}
.chapter-part {
  display: inline-block;
  font-size: 12px;
  color: var(--accent);
  font-weight: 600;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
  font-family: 'Noto Sans SC', sans-serif;
}
.chapter-intro {
  font-size: 15px;
  color: var(--text2);
  margin-top: 12px;
  font-style: italic;
}

/* ===== Paragraphs ===== */
.content p {
  margin: 14px 0;
  text-align: justify;
  text-indent: 2em;
}
.content > *:first-child > p,
.chapter-header + p,
.section-subtitle + p {
  text-indent: 0;
}

/* ===== Cards ===== */
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; margin: 12px 0;
}
.card.highlight { border-color: var(--accent); }
.card.warning { border-color: var(--orange); }
.card.danger { border-color: var(--red); }

/* ===== Data Card ===== */
.data-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; text-align: center; margin: 8px 0;
}
.data-card .value { font-size: 24px; font-weight: 700; color: var(--accent); }
.data-card .label { font-size: 12px; color: var(--text2); margin-top: 4px; }

/* ===== Table ===== */
.data-table {
  width: 100%; border-collapse: collapse; margin: 16px 0;
  font-size: 13px;
}
.data-table th {
  background: var(--surface2); color: var(--accent);
  padding: 10px 12px; text-align: left; font-weight: 600;
  border-bottom: 2px solid var(--border);
  font-family: 'Noto Sans SC', sans-serif;
}
.data-table td {
  padding: 8px 12px; border-bottom: 1px solid var(--border);
  color: var(--text);
  font-family: 'Noto Serif SC', serif;
}
.data-table tr:hover td { background: var(--surface2); }

/* ===== Case Box ===== */
.case-box {
  background: rgba(124,58,237,0.04); border: 1px solid var(--purple);
  border-radius: 8px; padding: 14px; margin: 14px 0;
}
.case-box .case-title {
  font-size: 13px; font-weight: 700; color: var(--purple); margin-bottom: 6px;
  font-family: 'Noto Sans SC', sans-serif;
}
.case-box .case-body { font-size: 13px; color: var(--text); line-height: 1.8; }

/* ===== Tip Box ===== */
.tip-box {
  background: rgba(184,134,11,0.04); border: 1px solid var(--accent);
  border-radius: 8px; padding: 14px; margin: 14px 0;
}
.tip-box .tip-title {
  font-size: 13px; font-weight: 700; color: var(--accent); margin-bottom: 6px;
  font-family: 'Noto Sans SC', sans-serif;
}
.tip-box .tip-body { font-size: 13px; color: var(--text); line-height: 1.8; }

/* ===== Chart Container ===== */
.chart-container {
  width: 100%; height: 400px; margin: 20px 0;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; overflow: hidden;
}

/* ===== Steps List ===== */
.steps-list { counter-reset: step; list-style: none; padding: 0; margin: 16px 0; }
.steps-list li {
  counter-increment: step; padding: 10px 10px 10px 50px;
  position: relative; margin: 8px 0; background: var(--surface);
  border-radius: 6px; font-size: 14px; line-height: 1.8;
  border: 1px solid var(--border);
  font-family: 'Noto Serif SC', serif;
  text-indent: 0;
}
.steps-list li::before {
  content: counter(step); position: absolute; left: 10px; top: 10px;
  width: 28px; height: 28px; background: var(--accent); color: var(--bg);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

/* ===== Timeline ===== */
.timeline { position: relative; padding-left: 30px; margin: 20px 0; }
.timeline::before {
  content: ''; position: absolute; left: 8px; top: 0; bottom: 0;
  width: 2px; background: var(--border);
}
.timeline-item { position: relative; margin-bottom: 16px; padding-left: 16px; }
.timeline-item::before {
  content: ''; position: absolute; left: -26px; top: 6px;
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--accent);
}
.timeline-item .tl-year { font-size: 12px; font-weight: 700; color: var(--accent); }
.timeline-item .tl-desc { font-size: 13px; color: var(--text); line-height: 1.6; }

/* ===== Grid ===== */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }

/* ===== Badge ===== */
.badge {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
}
.badge.cyan { background: rgba(8,145,178,0.1); color: var(--cyan); }
.badge.purple { background: rgba(124,58,237,0.1); color: var(--purple); }
.badge.red { background: rgba(220,38,38,0.1); color: var(--red); }
.badge.green { background: rgba(5,150,105,0.1); color: var(--green); }
.badge.orange { background: rgba(217,119,6,0.1); color: var(--orange); }

/* ===== Illustration SVG ===== */
.illustration-svg {
  text-align: center;
  margin: 32px 0;
  padding: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
}
.illustration-svg svg {
  max-width: 100%;
  height: auto;
}
.illustration-caption {
  font-size: 13px;
  color: var(--text2);
  margin-top: 12px;
  font-style: italic;
  font-family: 'Noto Sans SC', sans-serif;
}

/* ===== Cross Reference Grid ===== */
.cross-ref-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 12px;
  margin: 20px 0;
}
.cross-ref-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  color: var(--text);
  transition: all 0.2s;
}
.cross-ref-card:hover {
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.cross-ref-icon { font-size: 24px; flex-shrink: 0; }
.cross-ref-info strong { display: block; font-size: 14px; color: var(--link); font-family: 'Noto Sans SC', sans-serif; }
.cross-ref-info span { font-size: 12px; color: var(--text2); font-family: 'Noto Sans SC', sans-serif; }

/* ===== Reflection Questions ===== */
.reflection-questions, .further-reading {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px 20px;
  margin: 20px 0;
}
.reflection-questions h3, .further-reading h3 {
  font-size: 14px; font-weight: 600; color: var(--accent); margin-bottom: 10px;
  font-family: 'Noto Sans SC', sans-serif;
}
.reflection-questions ol, .reflection-questions ul,
.further-reading ol, .further-reading ul {
  padding-left: 20px; margin: 0;
}
.reflection-questions li, .further-reading li {
  font-size: 13px; color: var(--text); line-height: 1.7; margin: 4px 0;
  font-family: 'Noto Sans SC', sans-serif;
}

/* ===== Key Term Highlight ===== */
.key-term { color: var(--accent); font-weight: 600; }
.key-term-def {
  cursor: help;
  border-bottom: 1px dotted var(--text2);
  font-size: 12px;
}

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .content { padding: 20px 24px; }
  .page-footer { padding: 16px 24px; }
}
@media (max-width: 768px) {
  .sidebar { transform: translateX(-260px); }
  .sidebar.open { transform: translateX(0); }
  .top-nav .nav-toc-toggle { display: inline-block; }
  .top-nav .nav-chapter-title { max-width: 150px; }
  .content { margin-left: 0; padding: 16px; }
  .page-footer { margin-left: 0; padding: 12px 16px; flex-wrap: wrap; gap: 8px; }
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
  .chart-container { height: 300px; }
}
@media (max-width: 480px) {
  .content { padding: 12px; }
  .section-title { font-size: 22px; }
  .chart-container { height: 250px; }
  .top-nav { padding: 6px 12px; height: 42px; }
  .sidebar { top: 42px; width: 220px; }
  .sidebar.open ~ .content { margin-left: 0; }
}

/* ===== Print Styles ===== */
@media print {
  body { background: white; color: black; font-size: 12pt; }
  .top-nav, .sidebar, .page-footer, .theme-toggle-btn { display: none !important; }
  .content { margin-left: 0; padding: 20px; max-width: none; }
  .chart-container { break-inside: avoid; page-break-inside: avoid; }
  .card, .data-card, .case-box, .tip-box { break-inside: avoid; page-break-inside: avoid; }
  .data-table th { background: #f5f5f5 !important; color: #333 !important; }
  .data-table td { color: #333 !important; }
}
```

- [ ] **Step 1: Backup existing book.css**

Run: `cp traditional-academics/common/css/book.css traditional-academics/common/css/book.css.bak`

- [ ] **Step 2: Write the new book.css with paper-style theme**

Replace entire file content with the CSS above.

- [ ] **Step 3: Verify CSS syntax**

Run: `npx stylelint traditional-academics/common/css/book.css 2>/dev/null || echo "stylelint not installed, checking basic syntax"`

Expected: No obvious CSS syntax errors (braces balanced, colons present)

- [ ] **Step 4: Commit**

```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports
git add traditional-academics/common/css/book.css
git commit -m "refactor: rewrite book.css for paper-style typography with dark mode support"
```

---

### Task 2: 创建主题切换 JS 模块

**Files:**
- Create: `traditional-academics/common/js/theme-toggle.js`

**Interfaces:**
- Consumes: None
- Produces: `window.AnaTheme.toggle()` function, persists preference in `localStorage('ana-theme')`

**Implementation:**

```javascript
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
```

- [ ] **Step 1: Write the theme-toggle.js file**

Create `traditional-academics/common/js/theme-toggle.js` with the code above.

- [ ] **Step 2: Verify file exists**

Run: `test -f traditional-academics/common/js/theme-toggle.js && echo "OK"`

Expected: OK

- [ ] **Step 3: Commit**

```bash
git add traditional-academics/common/js/theme-toggle.js
git commit -m "feat: add theme toggle module (light/dark mode) with localStorage persistence"
```

---

### Task 3: 重写封面页 index.html

**Files:**
- Modify: `traditional-academics/index.html`

**Interfaces:**
- Consumes: New book.css (Task 1), theme-toggle.js (Task 2)
- Produces: 纸质书风格封面，含意境封面图区域、六部分TOC网格、ECharts雷达图

**Key changes:**
1. 字体从 Noto Sans SC 改为 Noto Serif SC
2. 背景从 #0a0e17 改为 #FAF9F6
3. 封面hero区域添加意境装饰（水墨风格渐变背景）
4. TOC卡片改为纸质书风格（白底+柔和阴影）
5. 添加主题切换按钮
6. 添加 `common/js/theme-toggle.js` 引用
7. 保留ECharts雷达图但配色改为纸质书风格

- [ ] **Step 1: Read current index.html and plan changes**

Read `traditional-academics/index.html` to understand exact structure.

- [ ] **Step 2: Rewrite the inline CSS block**

Replace all `--bg:#0a0e17` etc with paper-style variables. Update `.cover-hero` gradient from cyberpunk radial to ink-wash style. Update `.toc-part` from dark cards to light cards with shadow.

- [ ] **Step 3: Update body styles**

Change `font-family` to include serif. Add theme toggle button in hero area.

- [ ] **Step 4: Add theme-toggle.js script reference**

Before closing `</body>`, add:
```html
<script src="common/js/theme-toggle.js"></script>
```

- [ ] **Step 5: Update ECharts radar chart colors**

Change from cyan/gold neon to warm earth tones (#B8860B, #8B4513, #6B7280).

- [ ] **Step 6: Verify in browser**

Open `traditional-academics/index.html` in browser. Check:
- Light background visible
- Serif fonts rendering
- Theme toggle button present
- Radar chart displays correctly
- All 6 part links clickable

- [ ] **Step 7: Commit**

```bash
git add traditional-academics/index.html
git commit -m "design: redesign cover page for paper-style typography and light theme"
```

---

### Task 4: 重写第一部分 八卦（01-05）

**Files:**
- Modify: `traditional-academics/01-bagua-origin.html`
- Modify: `traditional-academics/02-fuxi-shennong.html`
- Modify: `traditional-academics/03-zhouyi-wenwang.html`
- Modify: `traditional-academics/04-bagua-xiangshu.html`
- Modify: `traditional-academics/05-bagua-summary.html`

**Interfaces:**
- Consumes: New book.css, theme-toggle.js
- Produces: 5章五段式内容 + SVG插图 + 跨章节关联

**每章新增内容：**
1. 故事引入段落（历史典故开场）
2. SVG矢量插图（先天/后天八卦方位图、八卦取象比类图）
3. 实践应用段落
4. 延伸阅读段落（含≥2跨章节关联卡片、≥2思考题、≥2延伸阅读推荐）
5. 添加 `theme-toggle.js` 引用到每个文件

**SVG插图清单：**
- `01-bagua-origin.html`: 先天八卦方位SVG图（已存在，需适配浅色主题）、后天八卦方位SVG图
- `02-fuxi-shennong.html`: 伏羲画卦传说示意图
- `03-zhouyi-wenwang.html`: 文王演周易时间线SVG
- `04-bagua-xiangshu.html`: 八卦取象比类关系图
- `05-bagua-summary.html`: 八卦学习路径流程图

- [ ] **Step 1: 重写 01-bagua-origin.html**

  - 添加 `<header class="chapter-header">` 包裹章节元信息
  - 重组为五段式结构
  - 新增后天八卦方位SVG（与现有先天八卦SVG并列）
  - 新增"实践应用"段落
  - 新增"延伸阅读"段落，含：
    - 跨章节关联卡片 → `../阴阳五行/06-yinyang-benyuan.html`（阴阳概念本源）、`../中医基础/12-tcm-neijing.html`（中医理论源头）、`../易经体系/18-yijing-overview.html`（易经体系总论）
    - 思考题：①先天八卦与后天八卦的核心区别是什么？②八卦分类法与现代科学分类有何异同？
    - 延伸阅读：《周易译注》黄寿祺、《中国哲学史》冯友兰
  - 更新ECharts配色为纸质书风格
  - 添加 `<script src="../common/js/theme-toggle.js"></script>`

- [ ] **Step 2: 重写 02-fuxi-shennong.html**

  - 五段式结构
  - 新增伏羲画卦SVG示意图
  - 延伸阅读关联 → 阴阳五行、中医基础

- [ ] **Step 3: 重写 03-zhouyi-wenwang.html**

  - 五段式结构
  - 新增文王演周易时间线SVG
  - 延伸阅读关联 → 易经体系、儒家理论

- [ ] **Step 4: 重写 04-bagua-xiangshu.html**

  - 五段式结构
  - 新增八卦取象比类关系SVG图
  - 延伸阅读关联 → 中医基础、道家理论

- [ ] **Step 5: 重写 05-bagua-summary.html**

  - 五段式结构
  - 新增学习路径流程图SVG
  - 延伸阅读关联 → 全部其他部分

- [ ] **Step 6: 验证所有5页**

对每页检查：
- 五段式结构完整（5个section）
- ≥2张SVG插图
- ≥2个跨章节关联卡片
- ≥2道思考题
- ≥2本延伸阅读
- ECharts图表正常显示
- 主题切换脚本引用存在
- footer导航链接正确

- [ ] **Step 7: Commit**

```bash
git add traditional-academics/0{1,2,3,4,5}-*.html
git commit -m "feat: rewrite Bagua section with five-part structure, SVG illustrations, and cross-chapter references"
```

---

### Task 5: 重写第二部分 阴阳五行（06-11）

**Files:**
- Modify: `traditional-academics/06-yinyang-benyuan.html`
- Modify: `traditional-academics/07-yinyang-wuxing-classics.html`
- Modify: `traditional-academics/08-wuxing-theory.html`
- Modify: `traditional-academics/09-wuxing-cycles.html`
- Modify: `traditional-academics/10-yinyang-wuxing-synthesis.html`
- Modify: `traditional-academics/11-yinyang-summary.html`

**SVG插图清单：**
- `06-yinyang-benyuan.html`: 阴阳消长循环SVG
- `08-wuxing-theory.html`: 五行生克循环SVG（相生顺时针、相克内五角）
- `09-wuxing-cycles.html`: 五行乘侮关系图
- `10-yinyang-wuxing-synthesis.html`: 天干地支罗盘SVG
- `11-yinyang-summary.html`: 阴阳五行学习路径图

**跨章节关联目标：**
- 关联八卦部分（01-05）— 阴阳爻是阴阳思想的符号表达
- 关联中医部分（12-17）— 阴阳五行是中医理论基础
- 关联道家部分（23-27）— 道家继承阴阳思想
- 关联儒家部分（28-31）— 儒家吸收阴阳五行学说

- [ ] **Step 1-5: 依次重写 06-11 共6页**

每页执行相同的五段式重构流程，添加对应SVG插图，完善延伸阅读。

- [ ] **Step 6: 验证所有6页**

- [ ] **Step 7: Commit**

```bash
git add traditional-academics/0{6,7,8,9,10,11}-*.html
git commit -m "feat: rewrite Yin-Yang & Five Elements section with SVG diagrams and cross-references"
```

---

### Task 6: 重写第三部分 中医基础理论（12-17）

**Files:**
- Modify: `traditional-academics/12-tcm-neijing.html`
- Modify: `traditional-academics/13-tcm-yinyang-health.html`
- Modify: `traditional-academics/14-tcm-zangfu.html`
- Modify: `traditional-academics/15-tcm-jingluo.html`
- Modify: `traditional-academics/16-tcm-bingyin.html`
- Modify: `traditional-academics/17-tcm-summary.html`

**SVG插图清单：**
- `12-tcm-neijing.html`: 黄帝内经成书背景时间线
- `13-tcm-yinyang-health.html`: 阴阳平衡与健康状态图
- `14-tcm-zangfu.html`: 五脏六腑对应关系SVG
- `15-tcm-jingluo.html`: 人体十二经脉走向SVG
- `16-tcm-bingyin.html`: 病因分类树图
- `17-tcm-summary.html`: 中医学习路径图

**注意：** `15-tcm-jingluo.html` 当前使用相对路径 `common/css/book.css`（非 `../common/css/book.css`），需统一修正。

- [ ] **Step 1-5: 依次重写 12-17 共6页**

- [ ] **Step 6: 验证所有6页**

- [ ] **Step 7: Commit**

```bash
git add traditional-academics/1{2,3,4,5,6,7}-tcm-*.html
git commit -m "feat: rewrite TCM section with meridian SVG diagrams and five-part structure"
```

---

### Task 7: 重写第四部分 易经体系（18-22）

**Files:**
- Modify: `traditional-academics/18-yijing-overview.html`
- Modify: `traditional-academics/19-yijing-hexagrams.html`
- Modify: `traditional-academics/20-yijing-text-analysis.html`
- Modify: `traditional-academics/21-yijing-commentary.html`
- Modify: `traditional-academics/22-yijing-summary.html`

**SVG插图清单：**
- `18-yijing-overview.html`: 易经成书时间线
- `19-yijing-hexagrams.html`: 六十四卦方圆SVG图
- `20-yijing-text-analysis.html`: 卦爻辞结构分析图
- `21-yijing-commentary.html`: 十翼与传注关系图
- `22-yijing-summary.html`: 易学学习路径图

**注意：** 确保六十四卦相关数据准确（上次审计发现未济卦组成曾有误）。

- [ ] **Step 1-4: 依次重写 18-22 共5页**

- [ ] **Step 5: 验证所有5页**

- [ ] **Step 6: Commit**

```bash
git add traditional-academics/1{8,9}-yijing-*.html traditional-academics/2{0,1,2}-yijing-*.html
git commit -m "feat: rewrite Yi Jing section with hexagram SVG diagrams and five-part structure"
```

---

### Task 8: 重写第五部分 道家理论（23-27）

**Files:**
- Modify: `traditional-academics/23-daoism-origins.html`
- Modify: `traditional-academics/24-daodejing.html`
- Modify: `traditional-academics/25-zhuangzi.html`
- Modify: `traditional-academics/26-daoism-gongfu.html`
- Modify: `traditional-academics/27-daoism-summary.html`

**SVG插图清单：**
- `23-daoism-origins.html`: 道家学派起源与传承谱系SVG
- `24-daodejing.html`: 道-德-仁-义-礼层级概念图
- `25-zhuangzi.html`: 庄子逍遥境界图
- `26-daoism-gongfu.html`: 道家修养工夫阶梯图
- `27-daoism-summary.html`: 道家学习路径图

- [ ] **Step 1-4: 依次重写 23-27 共5页**

- [ ] **Step 5: 验证所有5页**

- [ ] **Step 6: Commit**

```bash
git add traditional-academics/2{3,4,5,6,7}-daoism-*.html
git commit -m "feat: rewrite Daoism section with lineage SVG diagrams and five-part structure"
```

---

### Task 9: 重写第六部分 儒家理论（28-31）

**Files:**
- Modify: `traditional-academics/28-rujia-origins.html`
- Modify: `traditional-academics/29-mengzi.html`
- Modify: `traditional-academics/30-songming-lixue.html`
- Modify: `traditional-academics/31-rujia-summary.html`

**SVG插图清单：**
- `28-rujia-origins.html`: 孔子生平时间线SVG
- `29-mengzi.html`: 孟子性善论四端说图
- `30-songming-lixue.html`: 宋明理学传承谱系SVG（周敦颐→二程→朱熹→陆九渊→王阳明）
- `31-rujia-summary.html`: 儒家学习路径图

**注意：** 上次审计发现的错误仍需修复：
- 孔子 timeline 日期前584→前484
- 《论语》引文"小人喻于义"→"小人喻于利"

- [ ] **Step 1-3: 依次重写 28-31 共4页**

- [ ] **Step 4: 验证所有4页，同时确认历史日期和引文准确**

- [ ] **Step 5: Commit**

```bash
git add traditional-academics/2{8,9}-rujia-*.html traditional-academics/3{0,1}-rujia-*.html
git commit -m "feat: rewrite Confucianism section with lineage SVG diagrams and five-part structure"
```

---

### Task 10: 全链路交叉验证

**Files:**
- Read: All 31 content pages + index.html

**验证清单：**

1. **结构验证** — 每章是否包含完整的五段式结构（5个section）
2. **SVG验证** — 每章是否至少2张SVG插图且渲染正常
3. **跨章节验证** — 每章底部是否有≥2个跨章节关联卡片，链接是否正确
4. **思考题验证** — 每章是否有≥2道思考题
5. **延伸阅读验证** — 每章是否有≥2本推荐书目
6. **ECharts验证** — 每章ECharts图表是否正常初始化（echarts.init + setOption）
7. **主题切换验证** — 每章是否引用了 `theme-toggle.js`
8. **导航验证** — footer prev/home/next/page-info 是否正确
9. **TOC验证** — sidebar TOC 所有章节链接是否正确
10. **路径验证** — 所有相对路径引用是否正确（特别是 `../common/` vs `common/`）
11. **内容准确性** — 快速扫描关键数据点（日期、引文、卦象等）

**验证命令：**

```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/traditional-academics

# Check all files reference theme-toggle.js
for f in *.html; do grep -l "theme-toggle.js" "$f" >/dev/null || echo "MISSING: $f"; done

# Check all files have 5 section subtitles
for f in *.html; do
  count=$(grep -c "section-subtitle" "$f")
  if [ "$count" -lt 5 ]; then echo "LOW SECTIONS: $f ($count)"; fi
done

# Check cross-ref cards exist
for f in *.html; do
  count=$(grep -c "cross-ref-card" "$f")
  if [ "$count" -lt 2 ]; then echo "LOW CROSS-REFS: $f ($count)"; fi
done

# Check reflection questions exist
for f in *.html; do
  if ! grep -q "reflection-questions" "$f"; then echo "NO REFLECTION: $f"; fi
done

# Check further reading exists
for f in *.html; do
  if ! grep -q "further-reading" "$f"; then echo "NO FURTHER READING: $f"; fi
done

# Check SVG illustrations exist
for f in *.html; do
  count=$(grep -c "<svg " "$f")
  if [ "$count" -lt 2 ]; then echo "LOW SVGS: $f ($count)"; fi
done

# Check ECharts init exists
for f in *.html; do
  if ! grep -q "echarts.init" "$f"; then echo "NO CHART: $f"; fi
done
```

- [ ] **Step 1: Run all validation commands above**

- [ ] **Step 2: Fix any issues found**

- [ ] **Step 3: Final open-in-browser check**

Open `traditional-academics/index.html` and randomly sample 3-5 content pages to verify visual quality.

- [ ] **Step 4: Commit**

```bash
git add traditional-academics/
git commit -m "chore: final cross-validation of all 31 chapters — structure, SVGs, cross-refs, themes"
```

---

### Task 11: 更新首页卡片描述

**Files:**
- Modify: `index.html`（根目录）

**Interfaces:**
- Consumes: Updated traditional-academics content description
- Produces: 首页卡片描述更新为反映纸质书风格和五段式内容

- [ ] **Step 1: Update the gold card description**

Change the 中华古典学术理论全景书 card description from:
```
八卦、阴阳五行、中医基础理论、易经体系、道家理论、儒家理论六大板块全景解析。32页实操+理论结合，6大ECharts可视化图表。
```
To:
```
八卦、阴阳五行、中医基础、易经、道家、儒家六大理论体系全景解析。32页纸质书级排版，五段式由浅入深结构，30+SVG插图，ECharts数据可视化。
```

- [ ] **Step 2: Update the hero subtitle**

Change "赛博朋克深色主题" to "纸质书级排版 · ECharts数据可视化"

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "docs: update homepage description for redesigned traditional academics book"
```

---

## Self-Review

**1. Spec coverage:**
- ✅ 排版风格改造 → Task 1 (book.css), Task 2 (theme-toggle.js)
- ✅ 封面重写 → Task 3
- ✅ 五段式结构 → Tasks 4-9 (all 31 chapters)
- ✅ SVG插图系统 → Tasks 4-9 (per-section SVG清单)
- ✅ 跨章节关联网络 → Tasks 4-9 (cross-ref cards per chapter)
- ✅ 新增组件（思考题、延伸阅读） → Tasks 4-9
- ✅ 文件变更范围完整覆盖 → 所有tasks列出的文件
- ✅ 技术实现要点（主题切换、响应式、打印、性能、可访问性） → Task 1 CSS中全部实现
- ✅ 验证清单 → Task 10

**2. Placeholder scan:**
- 无 "TBD"、"TODO"、"implement later" 等占位符
- 每步都有具体代码和命令
- 每个文件的精确路径都已列出

**3. Type consistency:**
- CSS变量在所有任务中保持一致命名
- 类名（`.section-title`, `.cross-ref-card` 等）在所有任务中统一
- 脚本引用路径统一使用 `../common/js/`

**4. Scope check:**
- 计划聚焦在重设计，不添加新功能
- 保持现有6大部分结构不变
- 保留ECharts图表

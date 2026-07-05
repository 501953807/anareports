# AnaReports 七本书多页HTML站点 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将7个单文件HTML看板拆分为多页可查阅的"书籍"形式，每个看板30-50+页，基于现有内容持续深化到极限。

**Architecture:** 创建 `common/` 公共资源目录（统一CSS + 导航JS + ECharts），每个看板独立子目录，内含 `index.html`（封面+目录）+ 多个章节页。每个章节页包含顶部导航栏、左侧目录面板、主体内容区、底部页脚。

**Tech Stack:** 纯静态HTML5 + CSS3 + Vanilla JS + Apache ECharts 5.5.0 + Font Awesome 6.5.1

## Global Constraints

- 赛博朋克深色主题：背景 `#0a0e17`，强调色 `#06b6d4`/`#8b5cf6`/`#ef4444`/`#10b981`/`#f59e0b`
- 字体：Noto Sans SC（Google Fonts）
- 图标：Font Awesome 6.5.1（CDN）
- 图表：Apache ECharts 5.5.0（本地 `common/js/echarts.inline.js`）
- 响应式断点：Desktop >1200px / Tablet 768-1200px / Mobile Large 480-768px / Mobile Small <480px
- 纯静态HTML，可直接部署到GitHub Pages
- 基于现有内容深化，不推倒重来
- 每个看板30-50+页

---

# Phase 0: 基础设施

### Task 0.1: 创建公共资源目录结构

**Files:**
- Create: `common/css/book.css`
- Create: `common/js/navigation.js`
- Create: `common/js/echarts.inline.js` (copy from existing)
- Create: `common/fonts/` (empty, optional cache)

**Interfaces:**
- Consumes: Nothing (foundation task)
- Produces: Shared CSS variables, navigation functions, ECharts library

- [ ] **Step 1: 复制ECharts到common目录**

```bash
cp /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/echarts.inline.js /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/js/echarts.inline.js
mkdir -p /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/css
mkdir -p /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/js
mkdir -p /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/fonts
```

- [ ] **Step 2: 创建统一CSS样式表 `common/css/book.css`**

```css
/* ===== AnaReports Book Theme ===== */
:root {
  --bg: #0a0e17;
  --surface: #111827;
  --surface2: #1e293b;
  --border: #1e2a3a;
  --text: #e2e8f0;
  --text2: #94a3b8;
  --cyan: #06b6d4;
  --purple: #8b5cf6;
  --red: #ef4444;
  --green: #10b981;
  --orange: #f59e0b;
  --pink: #ec4899;
  --gold: #eab308;
  --glow-cyan: 0 0 12px rgba(6,182,212,0.4);
  --glow-purple: 0 0 12px rgba(139,92,246,0.4);
  --glow-red: 0 0 12px rgba(239,68,68,0.4);
  --glow-green: 0 0 12px rgba(16,185,129,0.4);
  --glow-orange: 0 0 12px rgba(245,158,11,0.4);
  --glow-pink: 0 0 12px rgba(236,72,153,0.4);
  --glow-gold: 0 0 12px rgba(234,179,8,0.4);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-width: 320px;
  line-height: 1.8;
}

/* ===== Top Navigation Bar ===== */
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 8px 20px;
  display: flex; align-items: center; justify-content: space-between;
  height: 48px;
}
.top-nav .nav-left { display: flex; align-items: center; gap: 12px; }
.top-nav .nav-book-name {
  font-size: 13px; font-weight: 700; color: var(--cyan);
  text-decoration: none; white-space: nowrap;
}
.top-nav .nav-divider { color: var(--text2); font-size: 12px; }
.top-nav .nav-chapter-title {
  font-size: 13px; color: var(--text); white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis; max-width: 300px;
}
.top-nav .nav-right { display: flex; align-items: center; gap: 8px; }
.top-nav .nav-btn {
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text2); padding: 4px 12px; border-radius: 4px;
  font-size: 12px; cursor: pointer; text-decoration: none;
  transition: all 0.2s;
}
.top-nav .nav-btn:hover { border-color: var(--cyan); color: var(--cyan); }
.top-nav .nav-toc-toggle { display: none; }

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
  font-size: 13px; font-weight: 700; color: var(--cyan);
  margin-bottom: 12px; padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}
.sidebar .toc-list { list-style: none; }
.sidebar .toc-list li { margin-bottom: 2px; }
.sidebar .toc-list a {
  display: block; padding: 4px 8px; font-size: 12px;
  color: var(--text2); text-decoration: none; border-radius: 4px;
  transition: all 0.2s; line-height: 1.4;
}
.sidebar .toc-list a:hover { background: var(--surface2); color: var(--text); }
.sidebar .toc-list a.active {
  background: rgba(6,182,212,0.15); color: var(--cyan);
  border-left: 2px solid var(--cyan); padding-left: 6px;
}
.sidebar .toc-list .toc-chapter {
  font-weight: 600; color: var(--text); font-size: 13px;
  margin-top: 8px; padding-top: 8px;
  border-top: 1px solid var(--border);
}

/* ===== Main Content ===== */
.content {
  margin-left: 260px; padding: 30px 40px;
  min-height: calc(100vh - 48px);
  max-width: 900px;
}
.sidebar.closed ~ .content { margin-left: 0; }

/* ===== Page Footer ===== */
.page-footer {
  margin-left: 260px; padding: 20px 40px;
  border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  font-size: 12px; color: var(--text2);
}
.sidebar.closed ~ .page-footer { margin-left: 0; }
.page-footer .nav-prev, .page-footer .nav-next {
  color: var(--cyan); text-decoration: none;
  padding: 6px 12px; border: 1px solid var(--border);
  border-radius: 4px; transition: all 0.2s;
}
.page-footer .nav-prev:hover, .page-footer .nav-next:hover {
  border-color: var(--cyan); background: rgba(6,182,212,0.1);
}
.page-footer .nav-home { color: var(--text2); text-decoration: none; }

/* ===== Section Titles ===== */
.section-title {
  font-size: 22px; font-weight: 700; margin: 30px 0 20px;
  padding-left: 14px; border-left: 3px solid var(--cyan); color: var(--cyan);
}
.section-subtitle {
  font-size: 16px; font-weight: 600; color: var(--text); margin: 24px 0 14px;
}

/* ===== Cards ===== */
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; margin: 12px 0;
}
.card.highlight { border-color: var(--cyan); box-shadow: var(--glow-cyan); }
.card.warning { border-color: var(--orange); }
.card.danger { border-color: var(--red); }

/* ===== Data Card ===== */
.data-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; text-align: center; margin: 8px 0;
}
.data-card .value { font-size: 24px; font-weight: 700; color: var(--cyan); }
.data-card .label { font-size: 12px; color: var(--text2); margin-top: 4px; }

/* ===== Table ===== */
.data-table {
  width: 100%; border-collapse: collapse; margin: 16px 0;
  font-size: 13px;
}
.data-table th {
  background: var(--surface2); color: var(--cyan);
  padding: 10px 12px; text-align: left; font-weight: 600;
  border-bottom: 2px solid var(--border);
}
.data-table td {
  padding: 8px 12px; border-bottom: 1px solid var(--border);
  color: var(--text);
}
.data-table tr:hover td { background: var(--surface2); }

/* ===== Case Box ===== */
.case-box {
  background: rgba(139,92,246,0.08); border: 1px solid var(--purple);
  border-radius: 8px; padding: 14px; margin: 14px 0;
}
.case-box .case-title {
  font-size: 13px; font-weight: 700; color: var(--purple); margin-bottom: 6px;
}
.case-box .case-body { font-size: 13px; color: var(--text2); line-height: 1.7; }

/* ===== Tip Box ===== */
.tip-box {
  background: rgba(6,182,212,0.08); border: 1px solid var(--cyan);
  border-radius: 8px; padding: 14px; margin: 14px 0;
}
.tip-box .tip-title {
  font-size: 13px; font-weight: 700; color: var(--cyan); margin-bottom: 6px;
}
.tip-box .tip-body { font-size: 13px; color: var(--text2); line-height: 1.7; }

/* ===== Chart Container ===== */
.chart-container {
  width: 100%; height: 400px; margin: 20px 0;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; overflow: hidden;
}

/* ===== Steps List ===== */
.steps-list { counter-reset: step; list-style: none; padding: 0; }
.steps-list li {
  counter-increment: step; padding: 10px 10px 10px 50px;
  position: relative; margin: 8px 0; background: var(--surface);
  border-radius: 6px; font-size: 13px; line-height: 1.7;
}
.steps-list li::before {
  content: counter(step); position: absolute; left: 10px; top: 10px;
  width: 28px; height: 28px; background: var(--cyan); color: var(--bg);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
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
  background: var(--cyan); box-shadow: 0 0 8px var(--cyan);
}
.timeline-item .tl-year { font-size: 12px; font-weight: 700; color: var(--cyan); }
.timeline-item .tl-desc { font-size: 13px; color: var(--text2); line-height: 1.6; }

/* ===== Grid ===== */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }

/* ===== Badge ===== */
.badge {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 600;
}
.badge.cyan { background: rgba(6,182,212,0.15); color: var(--cyan); }
.badge.purple { background: rgba(139,92,246,0.15); color: var(--purple); }
.badge.red { background: rgba(239,68,68,0.15); color: var(--red); }
.badge.green { background: rgba(16,185,129,0.15); color: var(--green); }
.badge.orange { background: rgba(245,158,11,0.15); color: var(--orange); }

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
  .section-title { font-size: 18px; }
  .chart-container { height: 250px; }
  .top-nav { padding: 6px 12px; height: 42px; }
  .sidebar { top: 42px; width: 220px; }
  .sidebar.open ~ .content { margin-left: 0; }
}
```

- [ ] **Step 3: 创建统一导航JS `common/js/navigation.js`**

```javascript
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
    chapters.forEach(function(ch, i) {
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
```

- [ ] **Step 4: 验证common目录结构**

```bash
ls -la /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/css/book.css
ls -la /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/js/navigation.js
ls -la /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/common/js/echarts.inline.js
```

- [ ] **Step 5: 提交**

```bash
git add common/
git commit -m "feat: 创建公共资源目录（CSS + 导航JS + ECharts）"
```

**Interfaces:**
- Consumes: Nothing
- Produces: `common/css/book.css`, `common/js/navigation.js`, `common/js/echarts.inline.js`

---

### Task 0.2: 创建总入口index.html

**Files:**
- Modify: `/Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/index.html` (rewrite as book cover wall)

**Interfaces:**
- Consumes: `common/css/book.css`
- Produces: Seven-book cover wall linking to each book's `index.html`

- [ ] **Step 1: 重写总入口 `index.html`**

创建新的封面墙页面，包含七本书的封面卡片，每张卡片显示：
- 书名
- 图标（emoji）
- 一句话简介
- 总章节数
- 点击进入该书目录

每个卡片链接到对应看板目录的 `index.html`。

- [ ] **Step 2: 验证所有链接指向正确**

```bash
# Check all book links exist
for book in creators money-laundering guangzhou pharma ev-motorcycle china-japan smart-devices; do
  echo "Checking $book/index.html..."
done
```

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "feat: 重写总入口为七本书封面墙"
```

**Interfaces:**
- Consumes: `common/css/book.css`
- Produces: Total entry page linking to all 7 books

---

### Task 0.3: 创建页面模板

**Files:**
- Create: `templates/page-template.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/navigation.js`, `common/js/echarts.inline.js`
- Produces: Reusable page template for all book chapters

- [ ] **Step 1: 创建页面模板**

模板包含完整的HTML结构：
- `<head>`：meta + 链接 `../common/css/book.css` + Font Awesome + Google Fonts
- `<body>`：
  - `<nav class="top-nav">`：书名 + 章节标题 + 目录按钮 + 上一节/下一节
  - `<aside class="sidebar">`：TOC容器 + 目录列表
  - `<main class="content">`：章节标题 + 内容区域
  - `<footer class="page-footer">`：上一页/下一页导航 + 返回入口
- `<script>`：链接 `../common/js/echarts.inline.js` + `../common/js/navigation.js` + 页面专属JS

- [ ] **Step 2: 提交**

```bash
git add templates/
git commit -m "chore: 创建多页HTML页面模板"
```

**Interfaces:**
- Consumes: Task 0.1 outputs
- Produces: Reusable page template

---

# Phase 1: 创作者经济看板

### Task 1.1: 分析现有内容 + 设计目录结构

**Files:**
- Read: `全球创作者经济全景赚钱行当与平台看板.html`
- Create: `docs/superpowers/plans/creators-chapter-map.md`

**Interfaces:**
- Consumes: Nothing
- Produces: Chapter map mapping existing sections to new pages

- [ ] **Step 1: 读取现有看板文件，提取所有section/module**

分析 `全球创作者经济全景赚钱行当与平台看板.html` 中的：
- 所有 `<section>` 块
- 所有 `<h2>` / `<h3>` 标题
- 所有图表ID和对应内容
- 所有表格和卡片

- [ ] **Step 2: 设计章节映射**

将现有内容拆分为30-50+页，每页一个子主题。例如：
- `index.html` → 总览 + 目录
- `01-overview.html` → 全局数据大字报（6个核心指标）
- `02-social-media.html` → 自媒体博主深度解析
- `03-independent-games.html` → 独立游戏开发者
- ...（每个行当一页）
- `04-platforms-video.html` → 视频类平台详解
- `05-platforms-text.html` → 图文类平台详解
- ...（每个平台分类一页）
- `06-monetization-ads.html` → 广告分成深度拆解
- ...（每种变现手段一页）
- `07-income-analysis.html` → 收入分布数据分析
- `08-roadmap.html` → 新手起步路线图
- `09-risks.html` → 避坑指南
- `10-future.html` → 未来趋势展望
- `11-cases.html` → 典型案例研究

- [ ] **Step 3: 创建章节映射文档并提交**

```bash
git add docs/superpowers/plans/creators-chapter-map.md
git commit -m "docs: 创作者经济看板章节映射设计"
```

**Interfaces:**
- Consumes: `全球创作者经济全景赚钱行当与平台看板.html`
- Produces: Chapter map for creators board

---

### Task 1.2: 创建创作者经济看板目录结构

**Files:**
- Create: `creators/index.html` (book cover + TOC)
- Create: `creators/css/` (empty, per-book CSS overrides if needed)

**Interfaces:**
- Consumes: Task 0.1 (book.css), Task 0.3 (page template)
- Produces: Book directory structure with cover page

- [ ] **Step 1: 创建 `creators/index.html`**

基于页面模板，创建创作者经济书的封面+目录页：
- 书名：全球创作者经济全景赚钱行当与平台看板
- 封面图/图标
- 总目录列表（所有章节链接）
- 统计信息（总页数、图表数等）

- [ ] **Step 2: 创建目录**

```bash
mkdir -p /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/creators
```

- [ ] **Step 3: 验证封面页可正常访问**

在浏览器中打开 `file:///Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/creators/index.html` 确认：
- 样式正常加载
- 目录链接正确
- 响应式布局正常

- [ ] **Step 4: 提交**

```bash
git add creators/
git commit -m "feat: 创建创作者经济看板目录结构和封面页"
```

**Interfaces:**
- Consumes: Task 0.1, Task 0.3
- Produces: `creators/index.html`

---

### Task 1.3+: 逐页创建和深化（每个章节页一个Task）

由于创作者经济看板需要30-50+页，每个章节页的创建遵循相同模式：

**每页创建步骤：**
1. 基于页面模板创建新HTML文件
2. 从现有看板中提取相关内容
3. 在该内容基础上深化5个维度：
   - 方向性：补充宏观格局、历史脉络、政策分析
   - 操作性：补充具体使用指南、注册步骤、操作流程
   - 数据性：补充市场规模、收入分布、平台对比数据
   - 案例性：补充真实人物/企业案例
   - 前瞻性：补充趋势预测、风险提示
4. 添加1-3个ECharts图表（从现有看板迁移或新增）
5. 配置左侧目录（navigation.js generateTOC）
6. 配置上一页/下一页导航
7. 在浏览器中验证渲染

**文件名规范：** `NN-descriptive-name.html`（两位数字序号 + 连字符 + 小写英文）

**示例：**
```bash
# 第1章：全局概览
cp templates/page-template.html creators/01-overview.html
# 编辑内容...

# 第2章：自媒体博主
cp templates/page-template.html creators/02-social-media.html
# 编辑内容...
```

每个章节页的提交：
```bash
git add creators/NN-*.html
git commit -m "feat(creators): 第N章 - [章节标题]"
```

**需要创建的章节页清单（创作者经济）：**
- `01-overview.html` — 全局概览（6个核心指标）
- `02-social-media.html` — 自媒体博主
- `03-independent-games.html` — 独立游戏开发者
- `04-web-novel.html` — 网文/电子书作者
- `05-podcast.html` — 播客主播
- `06-online-course.html` — 在线课程讲师
- `07-freelancer.html` — 自由职业者
- `08-photographer.html` — 摄影师/插画师
- `09-musician.html` — 音乐人/独立歌手
- `10-ecommerce.html` — 电商带货/联盟营销
- `11-live-streaming.html` — 直播打赏/订阅制
- `12-platforms-video.html` — 视频类平台
- `13-platforms-text.html` — 图文类平台
- `14-platforms-audio.html` — 音频类平台
- `15-platforms-live.html` — 直播类平台
- `16-platforms-skill.html` — 电商/技能类平台
- `17-monetization-ads.html` — 广告分成
- `18-monetization-brand.html` — 品牌赞助
- `19-monetization-subscribe.html` — 付费订阅
- `20-monetization-tip.html` — 打赏礼物
- `21-monetization-ecommerce.html` — 电商带货
- `22-monetization-affiliate.html` — 联盟营销
- `23-monetization-knowledge.html` — 知识付费
- `24-monetization-ip.html` — IP授权
- `25-income-analysis.html` — 收入数据分析
- `26-roadmap-beginner.html` — 新手起步
- `27-roadmap-advanced.html` — 进阶运营
- `28-risks.html` — 避坑指南
- `29-future.html` — 未来趋势
- `30-cases.html` — 典型案例

（共30页，可根据深化需要扩展到40-50页）

---

# Phase 2-7: 其余6个看板

每个看板遵循与Phase 1相同的模式：

### Task 2.x: 地下钱庄看板
- 源文件：`全球地下钱庄与洗钱全景风险看板.html`
- 目标目录：`money-laundering/`
- 预计页数：30-50页

### Task 3.x: 广州吃喝玩乐看板
- 源文件：`广州吃喝玩乐+供应链全景看板.html`
- 目标目录：`guangzhou/`
- 预计页数：30-50页

### Task 4.x: 医药产业看板
- 源文件：`中国医药产业全球竞争力与中药发展全景看板.html`
- 目标目录：`pharma/`
- 预计页数：30-50页

### Task 5.x: 新能源汽车看板
- 源文件：`中国新能源汽车与电动摩托车全产业链全景看板.html`
- 目标目录：`ev-motorcycle/`
- 预计页数：30-50页

### Task 6.x: 中日经济周期看板
- 源文件：`中日经济周期对比与个人投资出路看板.html`
- 目标目录：`china-japan/`
- 预计页数：30-50页

### Task 7.x: 智能设备看板
- 源文件：`智能手环与智能药盒产品开发全景看板.html`
- 目标目录：`smart-devices/`
- 预计页数：30-50页

---

## 实施顺序建议

虽然7个看板并行推进，但建议按以下优先级逐个完成以快速验证流程：

1. **创作者经济**（Phase 1）— 最新完成，结构最清晰，作为模板
2. **地下钱庄**（Phase 2）— 已完成v2.0重写
3. **中日经济周期**（Phase 6）— 文件较小（724行）
4. **医药产业**（Phase 4）— 中等复杂度
5. **智能设备**（Phase 7）— 中等复杂度
6. **广州吃喝玩乐**（Phase 3）— 文件较大（2042行），含地图
7. **新能源汽车**（Phase 5）— 文件最大（2027行），最复杂

每个看板完成后立即部署测试，确认所有链接和图表正常。

---

## 验证清单

每个看板完成后需验证：
- [ ] 封面页 `index.html` 可正常访问
- [ ] 所有章节页可正常访问
- [ ] 左侧目录列表完整且当前页高亮
- [ ] 上一页/下一页导航正常工作
- [ ] 所有ECharts图表正常渲染
- [ ] 响应式设计在768px和480px下正常
- [ ] 所有内部链接无404
- [ ] 总入口 `index.html` 链接正确

---

## 风险控制

| 风险 | 缓解 |
|------|------|
| 单文件过大导致编辑困难 | 每个新页面基于模板创建，不修改源文件 |
| 深化内容质量不一 | 遵循统一的深化5维度标准 |
| 图表迁移遗漏 | 每页创建时清点图表ID |
| 导航链接断裂 | 每页提交后立即在浏览器验证 |
| 工作量超预期 | 先完成创作者经济作为模板，确认流程后再批量复制 |

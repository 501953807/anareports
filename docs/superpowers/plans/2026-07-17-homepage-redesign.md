# AnaReports 首页视觉升级与看板合并实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重写 `index.html`，将 11 本书 + 11 个看板合并为统一卡片，添加粒子背景 + 3D 卡片效果 + 分类折叠。

**Architecture:** 单页纯静态 HTML，JS 数据驱动渲染卡片。粒子系统用原生 Canvas API（~80 节点）。3D 卡片用 CSS perspective + JS mousemove tilt。分类组用 `<details>/<summary>` 原生折叠。

**Tech Stack:** 纯 HTML5 + CSS3 + Vanilla JS (ES6+)。Font Awesome 6.5.1（已有）。不引入任何第三方 JS 库。

## Global Constraints

- 只修改 `index.html` 一个文件，不碰任何书籍或看板 HTML 文件
- 不引入任何第三方 JS 库，粒子系统和 3D 效果全部原生实现
- 保持现有 CSS 变量（--bg / --surface / --cyan 等）完全一致
- 响应式：移动端 grid 单列，粒子节点数减半
- 所有 11 本书的数据（书名、描述、链接、看板路径、高亮数据）必须完整准确
- 卡片 hover 倾斜范围 ±8deg，浮起 translateY(-8px)

---

### Task 1: 构建 BOOK_DATA 数据源

**Files:**
- Modify: `index.html` — 在 `</style>` 前注入 `<script>` 块，定义 `const BOOK_DATA = [...]`

**Interfaces:**
- Produces: `BOOK_DATA` 数组，每个元素包含 name, shortName, desc, group, icon, color, pages, charts, tags[], highlights[{label,value}], bookUrl, kanbanUrl

**步骤：**

- [ ] **Step 1: 定义 BOOK_DATA 常量**

在 `<body>` 之前插入 `<script>` 标签，写入完整的 11 本书数据：

```js
const BOOK_DATA = [
  {
    name: "《重庆产业格局与未来展望：成渝双城经济圈深度研判》",
    shortName: "重庆产业格局",
    desc: "常住人口与户籍制度深度解析、GDP 与产业结构全景、成渝双城经济圈协同路径、汽车制造与电子信息两大支柱产业。",
    group: "regional",
    icon: "fa-mountain-city",
    color: "cyan",
    pages: 32,
    charts: 32,
    tags: ["成渝经济圈", "汽车制造", "电子信息"],
    highlights: [
      { label: "GDP", value: "≈3万亿" },
      { label: "人口", value: "≈3200万" },
      { label: "支柱产业", value: "2大" }
    ],
    bookUrl: "chongqing/index.html",
    kanbanUrl: "重庆产业全景研判看板_成渝经济圈_制造业_人口结构.html"
  },
  {
    name: "《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》",
    shortName: "大湾区民生经济",
    desc: "千年商都概览与广东全省经济结构、广式早茶·烧腊·街头小吃美食地图、八大批发市场品类与六大城区商贸格局。",
    group: "regional",
    icon: "fa-city",
    color: "green",
    pages: 31,
    charts: 9,
    tags: ["大湾区", "美食经济", "跨境电商"],
    highlights: [
      { label: "GDP", value: "≈3万亿" },
      { label: "人口", value: "≈1880万" },
      { label: "跨境电商", value: "全国第一" }
    ],
    bookUrl: "guangzhou/index.html",
    kanbanUrl: "大湾区民生经济全景看板_广府消费_供应链_三产结构.html"
  },
  {
    name: "《中华古典学术源流与理论体系：从易经八卦到宋明理学》",
    shortName: "中华古典学术",
    desc: "八卦起源与伏羲神农、周易文王系辞、阴阳五行经典体系、中医藏象经络病机、道教修炼功法、儒家孟子女心学。",
    group: "academic",
    icon: "fa-scroll",
    color: "gold",
    pages: 32,
    charts: 21,
    tags: ["易经", "中医", "儒道"],
    highlights: [
      { label: "篇章", value: "32" },
      { label: "图表", value: "21" },
      { label: "学派", value: "多源" }
    ],
    bookUrl: "traditional-academics/index.html",
    kanbanUrl: "中华古典学术体系看板_易学_中医_儒道_阴阳五行.html"
  },
  {
    name: "《全球地下金融与洗钱机制研判：渠道·追踪·合规与反制》",
    shortName: "全球地下金融与洗钱",
    desc: "地下钱庄对敲、哈瓦拉体系、虚拟币混币/跨链、贸易洗钱、离岸空壳公司嵌套、东南亚杀猪盘 7 步链路。",
    group: "academic",
    icon: "fa-building-columns",
    color: "red",
    pages: 30,
    charts: 8,
    tags: ["反洗钱", "地下钱庄", "虚拟币"],
    highlights: [
      { label: "洗钱规模", value: "$8-2万亿" },
      { label: "AI洗钱增速", value: "340%" },
      { label: "链上犯罪", value: "$209亿" }
    ],
    bookUrl: "money-laundering/index.html",
    kanbanUrl: "全球地下金融与洗钱风险研判看板_渠道图谱_链上追踪_执法合规.html"
  },
  {
    name: "《中日经济周期比较研究：日本失去的三十年与中国路径选择》",
    shortName: "中日经济周期比较",
    desc: "中国经济周期演进、日本失去的三十年经验教训、GDP/工资/资产价格数据对比、政策应对时间线、个人投资出路。",
    group: "macro",
    icon: "fa-chart-line",
    color: "pink",
    pages: 30,
    charts: 12,
    tags: ["经济周期", "中日对比", "投资"],
    highlights: [
      { label: "日本失去年代", value: "30年" },
      { label: "图表", value: "12" },
      { label: "对比维度", value: "多维度" }
    ],
    bookUrl: "china-japan/index.html",
    kanbanUrl: "中日经济周期对比看板_宏观数据_政策应对_投资策略.html"
  },
  {
    name: "《全球创作者经济生态与变现模式研究：十大行当·八大手段·平台图谱》",
    shortName: "全球创作者经济",
    desc: "自媒体博主、独立游戏开发者、网文作者、播客主播、在线课程讲师、自由职业者、摄影师、音乐人、电商带货、直播打赏。",
    group: "industry",
    icon: "fa-palette",
    color: "purple",
    pages: 32,
    charts: 10,
    tags: ["创作者经济", "变现手段", "平台图谱"],
    highlights: [
      { label: "赚钱行当", value: "10大" },
      { label: "变现手段", value: "8种" },
      { label: "平台", value: "20+" }
    ],
    bookUrl: "creators/index.html",
    kanbanUrl: "全球创作者经济生态看板_赚钱行当_平台矩阵_变现模型.html"
  },
  {
    name: "《AI时代的创作者经济与数字版权保护：法律·技术·商业化全链路》",
    shortName: "AI创作者经济与版权",
    desc: "AI 创作者经济全景图谱、版权法与合理使用原则、AI 生成内容版权归属、区块链数字水印认证、侵权监测与取证。",
    group: "industry",
    icon: "fa-robot",
    color: "green",
    pages: 32,
    charts: 32,
    tags: ["AI版权", "区块链认证", "侵权维权"],
    highlights: [
      { label: "AI工具", value: "海量" },
      { label: "图表", value: "32" },
      { label: "版权类型", value: "多类" }
    ],
    bookUrl: "creators-ai/index.html",
    kanbanUrl: "AI创作者经济与数字版权看板_版权法_区块链认证_侵权维权.html"
  },
  {
    name: "《中国新能源汽车与电动摩托车产业链全景：从上游矿产到出海战略》",
    shortName: "NEV与电动摩托车产业链",
    desc: "NEV 产业链上游矿产（锂/钴/镍）、电池系统深度解析、电机与电控核心技术、电动摩托车全球市场与出海战略。",
    group: "industry",
    icon: "fa-car",
    color: "red",
    pages: 29,
    charts: 11,
    tags: ["新能源车", "电动摩托", "全产业链"],
    highlights: [
      { label: "产业链环节", value: "全链条" },
      { label: "图表", value: "11" },
      { label: "核心部件", value: "三电" }
    ],
    bookUrl: "ev-motorcycle/index.html",
    kanbanUrl: "新能源整车产业链看板_NEV_电动摩托_电池_电机_电控_出海.html"
  },
  {
    name: "《中国医药产业全球竞争力与中药现代化路径研究》",
    shortName: "中国医药产业竞争力",
    desc: "全球医药产业格局、中国医药竞争力分析、中药现代化发展路径、十大前沿医药赛道深度、原料药霸权、创新药管线。",
    group: "industry",
    icon: "fa-pills",
    color: "orange",
    pages: 31,
    charts: 10,
    tags: ["医药产业", "中药", "全球化"],
    highlights: [
      { label: "赛道", value: "10大" },
      { label: "图表", value: "10" },
      { label: "全球排名", value: "前列" }
    ],
    bookUrl: "pharma/index.html",
    kanbanUrl: "中国医药产业竞争力看板_全球格局_中药现代化_前沿赛道.html"
  },
  {
    name: "《智能健康硬件产品开发与商业化研究：手环·药盒·健康监测》",
    shortName: "智能健康硬件开发",
    desc: "智能手环产品规划（防走失+健康监测）、智能药盒技术方案、健康监测功能设计、产品开发全流程、市场竞争分析。",
    group: "industry",
    icon: "fa-microchip",
    color: "gold",
    pages: 30,
    charts: 9,
    tags: ["智能硬件", "产品开发", "健康"],
    highlights: [
      { label: "产品类型", value: "2类" },
      { label: "图表", value: "9" },
      { label: "功能模块", value: "多" }
    ],
    bookUrl: "smart-devices/index.html",
    kanbanUrl: "智能健康硬件开发看板_产品规划_技术方案_市场竞争_商业策略.html"
  },
  {
    name: "《即时配送与最后一公里商业模式研究：平台博弈·经济学研判与全球比较》",
    shortName: "即时配送与最后一公里",
    desc: "即时配送、社区团购、即时零售、积分经济、平台博弈与技术驱动六大板块全景解析。覆盖美团/Douyin/饿了么等平台。",
    group: "industry",
    icon: "fa-truck-fast",
    color: "cyan",
    pages: 63,
    charts: 20,
    tags: ["O2O", "即时配送", "平台博弈", "AI调度"],
    highlights: [
      { label: "页数", value: "63" },
      { label: "图表", value: "20+" },
      { label: "经济学派", value: "12+" }
    ],
    bookUrl: "last-mile-commerce/index.html",
    kanbanUrl: "即时配送与最后一公里商业看板_O2O_社区团购_积分经济_平台博弈.html"
  }
];
```

- [ ] **Step 2: 定义分类元数据**

紧随 BOOK_DATA 之后：

```js
const GROUPS = [
  { key: "regional", label: "第一辑 · 地域市场分析", icon: "fa-map-location-dot", color: "cyan" },
  { key: "academic", label: "第二辑 · 学术与文化研究", icon: "fa-book-open", color: "red" },
  { key: "macro", label: "第三辑 · 宏观经济分析", icon: "fa-chart-line", color: "pink" },
  { key: "industry", label: "第四辑 · 产业专题研究", icon: "fa-industry", color: "purple" }
];

// Map book color class to highlight accent colors
const HIGHLIGHT_COLORS = {
  cyan: "#06b6d4", purple: "#8b5cf6", red: "#ef4444",
  green: "#10b981", orange: "#f59e0b", pink: "#ec4899", gold: "#eab308"
};
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add BOOK_DATA and GROUPS data structures"
```

### Task 2: 实现卡片渲染引擎

**Files:**
- Modify: `index.html` — 在 Task 1 的 script 块中追加渲染函数

**Interfaces:**
- Consumes: `BOOK_DATA`, `GROUPS`, `HIGHLIGHT_COLORS` from Task 1
- Produces: DOM 元素插入到 `.container` 内

**步骤：**

- [ ] **Step 1: 实现 renderCards() 函数**

```js
function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderCards() {
  const container = document.querySelector('.container');
  
  // Remove old book cards and kanban section, keep hero and footer
  container.querySelectorAll('.group-section').forEach(el => el.remove());
  container.querySelector('.kanban-section')?.remove();
  
  GROUPS.forEach(group => {
    const books = BOOK_DATA.filter(b => b.group === group.key);
    if (books.length === 0) return;
    
    // Create details/summary collapsible group
    const section = document.createElement('div');
    section.className = 'group-section';
    section.dataset.group = group.key;
    
    section.innerHTML = `
      <details open>
        <summary class="group-summary">
          <i class="fas ${group.icon}"></i>
          <span>${group.label}</span>
          <small>(${books.length})</small>
        </summary>
        <div class="books-grid" data-group="${group.key}"></div>
      </details>
    `;
    
    // Insert before footer
    const footer = container.querySelector('footer');
    container.insertBefore(section, footer);
    
    // Render each card
    const grid = section.querySelector('.books-grid');
    books.forEach(book => {
      const card = document.createElement('div');
      card.className = `book-card ${book.color}`;
      card.dataset.name = book.shortName;
      card.dataset.search = `${book.name} ${book.desc} ${book.tags.join(' ')}`.toLowerCase();
      
      const hc = HIGHLIGHT_COLORS[book.color] || '#06b6d4';
      
      card.innerHTML = `
        <div class="card-header">
          <div class="card-icon"><i class="fas ${book.icon}"></i></div>
          <div class="card-title">${escapeHtml(book.name)}</div>
        </div>
        <div class="card-desc">${escapeHtml(book.desc)}</div>
        <div class="card-tags">
          ${book.tags.map(t => `<span class="card-tag">${t}</span>`).join('')}
        </div>
        <div class="card-meta">
          <span class="page-count"><i class="fas fa-file-alt"></i> ${book.pages} 页</span>
          <span><i class="fas fa-chart-bar"></i> ${book.charts} 图表</span>
        </div>
        <div class="card-highlights">
          ${book.highlights.map(h => `
            <div class="highlight-item">
              <span class="highlight-value" style="color:${hc}">${h.value}</span>
              <span class="highlight-label">${h.label}</span>
            </div>
          `).join('')}
        </div>
        <div class="card-actions">
          <a href="${book.bookUrl}" class="btn btn-book">
            <i class="fas fa-book-open"></i> 进入书籍
          </a>
          <a href="${book.kanbanUrl}" class="btn btn-kanban">
            <i class="fas fa-chart-column"></i> 查看看板
          </a>
        </div>
      `;
      
      grid.appendChild(card);
    });
  });
}

// Run on load
document.addEventListener('DOMContentLoaded', renderCards);
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: implement card rendering engine with data-driven DOM generation"
```

### Task 3: 实现粒子背景系统

**Files:**
- Modify: `index.html` — 在 `<body>` 末尾添加 `<canvas id="particle-bg">` 和粒子系统 JS

**Interfaces:**
- Produces: 全屏固定定位 Canvas，~80 个浮动粒子节点，距离 < 150px 时连线

**步骤：**

- [ ] **Step 1: 添加 Canvas 元素**

在 `<body>` 最前面（`.container` 之前）：

```html
<canvas id="particle-bg"></canvas>
<div class="container">
```

- [ ] **Step 2: 实现粒子系统**

在 `renderCards()` 之后追加：

```js
// Particle background system
(function initParticles() {
  const canvas = document.getElementById('particle-bg');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  let w, h, particles;
  const PARTICLE_COUNT = window.innerWidth < 768 ? 40 : 80;
  const CONNECTION_DIST = 150;
  const SPEED = 0.3;
  
  const COLORS = ['#06b6d4', '#8b5cf6', '#ef4444', '#10b981', '#f59e0b', '#ec4899', '#eab308'];
  
  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }
  
  function createParticles() {
    particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * SPEED,
        vy: (Math.random() - 0.5) * SPEED,
        r: Math.random() * 2 + 1,
        color: COLORS[Math.floor(Math.random() * COLORS.length)]
      });
    }
  }
  
  function draw() {
    ctx.clearRect(0, 0, w, h);
    
    // Draw connections first
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECTION_DIST) {
          const alpha = (1 - dist / CONNECTION_DIST) * 0.15;
          ctx.strokeStyle = `rgba(6,182,212,${alpha})`;
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
    
    // Draw and update particles
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = 0.6;
      ctx.fill();
      ctx.globalAlpha = 1;
      
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;
    });
    
    requestAnimationFrame(draw);
  }
  
  resize();
  createParticles();
  draw();
  window.addEventListener('resize', () => { resize(); createParticles(); });
})();
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add particle background canvas with floating nodes and connection lines"
```

### Task 4: 实现 3D 卡片视差倾斜效果

**Files:**
- Modify: `index.html` — 追加 3D tilt 交互 JS

**Interfaces:**
- Consumes: `.book-card` elements rendered by Task 2
- Produces: 鼠标在卡片上移动时产生 rotateX/Y 倾斜 + 浮起发光

**步骤：**

- [ ] **Step 1: 添加 3D Tilt 交互**

```js
// 3D card tilt effect
document.addEventListener('mousemove', (e) => {
  document.querySelectorAll('.book-card').forEach(card => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Check if mouse is over this card
    if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -8;
      const rotateY = ((x - centerX) / centerX) * 8;
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
      card.style.transition = 'transform 0.1s ease-out';
    } else {
      card.style.transform = '';
      card.style.transition = 'transform 0.4s ease-out';
    }
  });
});
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: add 3D card parallax tilt effect on mouse move"
```

### Task 5: 实现搜索过滤和分类折叠增强

**Files:**
- Modify: `index.html` — 添加搜索框和折叠增强

**Interfaces:**
- Consumes: `BOOK_DATA` cards with `data-search` attributes
- Produces: 实时搜索过滤 + 分类组平滑折叠动画

**步骤：**

- [ ] **Step 1: 在 Hero 后添加搜索框**

```html
<!-- Search -->
<div class="search-bar" style="text-align:center;margin-bottom:32px;">
  <input type="text" id="bookSearch" placeholder="🔍 搜索书籍名称、标签、关键词..." 
    style="width:100%;max-width:500px;padding:12px 20px;border-radius:24px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:14px;outline:none;transition:border-color 0.2s;"
    onfocus="this.style.borderColor='var(--cyan)'" onblur="this.style.borderColor='var(--border)'">
</div>
```

- [ ] **Step 2: 搜索过滤逻辑**

```js
// Search filter
document.getElementById('bookSearch')?.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  document.querySelectorAll('.book-card').forEach(card => {
    const match = !query || card.dataset.search.includes(query);
    card.style.display = match ? '' : 'none';
  });
  // Hide empty groups
  document.querySelectorAll('.group-section').forEach(section => {
    const visibleCards = section.querySelectorAll('.book-card:not([style*="display: none"])');
    section.style.display = visibleCards.length > 0 ? '' : 'none';
  });
});
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add search bar with real-time card filtering and empty group hiding"
```

### Task 6: 更新 CSS 样式（3D + 粒子 + 新卡片布局）

**Files:**
- Modify: `index.html` — 替换 `<style>` 块中的旧样式为新样式

**Interfaces:**
- Consumes: 新卡片结构（card-highlights, card-actions, group-summary）
- Produces: 完整的视觉效果

**步骤：**

- [ ] **Step 1: 替换 CSS**

将现有的 `<style>` 块整体替换为以下新样式（保留 `:root` 变量不变）：

```css
/* ===== Particle Canvas ===== */
#particle-bg {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  z-index: -1; pointer-events: none;
}

/* ===== Hero ===== */
.hero { text-align: center; padding: 80px 20px 40px; margin-bottom: 32px; position: relative; }
.hero::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(6,182,212,0.12) 0%, rgba(139,92,246,0.06) 40%, transparent 70%);
  pointer-events: none;
}
.hero h1 {
  font-size: clamp(28px, 5vw, 40px); font-weight: 700;
  background: linear-gradient(90deg, var(--cyan), var(--purple));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 12px;
}
.hero p { color: var(--text2); font-size: 16px; }
.hero .stats-bar {
  display: inline-flex; gap: 24px; margin-top: 20px; padding: 10px 24px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  font-size: 13px; color: var(--text2);
}
.hero .stats-bar strong { color: var(--cyan); font-weight: 600; }

/* ===== Group Sections (collapsible) ===== */
.group-section { margin-bottom: 40px; }
.group-summary {
  font-size: 16px; font-weight: 700; color: var(--text);
  padding: 12px 14px; margin-bottom: 16px;
  border-left: 3px solid var(--cyan);
  cursor: pointer; list-style: none;
  display: flex; align-items: center; gap: 8px;
}
.group-summary::-webkit-details-marker { display: none; }
.group-summary::after { content: '\f078'; font-family: 'Font Awesome 6 Free'; font-weight: 900; margin-left: auto; font-size: 12px; transition: transform 0.3s; }
details[open] > .group-summary::after { transform: rotate(-180deg); }
.group-summary small { font-size: 12px; color: var(--text2); font-weight: 400; margin-left: 4px; }

/* ===== Grid ===== */
.books-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px; margin-bottom: 0;
}

/* ===== Card (3D ready) ===== */
.book-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px;
  color: var(--text); display: flex; flex-direction: column; gap: 12px;
  position: relative; overflow: hidden;
  transition: transform 0.4s ease-out, box-shadow 0.4s ease-out, border-color 0.3s;
  transform-style: preserve-3d;
}
.book-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.book-card.cyan::before      { background: var(--cyan); box-shadow: var(--glow-cyan); }
.book-card.purple::before    { background: var(--purple); box-shadow: var(--glow-purple); }
.book-card.red::before       { background: var(--red); box-shadow: var(--glow-red); }
.book-card.green::before     { background: var(--green); box-shadow: var(--glow-green); }
.book-card.orange::before    { background: var(--orange); box-shadow: var(--glow-orange); }
.book-card.pink::before      { background: var(--pink); box-shadow: var(--glow-pink); }
.book-card.gold::before      { background: var(--gold); box-shadow: var(--glow-gold); }

.book-card:hover {
  border-color: var(--cyan);
  box-shadow: 0 12px 40px rgba(6,182,212,0.15);
}
.book-card.cyan:hover      { border-color: var(--cyan); box-shadow: 0 12px 40px rgba(6,182,212,0.2); }
.book-card.purple:hover    { border-color: var(--purple); box-shadow: 0 12px 40px rgba(139,92,246,0.2); }
.book-card.red:hover       { border-color: var(--red); box-shadow: 0 12px 40px rgba(239,68,68,0.2); }
.book-card.green:hover     { border-color: var(--green); box-shadow: 0 12px 40px rgba(16,185,129,0.2); }
.book-card.orange:hover    { border-color: var(--orange); box-shadow: 0 12px 40px rgba(245,158,11,0.2); }
.book-card.pink:hover      { border-color: var(--pink); box-shadow: 0 12px 40px rgba(236,72,153,0.2); }
.book-card.gold:hover      { border-color: var(--gold); box-shadow: 0 12px 40px rgba(234,179,8,0.2); }

.book-card .card-header { display: flex; align-items: center; gap: 14px; }
.book-card .card-icon {
  font-size: 30px; width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 12px; flex-shrink: 0;
}
.book-card.cyan .card-icon      { background: rgba(6,182,212,0.12); }
.book-card.purple .card-icon    { background: rgba(139,92,246,0.12); }
.book-card.red .card-icon       { background: rgba(239,68,68,0.12); }
.book-card.green .card-icon     { background: rgba(16,185,129,0.12); }
.book-card.orange .card-icon    { background: rgba(245,158,11,0.12); }
.book-card.pink .card-icon      { background: rgba(236,72,153,0.12); }
.book-card.gold .card-icon      { background: rgba(234,179,8,0.12); }

.book-card .card-title {
  font-size: 15px; font-weight: 600; line-height: 1.4; color: var(--text); flex: 1;
}
.book-card .card-desc { font-size: 13px; color: var(--text2); line-height: 1.6; }
.book-card .card-meta { display: flex; align-items: center; gap: 12px; font-size: 12px; color: var(--text2); }
.book-card .card-meta .page-count { padding: 2px 8px; border-radius: 4px; background: var(--surface2); font-weight: 500; }

.book-card .card-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.book-card .card-tag {
  display: inline-block; padding: 3px 10px; border-radius: 4px;
  font-size: 11px; font-weight: 500;
}
.book-card.cyan .card-tag       { background: rgba(6,182,212,0.12); color: var(--cyan); }
.book-card.purple .card-tag     { background: rgba(139,92,246,0.12); color: var(--purple); }
.book-card.red .card-tag        { background: rgba(239,68,68,0.12); color: var(--red); }
.book-card.green .card-tag      { background: rgba(16,185,129,0.12); color: var(--green); }
.book-card.orange .card-tag     { background: rgba(245,158,11,0.12); color: var(--orange); }
.book-card.pink .card-tag       { background: rgba(236,72,153,0.12); color: var(--pink); }
.book-card.gold .card-tag       { background: rgba(234,179,8,0.12); color: var(--gold); }

/* Highlights row */
.book-card .card-highlights {
  display: flex; gap: 12px; flex-wrap: wrap; padding-top: 4px;
  border-top: 1px solid var(--border);
}
.book-card .highlight-item { text-align: center; flex: 1; min-width: 60px; }
.book-card .highlight-value { display: block; font-size: 16px; font-weight: 700; }
.book-card .highlight-label { font-size: 10px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.05em; }

/* Action buttons */
.book-card .card-actions {
  display: flex; gap: 8px; margin-top: 4px;
}
.book-card .card-actions .btn {
  flex: 1; text-align: center; padding: 8px 12px; border-radius: 6px;
  font-size: 12px; font-weight: 600; text-decoration: none;
  transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 6px;
}
.book-card .card-actions .btn-book {
  background: rgba(6,182,212,0.1); color: var(--cyan); border: 1px solid rgba(6,182,212,0.3);
}
.book-card .card-actions .btn-book:hover { background: rgba(6,182,212,0.2); border-color: var(--cyan); }
.book-card .card-actions .btn-kanban {
  background: rgba(139,92,246,0.1); color: var(--purple); border: 1px solid rgba(139,92,246,0.3);
}
.book-card .card-actions .btn-kanban:hover { background: rgba(139,92,246,0.2); border-color: var(--purple); }

/* ===== Footer ===== */
footer {
  text-align: center; padding: 40px 20px; margin-top: 40px;
  border-top: 1px solid var(--border); color: var(--text2); font-size: 12px;
}
footer a { color: var(--cyan); text-decoration: none; }

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .books-grid { grid-template-columns: 1fr; }
  .hero h1 { font-size: 26px; }
  .hero .stats-bar { flex-wrap: wrap; gap: 12px; }
  .hero { padding: 50px 20px 30px; }
}
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "style: update all CSS for 3D cards, particle bg, collapsible groups, and new card layout"
```

### Task 7: 最终验证与清理

**Files:**
- Modify: `index.html`

**步骤：**

- [ ] **Step 1: 完整性检查清单**
  - 11 本书全部出现在正确分类下
  - 每本书有「进入书籍」和「查看看板」两个按钮
  - 所有链接可点击且跳转正确
  - 粒子背景正常渲染
  - 3D 倾斜在 hover 时生效
  - 分类可折叠/展开
  - 搜索框可按书名/标签过滤
  - 移动端响应式正常（grid 单列）

- [ ] **Step 2: 本地预览验证**

```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports && python3 -m http.server 8080 &
# Open http://localhost:8080 in browser
# Verify all features work
```

- [ ] **Step 3: 提交最终版本并推送**

```bash
git add index.html
git commit -m "feat: complete homepage redesign — 3D cards, particle bg, kanban-book merge, collapsible groups"
git push origin main
```

---

## Self-Review Checklist

1. **Spec coverage:** 
   - 粒子背景 → Task 3 ✅
   - 3D 卡片 → Task 4 ✅
   - 分类折叠 → Task 1 (GROUPS) + Task 2 (render) ✅
   - 双按钮卡片 → Task 2 (card-actions) ✅
   - 搜索过滤 → Task 5 ✅
   - 高亮数据 → Task 2 (card-highlights) ✅
   - 不引入第三方库 → 全部原生实现 ✅
   - 只改 index.html → 所有任务仅修改 index.html ✅

2. **Placeholder scan:** 无 TBD/TODO，所有代码完整 ✅

3. **Type consistency:** BOOK_DATA 字段在所有任务中一致使用 ✅

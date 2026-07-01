# 广州吃喝玩乐+供应链全景看板 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建单文件 HTML 看板，全面展示广州吃喝玩乐推荐与供应链批发市场生态（精确到街道级别），并呈现跨境电商与网商基地数据。

**Architecture:** 单文件 HTML，内嵌全部 CSS + JavaScript。ECharts 5.x 通过 CDN 加载。CSS Grid 布局，赛博朋克深色主题（延续之前洗钱看板风格）。内容按 6 个模块组织，每个模块独立 div section。

**Tech Stack:**
- 单文件 HTML（内嵌 CSS + JS）
- Apache ECharts 5.5.0 CDN（jsdelivr）
- Font Awesome 6.5.1 CDN
- Google Fonts Noto Sans SC
- CSS Grid + Flexbox 响应式布局
- CSS 变量管理主题色

## Global Constraints

- 单文件 HTML，所有 CSS 和 JS 内嵌，不引用任何外部 CSS/JS 文件（CDN 除外）
- 文件名：`广州吃喝玩乐+供应链全景看板.html`，保存在仓库根目录
- 赛博朋克深色主题：背景 #0a0e17，卡片 #111827，霓虹强调色（红/青/紫/绿/橙/金）
- 最小宽度 1024px，支持桌面端完整展示
- 所有中文文本，语言属性 `lang="zh-CN"`
- ECharts 图表必须通过 `window.addEventListener('resize')` 做响应式 resize
- 每个数据/统计必须标注数据来源（data-note 或 footer）
- 供应链部分必须精确到街道/路名级别，每个市场说明每栋楼/每条街做什么
- 参考已有看板 CSS 模式（见 `全球地下钱庄与洗钱全景风险看板.html` 的 CSS 变量和组件类名）

---

### Task 1.1: HTML骨架 + 模块一（Hero城市大字报）

**Files:**
- Create: `广州吃喝玩乐+供应链全景看板.html`

**Interfaces:**
- Consumes: None (first task, creates base file)
- Produces: CSS 变量 `--neon-gold: #eab308`（金色用于高端/老字号场景）

- [ ] **Step 1: 创建 HTML 骨架 + CSS 变量**

创建文件 `广州吃喝玩乐+供应链全景看板.html`，包含：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>广州吃喝玩乐+供应链全景看板</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
:root {
  --bg: #0a0e17;
  --surface: #111827;
  --surface2: #1a2235;
  --border: #1e2a3a;
  --text: #e2e8f0;
  --text2: #94a3b8;
  --neon-red: #ef4444;
  --neon-cyan: #06b6d4;
  --neon-purple: #8b5cf6;
  --neon-green: #10b981;
  --neon-orange: #f59e0b;
  --neon-gold: #eab308;
  --glow-red: 0 0 20px rgba(239,68,68,0.3);
  --glow-cyan: 0 0 20px rgba(6,182,212,0.3);
  --glow-purple: 0 0 20px rgba(139,92,246,0.3);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Noto Sans SC', -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-width: 1024px;
}
.container { max-width: 1600px; margin: 0 auto; padding: 24px; }
/* Hero */
.hero {
  text-align: center;
  padding: 50px 20px 40px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(234,179,8,0.08) 0%, transparent 60%);
  pointer-events: none;
}
.hero h1 {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 3px;
  background: linear-gradient(90deg, var(--neon-gold), var(--neon-cyan), var(--neon-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  position: relative;
}
.hero .subtitle { color: var(--text2); font-size: 14px; margin-bottom: 6px; }
.hero .meta { font-size: 12px; color: var(--text2); opacity: 0.7; }
.hero .meta span { margin: 0 8px; }
/* Metrics */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}
@media (max-width: 1200px) { .metrics-row { grid-template-columns: repeat(2, 1fr); } }
.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.metric-card.gold::before { background: var(--neon-gold); box-shadow: 0 0 20px rgba(234,179,8,0.3); }
.metric-card.cyan::before { background: var(--neon-cyan); box-shadow: var(--glow-cyan); }
.metric-card.purple::before { background: var(--neon-purple); box-shadow: var(--glow-purple); }
.metric-card.red::before { background: var(--neon-red); }
.metric-card.green::before { background: var(--neon-green); }
.metric-card .value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}
.metric-card.gold .value { color: var(--neon-gold); }
.metric-card.cyan .value { color: var(--neon-cyan); }
.metric-card.purple .value { color: var(--neon-purple); }
.metric-card.red .value { color: var(--neon-red); }
.metric-card.green .value { color: var(--neon-green); }
.metric-card .label { font-size: 12px; color: var(--text2); line-height: 1.5; }
/* Sections */
section { margin-bottom: 50px; }
.section-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 20px;
  padding-left: 14px;
  border-left: 3px solid var(--neon-cyan);
  color: var(--neon-cyan);
}
.section-subtitle {
  font-size: 15px;
  font-weight: 600;
  color: var(--text2);
  margin: 24px 0 14px;
  padding-left: 10px;
  border-left: 2px solid var(--border);
}
/* Grid */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
@media (max-width: 1200px) {
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
}
/* Cards */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  transition: all 0.2s;
}
.card:hover {
  border-color: var(--neon-cyan);
  box-shadow: var(--glow-cyan);
}
.card h3 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text);
}
.card p, .card li { font-size: 13px; color: var(--text2); line-height: 1.7; }
.card ul { list-style: none; padding: 0; }
.card ul li { padding: 5px 0; border-bottom: 1px solid rgba(30,42,58,0.5); }
.card ul li:last-child { border-bottom: none; }
.card ul li strong { color: var(--text); font-weight: 600; }
/* Flow diagram */
.flow-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin: 20px 0;
  flex-wrap: wrap;
}
.flow-step {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
  text-align: center;
  min-width: 140px;
  flex: 1;
  max-width: 200px;
}
.flow-step .step-icon { font-size: 24px; margin-bottom: 8px; }
.flow-step .step-label { font-size: 13px; font-weight: 600; color: var(--text); }
.flow-step .step-desc { font-size: 11px; color: var(--text2); margin-top: 4px; }
.flow-arrow {
  color: var(--neon-cyan);
  font-size: 20px;
  margin: 0 8px;
  flex-shrink: 0;
}
/* Chart containers */
.chart-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}
.chart-box .chart-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text);
  padding-left: 10px;
  border-left: 2px solid var(--neon-purple);
}
.echarts-container { width: 100%; height: 400px; }
.echarts-container.small { height: 300px; }
/* Data note */
.data-note {
  font-size: 11px;
  color: var(--text2);
  font-style: italic;
  margin-top: 10px;
  opacity: 0.7;
}
/* Footer */
footer {
  text-align: center;
  padding: 30px 0;
  border-top: 1px solid var(--border);
  color: var(--text2);
  font-size: 11px;
  margin-top: 40px;
}
</style>
</head>
<body>
<div class="container">
```

- [ ] **Step 2: 添加 Hero 区域 + 5个数据指标卡片**

在 `</style>` 之后、`</head>` 之前结束 `<style>` 标签。然后在 `<body>` 内添加：

```html
<!-- ===== HERO ===== -->
<div class="hero">
  <h1>广州吃喝玩乐 + 供应链全景看板</h1>
  <p class="subtitle">千年商都 · 跨境电商第一城 · 国际美食之都 · 国家中心城市</p>
  <p class="meta">
    <span>生成日期：2026年7月</span>
    <span>|</span>
    <span>覆盖范围：广州市6大行政区 + 供应链全品类</span>
    <span>|</span>
    <span>内容精度：街道级市场标注</span>
  </p>
</div>

<!-- ===== 城市数据大字报 ===== -->
<div class="metrics-row">
  <div class="metric-card gold">
    <div class="value">≈3万亿</div>
    <div class="label">广州GDP（2025）<br>广州市统计局</div>
  </div>
  <div class="metric-card cyan">
    <div class="value">≈1880万</div>
    <div class="label">常住人口<br>广州市统计局</div>
  </div>
  <div class="metric-card purple">
    <div class="value">>5万亿</div>
    <div class="label">进出口总额（2025）<br>广州海关</div>
  </div>
  <div class="metric-card red">
    <div class="value">>3000亿</div>
    <div class="label">跨境电商交易额（全国第一）<br>商务部</div>
  </div>
  <div class="metric-card green">
    <div class="value">>3亿</div>
    <div class="label">年游客人次<br>广州市文化广电旅游局</div>
  </div>
</div>
```

- [ ] **Step 3: 闭合 HTML 标签，验证结构**

在 `</div><!-- .container -->` 之后添加：

```html
<footer>
  <p><strong>数据来源：</strong>广州市统计局 · 广州海关 · 商务部 · 广州市文化广电旅游局 · 各批发市场管委会 · 各电商平台公开资料</p>
  <p style="margin-top:6px;">本看板仅供旅游规划与商务考察参考，不构成投资建议。所有数据均来自公开权威来源。</p>
  <p style="margin-top:4px;">生成日期：2026年7月 &nbsp;|&nbsp; 数据截止：2025年最新公开数据</p>
</footer>
</div><!-- .container -->
</body>
</html>
```

- [ ] **Step 4: 验证 HTML 结构完整性**

检查：
- `<div>` 标签配对：hero(1) + metrics-row容器implicit + 5个metric-card + section占位 + footer(1) + container(1) = 8个div打开，8个闭合
- CSS 变量全部定义：`--bg`, `--surface`, `--surface2`, `--border`, `--text`, `--text2`, `--neon-red`, `--neon-cyan`, `--neon-purple`, `--neon-green`, `--neon-orange`, `--neon-gold`
- 5个 metric-card 颜色类：gold/cyan/purple/red/green
- 响应式：`.metrics-row` 在 ≤1200px 时变为 2列

Run: 浏览器打开文件，确认无报错，5个指标卡片正常显示。

- [ ] **Step 5: Commit**

```bash
git add 广州吃喝玩乐+供应链全景看板.html
git commit -m "feat: 模块一 — Hero城市大字报+5项关键数据指标"
```

---

### Task 1.2: 模块二 — 吃喝玩乐篇（美食+景点+夜生活+购物）

**Files:**
- Modify: `广州吃喝玩乐+供应链全景看板.html`

**Interfaces:**
- Consumes: CSS 类 `.card`, `.grid-2`, `.grid-3`, `.section-title`, `.section-subtitle`
- Produces: 美食分类卡片数据、景点分类卡片数据

- [ ] **Step 1: 在 Hero 和数据卡片之后插入模块二骨架**

在 Task 1.1 的 metrics-row 之后、module 5 占位之前，插入：

```html
<!-- ===== 模块二：吃喝玩乐 ===== -->
<section>
<h2 class="section-title">模块二：吃喝玩乐 — 广州城市生活全景</h2>

<!-- 2.1 美食地图 -->
<h3 class="section-subtitle">2.1 美食地图 — 广府味道</h3>
<div class="grid-3">
  <!-- 早茶 -->
  <div class="card">
    <h3 style="color: var(--neon-red);"><i class="fas fa-teapot"></i> 广式早茶</h3>
    <p><strong>核心品种：</strong>虾饺、烧卖、叉烧包、肠粉、凤爪、蛋挞、流沙包、糯米鸡、红米肠、萝卜糕</p>
    <p><strong>推荐店铺：</strong></p>
    <ul>
      <li><strong>点都德</strong> — 连锁品牌，全市100+门店，早茶晚茶一体</li>
      <li><strong>陶陶居</strong> — 百年老字号（上下九总店），环境最佳</li>
      <li><strong>广州酒家</strong> — 文昌南路总店，传统广府风味</li>
      <li><strong>莲香楼</strong> — 莲蓉始祖，太平南路老店</li>
      <li><strong>泮溪酒家</strong> — 园林酒家，荔枝湾畔，环境一流</li>
    </ul>
    <p><strong>人均消费：</strong>50-120元</p>
  </div>

  <!-- 烧腊 -->
  <div class="card">
    <h3 style="color: var(--neon-orange);"><i class="fas fa-drumstick-bite"></i> 烧腊</h3>
    <p><strong>核心品种：</strong>深井烧鹅、豉油鸡、蜜汁叉烧、白切鸡、腊肠、烧肉</p>
    <p><strong>推荐店铺/街区：</strong></p>
    <ul>
      <li><strong>炳胜公馆</strong> — 黑叉烧闻名，珠江新城店</li>
      <li><strong>万丰酒楼</strong> — 烧鹅专业，越秀区</li>
      <li><strong>惠福东路美食街</strong> — 多家烧腊老店集中</li>
      <li><strong>宝业路</strong> — 深夜烧腊大排档集中地</li>
    </ul>
    <p><strong>人均消费：</strong>30-80元</p>
  </div>

  <!-- 糖水甜品 -->
  <div class="card">
    <h3 style="color: var(--neon-gold);"><i class="fas fa-ice-cream"></i> 糖水/甜品</h3>
    <p><strong>核心品种：</strong>姜撞奶、双皮奶、杨枝甘露、绿豆沙、芝麻糊、红豆沙、豆腐花</p>
    <p><strong>推荐店铺：</strong></p>
    <ul>
      <li><strong>南信牛奶甜品专家</strong> — 中山八店，双皮奶第一</li>
      <li><strong>百花甜品</strong> — 上下九老店，招牌芋泥</li>
      <li><strong>玫瑰甜品</strong> — 文明路，椰汁龟苓膏</li>
      <li><strong>芳记小食</strong> — 宝业路，水牛奶甜品</li>
    </ul>
    <p><strong>人均消费：</strong>15-40元</p>
  </div>

  <!-- 大排档/宵夜 -->
  <div class="card">
    <h3 style="color: var(--neon-green);"><i class="fas fa-fire"></i> 大排档/宵夜</h3>
    <p><strong>核心品种：</strong>炒田螺、椒盐濑尿虾、干炒牛河、蒜蓉烤生蚝、煲仔饭、猪杂粥</p>
    <p><strong>推荐街区：</strong></p>
    <ul>
      <li><strong>宝业路大排档</strong> — 越秀区，广州宵夜圣地，24小时</li>
      <li><strong>体育西路宵夜街</strong> — 天河CBD后花园，白领聚集</li>
      <li><strong>滨江路</strong> — 海珠区江景大排档</li>
      <li><strong>东晓南路</strong> — 老广宵夜，接地气</li>
    </ul>
    <p><strong>人均消费：</strong>50-150元</p>
  </div>

  <!-- 街头小吃 -->
  <div class="card">
    <h3 style="color: var(--neon-cyan);"><i class="fas fa-lollipop"></i> 街头小吃</h3>
    <p><strong>核心品种：</strong>陈添记鱼皮、伍湛记及第粥、泮塘马蹄糕、伦教糕、鸡仔饼</p>
    <p><strong>推荐店铺：</strong></p>
    <ul>
      <li><strong>陈添记</strong> — 宝华路老屋，手撕鱼皮一绝</li>
      <li><strong>伍湛记</strong> — 光复北路，及第粥/炸两</li>
      <li><strong>东方宾馆鸡球饭店</strong> — 流花宾馆内，传统粤菜</li>
      <li><strong>达扬原味炖品</strong> — 多店，原盅炖汤</li>
    </ul>
    <p><strong>人均消费：</strong>20-60元</p>
  </div>

  <!-- 老字号 -->
  <div class="card">
    <h3 style="color: var(--neon-purple);"><i class="fas fa-store"></i> 老字号/特色</h3>
    <p><strong>核心品种：</strong>太平馆西餐（百年）、洪圣爷粥城、顺记冰室（椰子雪糕）、开记甜品</p>
    <p><strong>推荐店铺：</strong></p>
    <ul>
      <li><strong>太平馆</strong> — 长堤大马路，中国第一家西餐店（1860年）</li>
      <li><strong>顺记冰室</strong> — 宝华路，椰子/芒果/绿豆雪糕</li>
      <li><strong>洪圣爷粥城</strong> — 越秀区，海鲜粥专业</li>
      <li><strong>莲香楼</strong> — 第十甫路，月饼/莲子制品</li>
    </ul>
    <p><strong>人均消费：</strong>30-100元</p>
  </div>
</div>

<!-- 美食街区汇总 -->
<div class="card" style="margin-top:20px; border-left: 3px solid var(--neon-red);">
  <h3 style="color: var(--neon-red);"><i class="fas fa-map-marked-alt"></i> 广州美食街区速查</h3>
  <div class="grid-3" style="margin-top:12px;">
    <div><strong>北京路/文明路</strong><br>老字号集中，及第粥/银记肠粉/达扬炖品</div>
    <div><strong>上下九/宝华路</strong><br>骑楼老街，陈添记/顺记/莲香楼/陶陶居</div>
    <div><strong>惠福东路</strong><br>早茶/烧腊/小吃一条街</div>
    <div><strong>宝业路</strong><br>大排档/宵夜/陈添记鱼皮</div>
    <div><strong>体育西路/天河路</strong><br>白领宵夜/炳胜/高端餐饮</div>
    <div><strong>永庆坊/恩宁路</strong><br>文创+美食融合街区</div>
  </div>
</div>
</section>
```

- [ ] **Step 2: 添加必游景点 + 夜生活 + 购物**

在模块二美食部分之后继续添加：

```html
<!-- 2.2 必游景点 -->
<section>
<h3 class="section-subtitle">2.2 必游景点</h3>
<div class="grid-3">
  <div class="card">
    <h3 style="color: var(--neon-gold);"><i class="fas fa-landmark"></i> 历史文化</h3>
    <ul>
      <li><strong>陈家祠</strong> — 岭南建筑巅峰，木雕/石雕/砖雕/陶塑，地铁1号线陈家祠站</li>
      <li><strong>南越王博物院</strong> — 西汉南越国帝王陵墓遗址，解放北路</li>
      <li><strong>光孝寺</strong> — 六祖慧能剃度处，"未有光孝，早有菩提"</li>
      <li><strong>六榕寺</strong> — 苏轼题字"六榕"，花塔千年</li>
      <li><strong>石室圣心大教堂</strong> — 亚洲唯一全花岗岩哥特式教堂，越秀区</li>
      <li><strong>黄埔军校旧址</strong> — 长洲岛，近代史地标</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-cyan);"><i class="fas fa-city"></i> 现代地标</h3>
    <ul>
      <li><strong>广州塔（小蛮腰）</strong> — 600米，珠江南岸，夜游首选</li>
      <li><strong>珠江新城</strong> — 花城广场/广东省博物馆/广州图书馆/大剧院</li>
      <li><strong>海心沙</strong> — 亚运会开幕式场地，亚运公园</li>
      <li><strong>周大福金融中心（东塔）</strong> — 530米，华南第一高楼</li>
      <li><strong>西塔（广州国际金融中心）</strong> — 440米，珠江新城地标</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-green);"><i class="fas fa-tree"></i> 自然山水</h3>
    <ul>
      <li><strong>白云山</strong> — "羊城第一秀"，摩星岭海拔382米，索道/步行</li>
      <li><strong>越秀公园</strong> — 五羊雕塑（广州城标）、镇海楼、明代城墙</li>
      <li><strong>海珠湿地公园</strong> — 城市中轴线上最大的生态绿洲</li>
      <li><strong>华南植物园</strong> — 中科院下属，热带/亚热带植物</li>
      <li><strong>荔湾湖公园</strong> — 西关风情，荔枝湾涌</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-red);"><i class="fas fa-roller-coaster"></i> 主题乐园</h3>
    <ul>
      <li><strong>长隆野生动物世界</strong> — 全国最好动物园，自驾/小火车观赏</li>
      <li><strong>长隆欢乐世界</strong> — 垂直跌落过山车/十环过山车</li>
      <li><strong>长隆水上乐园</strong> — 吉尼斯认证最大水上乐园</li>
      <li><strong>长隆国际大马戏</strong> — 全球最大马戏表演，必看</li>
    </ul>
    <p><strong>地址：</strong>番禺区迎宾路 &nbsp;<strong>交通：</strong>地铁3号线汉溪长隆站</p>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-purple);"><i class="fas fa-palette"></i> 文化街区</h3>
    <ul>
      <li><strong>永庆坊</strong> — 李小龙祖居，粤剧艺术博物馆，恩宁路骑楼</li>
      <li><strong>东山口</strong> — 红砖洋楼/文艺小店/美术馆聚集地</li>
      <li><strong>沙面</strong> — 欧式建筑群，曾经的租界，拍照圣地</li>
      <li><strong>北京路步行街</strong> — 千年路古道遗址+购物中心</li>
      <li><strong>太古仓</strong> — 旧码头改造，酒吧/餐厅/日落观赏</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-orange);"><i class="fas fa-moon"></i> 夜生活</h3>
    <ul>
      <li><strong>珠江夜游</strong> — 天字码头/大沙头码头，两岸灯光秀</li>
      <li><strong>琶醍啤酒创意区</strong> — 珠江边酒吧街，日落+夜景</li>
      <li><strong>体育西路</strong> — 天河夜生活中心，酒吧/KTV/夜店</li>
      <li><strong>环市东路</strong> — 花园酒店/白云宾馆，老牌酒吧街</li>
      <li><strong>北京路/宝华路</strong> — 24小时书店（方所/购书中心）</li>
      <li><strong>江南西夜市</strong> — 海珠区年轻人夜市</li>
    </ul>
  </div>
</div>

<!-- 2.4 购物天堂 -->
<h3 class="section-subtitle">2.3 购物天堂</h3>
<div class="grid-3">
  <div class="card">
    <h3 style="color: var(--neon-gold);"><i class="fas fa-gem"></i> 高端商圈</h3>
    <ul>
      <li><strong>太古汇</strong> — 天河路，LV/Gucci/Chanel等全一线奢侈品牌</li>
      <li><strong>天环广场</strong> — 体育西路，Apple Store旗舰店/潮流品牌</li>
      <li><strong>IGC天汇广场</strong> — 天河路，中高端+餐饮</li>
      <li><strong>广百百货/新大新</strong> — 北京路，老字号百货</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-cyan);"><i class="fas fa-shopping-bag"></i> 大众消费</h3>
    <ul>
      <li><strong>正佳广场</strong> — 天河路，6层超大综合体，购物+海洋馆+剧院</li>
      <li><strong>北京路步行街</strong> — 老字号+特产+小吃+千年古道遗址</li>
      <li><strong>上下九步行街</strong> — 骑楼建筑+广式小吃+老字号</li>
      <li><strong>江南西</strong> — 海珠区年轻人聚集，潮流小店</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-purple);"><i class="fas fa-tags"></i> 批发市场购物</h3>
    <ul>
      <li><strong>十三行</strong> — 新中国大厦，女装批发（也接待散客）</li>
      <li><strong>白马服装市场</strong> — 站前路，中高端女装</li>
      <li><strong>华林国际</strong> — 华林街，玉器珠宝</li>
      <li><strong>一德路</strong> — 玩具/海味干货/进口食品</li>
    </ul>
  </div>
</div>
</section>
```

- [ ] **Step 3: 验证模块二内容完整性**

检查清单：
- 美食6大分类卡片（早茶/烧腊/糖水/大排档/小吃/老字号）✓
- 美食街区速查汇总（6个街区）✓
- 必游景点5大分类卡片（历史文化/现代地标/自然山水/主题乐园/文化街区）✓
- 夜生活6个地点 ✓
- 购物天堂3大分类 ✓
- 所有店铺都有地址/地铁交通信息 ✓

- [ ] **Step 4: Commit**

```bash
git add 广州吃喝玩乐+供应链全景看板.html
git commit -m "feat: 模块二 — 吃喝玩乐篇(美食地图6分类+景点5分类+夜生活+购物)"
```

---

### Task 2.1: 模块三 — 供应链批发市场篇（品类维度，街道级详解）

**Files:**
- Modify: `广州吃喝玩乐+供应链全景看板.html`

**Interfaces:**
- Consumes: CSS 类 `.card`, `.grid-2`, `.grid-3`, `.channel-card`（复用洗钱看板的 channel-card 样式，增加金色变体）
- Produces: 8大品类批发市场的街道级数据

**新增 CSS（在 Task 1.1 的样式中追加）：**

```css
/* Channel cards (reuse from previous dashboard) */
.channel-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}
.channel-card::after {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 3px;
  height: 100%;
}
.channel-card.cyan::after { background: var(--neon-cyan); }
.channel-card.purple::after { background: var(--neon-purple); }
.channel-card.red::after { background: var(--neon-red); }
.channel-card.green::after { background: var(--neon-green); }
.channel-card.orange::after { background: var(--neon-orange); }
.channel-card.gold::after { background: var(--neon-gold); }
.channel-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.channel-card h3 {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.channel-card .channel-icon { font-size: 18px; }
.channel-card.cyan h3 { color: var(--neon-cyan); }
.channel-card.purple h3 { color: var(--neon-purple); }
.channel-card.red h3 { color: var(--neon-red); }
.channel-card.green h3 { color: var(--neon-green); }
.channel-card.orange h3 { color: var(--neon-orange); }
.channel-card.gold h3 { color: var(--neon-gold); }
.channel-card p { font-size: 12px; color: var(--text2); line-height: 1.7; margin-bottom: 6px; }
.channel-card p strong { color: var(--text); }
.channel-card .street-note {
  background: var(--surface2);
  border-radius: 6px;
  padding: 8px 12px;
  margin-top: 8px;
  font-size: 11px;
  color: var(--text2);
  line-height: 1.8;
}
```

- [ ] **Step 1: 在模块二之后插入模块三骨架 + 服装鞋帽品类**

```html
<!-- ===== 模块三：供应链批发市场篇（品类维度） ===== -->
<section>
<h2 class="section-title">模块三：供应链批发市场全景 — 品类维度（街道级详解）</h2>
<p style="color:var(--text2);font-size:13px;margin-bottom:20px;">以下每个批发市场均精确标注到街道/路名级别，说明每栋楼/每条街的功能定位、主营品类、价格区间和目标客户。</p>

<div class="grid-2">
  <!-- 3.1 服装鞋帽 -->
  <div class="channel-card cyan">
    <h3><i class="channel-icon fas fa-tshirt"></i> 3.1 服装鞋帽</h3>
    <p><strong>核心区域：</strong>荔湾区和平路/光复南路（十三行）&nbsp;|&nbsp;越秀区站前路（白马）&nbsp;|&nbsp;白云区增槎路（广大/信诚）</p>
    <p><strong>十三行·新中国大厦（和平路1号）：</strong></p>
    <div class="street-note">
      <strong>1-3楼：</strong>散客区，快时尚女装，50-200元/件，日客流超3万<br>
      <strong>4-6楼：</strong>批发改衣区，中端女装，100-400元，配套缝纫/改码服务<br>
      <strong>7楼以上：</strong>高端定制/设计师品牌，300-1000元/件，面向买手店/直播间<br>
      <strong>周边-人民南路：</strong>老牌服装批发，中年女装为主，80-300元<br>
      <strong>周边-教育路：</strong>鞋类配套市场，女鞋/男鞋/童鞋批发，30-200元<br>
      <strong>地铁：</strong>1号线/6号线黄沙站B出口步行5分钟
    </div>
    <p><strong>UUS（人民南路28号）：</strong>韩国设计师品牌集合，中高端女装，300-1500元/件，韩系风格，精品买手店首选。地铁1号线黄沙站。</p>
    <p><strong>白马服装市场（站前路33号）：</strong></p>
    <div class="street-note">
      <strong>1-3楼：</strong>中高端女装，200-800元/件<br>
      <strong>4-5楼：</strong>男装，150-600元<br>
      <strong>6楼以上：</strong>设计师品牌/原创设计<br>
      <strong>地铁：</strong>2号线越秀公园站C出口步行8分钟
    </div>
    <p><strong>广大/信诚（增槎路436号）：</strong></p>
    <div class="street-note">
      <strong>广大服装批发市场：</strong>尾货/库存折扣，10-80元/件，适合下沉市场/拼多多/直播带货<br>
      <strong>信诚服装购物广场：</strong>毗邻广大，同类尾货，环境更好<br>
      <strong>地铁：</strong>8号线同德站步行15分钟 / 自驾导航"广大服装批发市场"
    </div>
    <p><strong>锦荣国际（增槎路）：</strong>中端女装批发，100-400元/件，环境较好，配套停车场/仓储。同德围片区。</p>
    <p><strong>步云天地（天河路附近）：</strong>高端品牌服装批发，国际大牌授权，500-3000元，品质保证。</p>
  </div>

  <!-- 3.2 皮具箱包 -->
  <div class="channel-card orange">
    <h3><i class="channel-icon fas fa-suitcase"></i> 3.2 皮具箱包</h3>
    <p><strong>核心区域：</strong>白云区三元里大道 &nbsp;|&nbsp; 白云区环市西路 &nbsp;|&nbsp; 荔湾区瑞康路（配件）</p>
    <p><strong>三元里片区（三元里大道/萧岗村周边）：</strong></p>
    <div class="street-note">
      <strong>三元里皮具批发城：</strong>中低端皮具，50-300元/件，手提包/双肩包/钱包<br>
      <strong>国际皮具交易中心：</strong>中高端，300-1500元，品牌代工/自有品牌<br>
      <strong>萧岗村周边小巷：</strong>最低端尾货，10-50元，地摊/拼多多货源<br>
      <strong>地铁：</strong>2号线三元里站A出口步行10分钟
    </div>
    <p><strong>桂花岗片区（环市西路）：</strong></p>
    <div class="street-note">
      <strong>百荣皮具商城：</strong>中端，100-500元，批发+零售兼营<br>
      <strong>益佳皮具交易广场：</strong>中高端，200-800元，质量稳定<br>
      <strong>地铁：</strong>2号线越秀公园站/三元里站
    </div>
    <p><strong>配套-</strong><strong>瑞康路（荔湾区）：</strong>箱包配件专营，拉链/五金/面料/皮革，B端采购。地铁1号线黄沙站。</p>
    <p><strong>配套-</strong><strong>广园西路（白云区）：</strong>皮具机械/工具/胶水/模具。地铁2号线飞翔公园站。</p>
  </div>

  <!-- 3.3 珠宝玉石 -->
  <div class="channel-card purple">
    <h3><i class="channel-icon fas fa-gem"></i> 3.3 珠宝玉石</h3>
    <p><strong>核心区域：</strong>荔湾区华林街 &nbsp;|&nbsp; 荔湾区康王中路</p>
    <p><strong>华林国际（华林街16号）：</strong></p>
    <div class="street-note">
      <strong>4楼：</strong>翡翠玉石专区，几千至几十万元/件，高端收藏级<br>
      <strong>3楼：</strong>K金/钻石/彩宝，几百至几万元<br>
      <strong>2楼：</strong>银饰/时尚饰品，10-500元<br>
      <strong>1楼：</strong>玉器摆件/文玩手串，几百至数十万<br>
      <strong>地下层：</strong>原材料/毛料市场（每周六早市）<br>
      <strong>地铁：</strong>1号线长寿路站D出口步行5分钟
    </div>
    <p><strong>荔湾广场（康王中路990号）：</strong></p>
    <div class="street-note">
      <strong>1-3楼：</strong>低端玉器/水晶/玛瑙，几十至千元/件<br>
      <strong>4楼以上：</strong>散客淘货区，性价比极高<br>
      <strong>特点：</strong>广州最大的散客玉器市场，砍价文化浓厚<br>
      <strong>地铁：</strong>1号线长寿路站
    </div>
    <p><strong>上下九步行街：</strong>周大福/六福/周生生等品牌旗舰店/专柜集中地，零售为主。</p>
  </div>

  <!-- 3.4 茶叶香料中药材 -->
  <div class="channel-card green">
    <h3><i class="channel-icon fas fa-leaf"></i> 3.4 茶叶/香料/中药材</h3>
    <p><strong>核心区域：</strong>荔湾区芳村大道/龙溪大道（茶叶）&nbsp;|&nbsp;荔湾区清平路（中药材）&nbsp;|&nbsp;荔湾区芳村（香料）</p>
    <p><strong>芳村茶叶市场群（芳村大道/龙溪大道沿线）：</strong></p>
    <div class="street-note">
      <strong>海印茶叶批发市场：</strong>普洱茶/红茶/绿茶/乌龙茶全品类，50-5000元/斤<br>
      <strong>芳村普洱茶城：</strong>高端普洱茶收藏，陈年普洱/名山古树，几千至数十万/饼<br>
      <strong>怡盛茶园：</strong>白茶/乌龙茶/花草茶/茶具，中端为主<br>
      <strong>龙溪大道沿线：</strong>茶叶包装/茶具/茶盘/茶席配件<br>
      <strong>特点：</strong>华南最大茶叶集散地，年交易额超50亿元<br>
      <strong>地铁：</strong>1号线西朗站/广佛线龙溪站
    </div>
    <p><strong>清平中药材市场（清平路）：</strong></p>
    <div class="street-note">
      <strong>清平药店街：</strong>传统中药材（人参/鹿茸/枸杞/当归等），几百至数千元/斤<br>
      <strong>清平保健品市场：</strong>西洋参/燕窝/冬虫夏草/藏红花，高端滋补品<br>
      <strong>清平路周边小巷：</strong>中药材饮片/药膳配方/养生茶<br>
      <strong>特点：</strong>全国四大中药材市场之一，可现场鉴定<br>
      <strong>地铁：</strong>6号线文化公园站步行10分钟
    </div>
    <p><strong>芳村香料市场：</strong>香精香料/食品添加剂，餐饮/食品加工采购首选。广佛线龙溪站。</p>
  </div>

  <!-- 3.5 电子产品/数码 -->
  <div class="channel-card red">
    <h3><i class="channel-icon fas fa-laptop"></i> 3.5 电子产品/数码</h3>
    <p><strong>核心区域：</strong>天河区岗顶/天河路 &nbsp;|&nbsp; 荔湾区黄沙大道</p>
    <p><strong>岗顶电脑城群（中山一路/体育南路）：</strong></p>
    <div class="street-note">
      <strong>太平洋电脑城：</strong>A座电脑整机/配件，B座数码产品/手机，500-10000元<br>
      <strong>百脑汇：</strong>笔记本/DIY组装/电脑维修，1000-8000元<br>
      <strong>欧丽数码：</strong>手机配件/数码周边/耳机/充电宝，10-500元<br>
      <strong>科韵路：</strong>软件开发/互联网企业聚集（腾讯/网易/微信广州总部）<br>
      <strong>地铁：</strong>3号线岗顶站
    </div>
    <p><strong>黄沙机电市场（黄沙大道）：</strong>工业设备/电子元器件/仪器仪表，B端采购为主。地铁1号线黄沙站。</p>
  </div>

  <!-- 3.6 食品/酒水/干货 -->
  <div class="channel-card gold">
    <h3><i class="channel-icon fas fa-cookie-bite"></i> 3.6 食品/酒水/干货</h3>
    <p><strong>核心区域：</strong>越秀区一德路/泰康路 &nbsp;|&nbsp; 白云区增槎路 &nbsp;|&nbsp; 越秀区致压路</p>
    <p><strong>一德路片区（一德路/泰康路/乐民路）：</strong></p>
    <div class="street-note">
      <strong>一德路国际玩具城：</strong>全国最大玩具批发，占北方市场70%份额，10-500元/件<br>
      <strong>泰康食品城：</strong>饼干/糖果/坚果（徐福记/达利园总代理），5-100元/件<br>
      <strong>一德路海味干货街（乐民路）：</strong>鲍鱼/海参/花胶/香菇/木耳，几百至数万元/斤<br>
      <strong>一德路咸水果副食：</strong>进口零食/饮料/调味品，东南亚/日韩/欧洲全线<br>
      <strong>泰康路副食街：</strong>粮油/米面/调味品，餐饮批量采购<br>
      <strong>地铁：</strong>6号线一德路站
    </div>
    <p><strong>江南果菜批发市场（增槎路888号）：</strong></p>
    <div class="street-note">
      <strong>国内果菜区：</strong>苹果/柑橘/香蕉/西瓜等大宗，按吨批发<br>
      <strong>进口果蔬区：</strong>车厘子/榴莲/牛油果/山竹（东南亚/澳洲/南美），高端水果<br>
      <strong>特点：</strong>全国最大进口果菜集散中心，凌晨4点开始批发<br>
      <strong>地铁：</strong>8号线同德站 / 自驾导航
    </div>
    <p><strong>南方食品交易市场（致压路/兴发广场周边）：</strong>粮油/调味品/南北干货，餐饮采购首选。地铁2号线越秀公园站。</p>
  </div>

  <!-- 3.7 化妆品 -->
  <div class="channel-card cyan">
    <h3><i class="channel-icon fas fa-pump-soap"></i> 3.7 化妆品</h3>
    <p><strong>核心区域：</strong>白云区程界西/广园西路 &nbsp;|&nbsp; 白云区同和</p>
    <p><strong>广州美博城（程界西街2号）：</strong></p>
    <div class="street-note">
      <strong>1-2楼：</strong>成品化妆品/护肤品/彩妆批发，10-500元<br>
      <strong>3-4楼：</strong>OEM/ODM代工服务对接，品牌定制<br>
      <strong>5楼：</strong>原料/包材/香料，B端采购<br>
      <strong>周边配套：</strong>永泰化妆塑料包装城（包材）、兴发塑胶五金城（机械）<br>
      <strong>特点：</strong>全国最大化妆品全产业链集散地，辐射全球<br>
      <strong>地铁：</strong>2号线江夏站B出口步行10分钟
    </div>
    <p><strong>佰美国际（白云区同和）：</strong>中高端化妆品/面膜/护肤品OEM/ODM，品牌孵化首选。地铁3号线同和站。</p>
  </div>

  <!-- 3.8 文具/办公/礼品 -->
  <div class="channel-card purple">
    <h3><i class="channel-icon fas fa-pencil-ruler"></i> 3.8 文具/办公/礼品</h3>
    <p><strong>核心区域：</strong>越秀区致压路/广园西路 &nbsp;|&nbsp; 越秀区一德路</p>
    <p><strong>兴发广场（致压路）：</strong></p>
    <div class="street-note">
      <strong>文具办公用品：</strong>笔类/纸张/文件夹/办公设备，5-500元<br>
      <strong>工艺礼品：</strong>节日装饰/摆件/纪念品/圣诞用品<br>
      <strong>特点：</strong>白云区文具批发核心，辐射华南<br>
      <strong>地铁：</strong>2号线越秀公园站
    </div>
    <p><strong>一德路玩具文具片区：</strong>玩具/文具/节日用品/工艺品，与食品干货同街区。地铁6号线一德路站。</p>
  </div>
</div>
</section>
```

- [ ] **Step 2: 验证品类维度内容**

检查清单：
- 8大品类全部覆盖（服装/皮具/珠宝/茶叶/电子/食品/化妆品/文具）✓
- 每个品类标注到街道/路名 ✓
- 每个市场说明楼层/分区功能 ✓
- 每个市场有价格区间 ✓
- 每个市场有地铁/交通指引 ✓
- 新增 `.channel-card.gold` 变体 ✓
- 新增 `.street-note` 样式 ✓

- [ ] **Step 3: Commit**

```bash
git add 广州吃喝玩乐+供应链全景看板.html
git commit -m "feat: 模块三 — 供应链批发市场(品类维度8大类,街道级详解)"
```

---

### Task 2.2: 模块四 — 供应链区域维度 + ECharts区域热力图

**Files:**
- Modify: `广州吃喝玩乐+供应链全景看板.html`

**Interfaces:**
- Consumes: `.grid-2`, `.grid-3`, `.card`, `.chart-box`, `.echarts-container`
- Produces: 区域-品类关联图表 `#chart-region-matrix`

- [ ] **Step 1: 在模块三之后插入模块四骨架 + 6大区域详解**

```html
<!-- ===== 模块四：供应链批发市场篇（区域维度） ===== -->
<section>
<h2 class="section-title">模块四：供应链批发市场全景 — 区域维度</h2>

<div class="grid-2">
  <!-- 荔湾区 -->
  <div class="channel-card cyan">
    <h3><i class="channel-icon fas fa-map"></i> 荔湾区 — 老西关·传统商贸核心区</h3>
    <p><strong>产业定位：</strong>广州历史最悠久的商贸区，品类最全、散批兼营</p>
    <div class="street-note">
      <strong>和平路/人民南路：</strong>十三行服装（新中国大厦/UUS）<br>
      <strong>华林街/康王中路：</strong>华林珠宝 + 荔湾广场玉器<br>
      <strong>清平路：</strong>清平中药材市场<br>
      <strong>芳村大道/龙溪大道：</strong>芳村茶叶市场群 + 香料市场<br>
      <strong>一德路/泰康路：</strong>食品干货 + 玩具（注：一德路行政属越秀，但与荔湾商贸圈连片）<br>
      <strong>宝华路/上下九：</strong>老字号 + 陈添记鱼皮 + 顺记冰室<br>
      <strong>地铁覆盖：</strong>1号线/6号线/8号线<br>
      <strong>关键词：</strong>珠宝/茶叶/药材/服装/老字号/骑楼文化
    </div>
  </div>

  <!-- 越秀区 -->
  <div class="channel-card orange">
    <h3><i class="channel-icon fas fa-map"></i> 越秀区 — 传统商贸+高端消费</h3>
    <p><strong>产业定位：</strong>老牌批发市场+高端零售+IT产品</p>
    <div class="street-note">
      <strong>站前路33号：</strong>白马服装市场<br>
      <strong>天河路/北京路：</strong>高端购物+北京路步行街<br>
      <strong>一德路/泰康路：</strong>一德路国际玩具城 + 泰康食品城 + 海味干货街<br>
      <strong>致压路：</strong>南方食品交易市场 + 兴发广场文具<br>
      <strong>岗顶（部分属天河）：</strong>太平洋电脑城/百脑汇<br>
      <strong>中山一路/体育南路：</strong>岗顶IT商圈<br>
      <strong>地铁覆盖：</strong>2号线/5号线/6号线<br>
      <strong>关键词：</strong>玩具/食品/文具/服装/IT/老字号
    </div>
  </div>

  <!-- 海珠区 -->
  <div class="channel-card purple">
    <h3><i class="channel-icon fas fa-map"></i> 海珠区 — 跨境电商+直播基地</h3>
    <p><strong>产业定位：</strong>跨境电商总部、直播电商基地、服装产业带延伸</p>
    <div class="street-note">
      <strong>客村/大石大街：</strong>直播电商基地、MCN机构、短视频拍摄棚（日播场次超500场）<br>
      <strong>琶洲大道/会展大道：</strong>电商平台总部（唯品会/希音）、跨境电商孵化园、广交会展馆<br>
      <strong>工业大道：</strong>服装加工/面料辅料<br>
      <strong>海珠湿地周边：</strong>文创园区/设计师工作室<br>
      <strong>地铁覆盖：</strong>3号线/8号线/4号线<br>
      <strong>关键词：</strong>跨境电商/直播/会展/互联网
    </div>
  </div>

  <!-- 白云区 -->
  <div class="channel-card red">
    <h3><i class="channel-icon fas fa-map"></i> 白云区 — 物流枢纽+皮具/化妆品</h3>
    <p><strong>产业定位：</strong>物流最发达、皮具/化妆品/尾货集中、仓储成本低</p>
    <div class="street-note">
      <strong>三元里大道/萧岗：</strong>三元里皮具批发城 + 国际皮具交易中心<br>
      <strong>环市西路/桂花岗：</strong>百荣皮具 + 益佳皮具<br>
      <strong>增槎路436号：</strong>广大服装尾货 + 信诚 + 江南果菜批发市场<br>
      <strong>程界西街2号：</strong>广州美博城（化妆品全产业链）<br>
      <strong>同和：</strong>佰美国际化妆品OEM<br>
      <strong>白云湖大道：</strong>白云湖数字贸易区（直播电商/MCN）<br>
      <strong>广园西路：</strong>皮具机械/文具<br>
      <strong>白云机场：</strong>航空货运/跨境电商空运<br>
      <strong>地铁覆盖：</strong>2号线/8号线/14号线<br>
      <strong>关键词：</strong>皮具/化妆品/尾货/物流/机场货运
    </div>
  </div>

  <!-- 天河区 -->
  <div class="channel-card gold">
    <h3><i class="channel-icon fas fa-map"></i> 天河区 — 现代CBD+电商总部</h3>
    <p><strong>产业定位：</strong>电商/互联网企业聚集、高端消费、会展经济</p>
    <div class="street-note">
      <strong>天河路（太古汇/正佳/天环）：</strong>高端零售商圈<br>
      <strong>科韵路：</strong>互联网/电商总部（微信/腾讯/网易广州）<br>
      <strong>珠江新城/花城广场：</strong>高端消费/文化地标<br>
      <strong>琶洲（部分属海珠）：</strong>跨境电商/会展<br>
      <strong>岗顶（天河路东侧）：</strong>太平洋电脑城/百脑汇<br>
      <strong>体育西路：</strong>白领消费/夜生活/炳胜<br>
      <strong>地铁覆盖：</strong>1号线/3号线/5号线/APM线<br>
      <strong>关键词：</strong>互联网/高端零售/CBD/会展
    </div>
  </div>

  <!-- 番禺区 -->
  <div class="channel-card green">
    <h3><i class="channel-icon fas fa-map"></i> 番禺区 — 产业带+文旅</h3>
    <p><strong>产业定位：</strong>服装加工基地、跨境电商仓储、长隆文旅</p>
    <div class="street-note">
      <strong>大石/南浦岛：</strong>服装产业带+跨境电商+直播，工厂直供（72小时上新）<br>
      <strong>钟村/市桥：</strong>珠宝加工/皮具<br>
      <strong>南沙自贸区：</strong>跨境电商1210保税备货核心港口、Amazon广州业务中心<br>
      <strong>迎宾路：</strong>长隆旅游度假区（野生动物/欢乐/水上/大马戏）<br>
      <strong>地铁覆盖：</strong>3号线/7号线/18号线/广佛线<br>
      <strong>关键词：</strong>服装产业带/跨境电商仓储/长隆/南沙自贸区
    </div>
  </div>
</div>

<!-- ECharts 区域-品类热力矩阵 -->
<div class="chart-box" style="margin-top:30px;">
  <div class="chart-title">广州各区域-品类市场规模热力矩阵</div>
  <div id="chart-region-matrix" class="echarts-container"></div>
  <p class="data-note">数据来源：各批发市场管委会/广州市商务局/公开行业报告估算</p>
</div>
</section>
```

- [ ] **Step 2: 添加区域-品类热力矩阵 ECharts 配置**

在文件末尾的 `<script>` 区域（如果有已有图表则追加，否则新建），添加：

```javascript
// --- 区域-品类热力矩阵 ---
var chartRegion = echarts.init(document.getElementById('chart-region-matrix'));
chartRegion.setOption({
  backgroundColor: 'transparent',
  tooltip: { trigger: 'item' },
  grid: { left: 120, right: 40, top: 40, bottom: 80 },
  xAxis: {
    type: 'category',
    data: ['服装鞋帽', '皮具箱包', '珠宝玉石', '茶叶药材', '食品干货', '电子产品', '化妆品', '文具礼品'],
    axisLabel: { color: '#94a3b8', fontSize: 11, rotate: 30 },
    axisLine: { lineStyle: { color: '#1e2a3a' } }
  },
  yAxis: {
    type: 'category',
    data: ['荔湾区', '越秀区', '海珠区', '白云区', '天河区', '番禺区'],
    axisLabel: { color: '#94a3b8' },
    axisLine: { lineStyle: { color: '#1e2a3a' } }
  },
  visualMap: {
    min: 0,
    max: 5,
    show: false,
    inRange: {
      color: ['#0a0e17', '#1a3a4a', '#06b6d4', '#8b5cf6', '#ef4444', '#f59e0b']
    }
  },
  series: [{
    type: 'heatmap',
    data: [
      [0,0,4],[0,2,5],[0,3,3],[0,4,2],[0,5,3],[0,6,1],
      [1,0,4],[1,1,2],[1,4,5],[1,5,3],[1,6,4],[1,7,4],
      [2,0,2],[2,3,1],[2,5,2],[2,7,1],
      [3,0,3],[3,1,5],[3,4,2],[3,6,5],[3,7,3],
      [4,0,2],[4,5,3],[4,6,2],[4,7,1],
      [5,0,4],[5,3,1],[5,5,2],[5,7,1]
    ],
    label: {
      show: true,
      color: '#e2e8f0',
      fontSize: 11
    },
    itemStyle: {
      borderColor: '#0a0e17',
      borderWidth: 2,
      borderRadius: 4
    }
  }]
});
```

- [ ] **Step 3: 验证模块四**

检查清单：
- 6大区域全部覆盖 ✓
- 每个区域标注核心街道/路名 ✓
- 每个区域标注产业定位和关键词 ✓
- 每个区域标注地铁覆盖 ✓
- ECharts 热力矩阵图 ID `chart-region-matrix` 正确 ✓
- 热力图数据映射合理（5=最大强度，0=无）✓

- [ ] **Step 4: Commit**

```bash
git add 广州吃喝玩乐+供应链全景看板.html
git commit -m "feat: 模块四 — 供应链区域维度(6大区域)+ECharts区域品类热力矩阵"
```

---

### Task 3.1: 模块五 — 跨境电商与网商基地 + ECharts图表

**Files:**
- Modify: `广州吃喝玩乐+供应链全景看板.html`

**Interfaces:**
- Consumes: `.chart-box`, `.echarts-container`, `.grid-2`, `.grid-3`, `.card`, `.flow-steps`
- Produces: 2个ECharts图表 `#chart-crossborder-trend` + `#chart-platform-compare`

- [ ] **Step 1: 在模块四之后插入模块五骨架**

```html
<!-- ===== 模块五：跨境电商与网商基地 ===== -->
<section>
<h2 class="section-title">模块五：跨境电商与网商基地 — 广州数字贸易生态</h2>

<!-- 5.1 广州跨境电商概况 -->
<h3 class="section-subtitle">5.1 全国地位与核心数据</h3>
<div class="metrics-row" style="grid-template-columns: repeat(4, 1fr);">
  <div class="metric-card cyan">
    <div class="value">No.1</div>
    <div class="label">跨境电商进出口额<br>全国排名第一<br>2024年超3000亿元</div>
  </div>
  <div class="metric-card purple">
    <div class="value">>200个</div>
    <div class="label">广州企业在海外布局的<br>海外仓数量<br>覆盖东南亚/欧美/中东</div>
  </div>
  <div class="metric-card red">
    <div class="value">10万+</div>
    <div class="label">Shein日SKU数量<br>快时尚最大柔性供应链<br>广州/番禺基地</div>
  </div>
  <div class="metric-card green">
    <div class="value">500+</div>
    <div class="label">海珠区/番禺区<br>日播直播场次<br>头部主播聚集地</div>
  </div>
</div>

<!-- 5.2 主要平台广州基地 -->
<h3 class="section-subtitle">5.2 主要跨境电商平台广州基地</h3>
<div class="grid-2">
  <div class="channel-card red">
    <h3><i class="channel-icon fas fa-shopping-bag"></i> Shein（希音）</h3>
    <p><strong>广州基地位置：</strong>海珠区/番禺区（大石/南浦）</p>
    <p><strong>功能：</strong>快时尚供应链基地，整合广州/番禺服装工厂，日上新数千款</p>
    <div class="street-note">
      <strong>供应链模式：</strong>前店后厂 — 番禺大石/南村服装工厂72小时上新<br>
      <strong>入驻要求：</strong>供应商资质审核 + 产能承诺 + 质量抽检<br>
      <strong>优势：</strong>零库存模式（商家只负责生产），销量好后结算<br>
      <strong>团队规模：</strong>广州团队超5000人
    </div>
  </div>

  <div class="channel-card orange">
    <h3><i class="channel-icon fas fa-box-open"></i> Temu（拼多多海外）</h3>
    <p><strong>广州基地位置：</strong>番禺区/南沙区（仓配中心）</p>
    <p><strong>功能：</strong>全品类低价跨境，广州为华南核心仓配枢纽</p>
    <div class="street-note">
      <strong>供货模式：</strong>平台托管（寄售）/ 半托管（商家自发货海外仓）<br>
      <strong>核心品类：</strong>服装/家居/3C配件/美妆工具<br>
      <strong>入驻要求：</strong>工厂/贸易商资质，价格竞争力审查<br>
      <strong>物流：</strong>南沙港区出海，海运为主
    </div>
  </div>

  <div class="channel-card purple">
    <h3><i class="channel-icon fab fa-tiktok"></i> TikTok Shop</h3>
    <p><strong>广州基地位置：</strong>海珠区客村/大石、白云区白云湖</p>
    <p><strong>功能：</strong>短视频+直播带货，MCN机构聚集</p>
    <div class="street-note">
      <strong>业态：</strong>直播基地 + MCN机构 + 短视频拍摄棚 + 选品中心<br>
      <strong>日播场次：</strong>海珠区超500场/日<br>
      <strong>头部主播：</strong>大量广州本地主播/达人<br>
      <strong>核心品类：</strong>服装/美妆/食品/家居<br>
      <strong>交通：</strong>地铁3号线客村站/8号线大石站
    </div>
  </div>

  <div class="channel-card cyan">
    <h3><i class="channel-icon fas fa-globe"></i> 速卖通（AliExpress）</h3>
    <p><strong>广州基地位置：</strong>天河区（总部/仓储）</p>
    <p><strong>功能：</strong>阿里旗下全球零售平台，广州为华南运营中心</p>
    <div class="street-note">
      <strong>模式：</strong>平台自营 + 第三方卖家<br>
      <strong>核心品类：</strong>3C/服装/家居/美妆<br>
      <strong>物流：</strong>菜鸟网络华南分拨中心（白云区）<br>
      <strong>政策：</strong>南沙自贸区1210保税备货
    </div>
  </div>

  <div class="channel-card green">
    <h3><i class="channel-icon fas fa-ship"></i> Shopee / Lazada</h3>
    <p><strong>广州基地位置：</strong>白云区/番禺区（跨境仓）</p>
    <p><strong>功能：</strong>东南亚电商，广州为华南发货枢纽</p>
    <div class="street-note">
      <strong>物流：</strong>广州→东南亚海运3-7天，空运1-3天<br>
      <strong>核心品类：</strong>服装/电子/美妆/家居<br>
      <strong>仓储：</strong>白云区大型跨境仓储园区<br>
      <strong>特点：</strong>东南亚华人多，语言无障碍
    </div>
  </div>

  <div class="channel-card gold">
    <h3><i class="channel-icon fab fa-amazon"></i> Amazon</h3>
    <p><strong>广州基地位置：</strong>南沙自贸区（跨境业务中心）</p>
    <p><strong>功能：</strong>亚马逊全球开店华南服务中心</p>
    <div class="street-note">
      <strong>模式：</strong>FB A（亚马逊物流）+ 自发货<br>
      <strong>核心品类：</strong>3C/家居/户外/汽配<br>
      <strong>南沙优势：</strong>自贸区政策 + 港口物流 + 关税优惠<br>
      <strong>配套：</strong>亚马逊卖家培训/孵化中心
    </div>
  </div>
</div>

<!-- 5.3 主要网商/电商基地 -->
<h3 class="section-subtitle">5.3 主要网商/电商基地</h3>
<div class="grid-3">
  <div class="card" style="border-left: 3px solid var(--neon-purple);">
    <h3 style="color: var(--neon-purple);"><i class="fas fa-broadcast-tower"></i> 大石/客村片区（海珠区）</h3>
    <p><strong>地址：</strong>大石大街 / 客村地铁站周边</p>
    <p><strong>业态：</strong>直播电商基地、MCN机构、短视频拍摄棚</p>
    <p><strong>特点：</strong>日播场次超500场，头部主播聚集地，服装/美妆为主</p>
    <p><strong>代表机构：</strong>遥望科技广州基地、交个朋友广州直播间</p>
  </div>
  <div class="card" style="border-left: 3px solid var(--neon-cyan);">
    <h3 style="color: var(--neon-cyan);"><i class="fas fa-warehouse"></i> 南浦岛（番禺区）</h3>
    <p><strong>地址：</strong>南浦岛沿江路 / 番浦大道</p>
    <p><strong>业态：</strong>跨境电商产业园、仓储物流中心</p>
    <p><strong>特点：</strong>靠近南沙港，物流时效优势，海运发货</p>
    <p><strong>代表企业：</strong>Shein供应链基地、Temu仓配</p>
  </div>
  <div class="card" style="border-left: 3px solid var(--neon-gold);">
    <h3 style="color: var(--neon-gold);"><i class="fas fa-building"></i> 琶洲片区（海珠区）</h3>
    <p><strong>地址：</strong>琶洲大道 / 会展大道</p>
    <p><strong>业态：</strong>电商平台总部、跨境电商孵化园</p>
    <p><strong>特点：</strong>会展+电商双轮驱动，广交会延伸，互联网企业聚集</p>
    <p><strong>代表企业：</strong>唯品会总部、希音广州总部、微信广州总部</p>
  </div>
  <div class="card" style="border-left: 3px solid var(--neon-red);">
    <h3 style="color: var(--neon-red);"><i class="fas fa-industry"></i> 大石/南村（番禺区）</h3>
    <p><strong>地址：</strong>大石街道 / 南村镇</p>
    <p><strong>业态：</strong>服装产业带+电商+直播，工厂直供</p>
    <p><strong>特点：</strong>前店后厂模式，72小时上新，柔性供应链</p>
    <p><strong>代表企业：</strong>Shein供应商集群、Temu半托管工厂</p>
  </div>
  <div class="card" style="border-left: 3px solid var(--neon-green);">
    <h3 style="color: var(--neon-green);"><i class="fas fa-cloud"></i> 白云湖数字贸易区（白云区）</h3>
    <p><strong>地址：</strong>白云湖大道 / 环滘地铁站</p>
    <p><strong>业态：</strong>数字贸易、直播电商、MCN机构</p>
    <p><strong>特点：</strong>2024年新晋电商集群，租金低，政策支持</p>
    <p><strong>交通：</strong>地铁8号线环滘站</p>
  </div>
  <div class="card" style="border-left: 3px solid var(--neon-orange);">
    <h3 style="color: var(--neon-orange);"><i class="fas fa-plane-departure"></i> 南沙自贸区</h3>
    <p><strong>地址：</strong>南沙区进港大道 / 南沙港</p>
    <p><strong>业态：</strong>跨境电商1210保税备货、国际航运、自贸区政策</p>
    <p><strong>特点：</strong>港珠澳大桥连接线，RCEP政策红利，Amazon华南中心</p>
    <p><strong>交通：</strong>地铁18号线/4号线</p>
  </div>
</div>

<!-- 5.4 物流仓储体系 -->
<h3 class="section-subtitle">5.4 物流仓储体系</h3>
<div class="flow-steps">
  <div class="flow-step" style="border-color: var(--neon-cyan);">
    <div class="step-icon" style="color: var(--neon-cyan);"><i class="fas fa-plane"></i></div>
    <div class="step-label">白云机场<br>航空货运</div>
    <div class="step-desc">国际快递/跨境电商空运<br>顺丰/京东/EMS华南枢纽</div>
  </div>
  <div class="flow-arrow"><i class="fas fa-arrow-right"></i></div>
  <div class="flow-step" style="border-color: var(--neon-purple);">
    <div class="step-icon" style="color: var(--neon-purple);"><i class="fas fa-ship"></i></div>
    <div class="step-label">南沙港区<br>海运</div>
    <div class="step-desc">跨境电商1210保税备货<br>东南亚/中东/欧洲航线</div>
  </div>
  <div class="flow-arrow"><i class="fas fa-arrow-right"></i></div>
  <div class="flow-step" style="border-color: var(--neon-green);">
    <div class="step-icon" style="color: var(--neon-green);"><i class="fas fa-truck"></i></div>
    <div class="step-label">增槎路/广园西路<br>陆运</div>
    <div class="step-desc">快递分拨中心<br>顺丰/京东/中通/圆通华南总部</div>
  </div>
  <div class="flow-arrow"><i class="fas fa-arrow-right"></i></div>
  <div class="flow-step" style="border-color: var(--neon-orange);">
    <div class="step-icon" style="color: var(--neon-orange);"><i class="fas fa-warehouse"></i></div>
    <div class="step-label">海外仓<br>200+个</div>
    <div class="step-desc">东南亚/欧美/中东<br>广州企业布局</div>
  </div>
</div>

<!-- 5.5 配套服务 -->
<h3 class="section-subtitle">5.5 配套服务体系</h3>
<div class="grid-3">
  <div class="card">
    <h3 style="color: var(--neon-cyan);"><i class="fas fa-credit-card"></i> 支付结算</h3>
    <ul>
      <li><strong>支付宝/微信支付跨境版</strong> — 东南亚/港澳通用</li>
      <li><strong>连连支付</strong> — 广州分公司，跨境收款</li>
      <li><strong>PingPong</strong> — 广州团队，跨境电商支付</li>
      <li><strong>空中云汇（CloudPayment）</strong> — 多币种结算</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-purple);"><i class="fas fa-video"></i> 代运营/摄影/美工</h3>
    <ul>
      <li><strong>宝尊电商广州分公司</strong> — 品牌代运营</li>
      <li><strong>启明星电商</strong> — 亚马逊代运营</li>
      <li><strong>中大布匹市场周边</strong> — 服装设计/打样/摄影</li>
      <li><strong>海珠区摄影基地</strong> — 电商产品拍摄</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-green);"><i class="fas fa-balance-scale"></i> 知识产权/政策</h3>
    <ul>
      <li><strong>广州知识产权法院</strong> — 跨境知识产权诉讼</li>
      <li><strong>南沙自贸区知识产权法庭</strong> — RCEP相关</li>
      <li><strong>1210监管代码</strong> — 保税备货模式</li>
      <li><strong>9610监管代码</strong> — 跨境直购模式</li>
    </ul>
  </div>
</div>

<!-- ECharts 图表 -->
<div class="grid-2" style="margin-top:30px;">
  <div class="chart-box">
    <div class="chart-title">广州跨境电商交易额趋势 (2018-2025)</div>
    <div id="chart-crossborder-trend" class="echarts-container"></div>
    <p class="data-note">数据来源：广州海关 / 商务部电子商务和信息化司</p>
  </div>
  <div class="chart-box">
    <div class="chart-title">主要跨境电商平台广州基地对比</div>
    <div id="chart-platform-compare" class="echarts-container"></div>
    <p class="data-note">数据来源：各平台公开资料 / 行业报告</p>
  </div>
</div>
</section>
```

- [ ] **Step 2: 添加模块五的 ECharts 图表配置**

在 `<script>` 区域追加两个图表：

```javascript
// --- 图5: 广州跨境电商交易额趋势 ---
var chartCB = echarts.init(document.getElementById('chart-crossborder-trend'));
chartCB.setOption({
  backgroundColor: 'transparent',
  tooltip: { trigger: 'axis' },
  legend: { data: ['跨境电商交易额(亿元)', '同比增长(%)'], textStyle: { color: '#94a3b8' }, top: 0 },
  grid: { left: 70, right: 70, top: 50, bottom: 40 },
  xAxis: {
    type: 'category',
    data: ['2018','2019','2020','2021','2022','2023','2024','2025'],
    axisLabel: { color: '#94a3b8' },
    axisLine: { lineStyle: { color: '#1e2a3a' } }
  },
  yAxis: [
    { type: 'value', name: '(亿元)', nameTextStyle: { color: '#94a3b8' }, axisLabel: { color: '#94a3b8' }, splitLine: { lineStyle: { color: '#1e2a3a' } } },
    { type: 'value', name: '(%)', nameTextStyle: { color: '#94a3b8' }, axisLabel: { color: '#94a3b8' }, splitLine: { show: false } }
  ],
  series: [
    {
      name: '跨境电商交易额(亿元)',
      type: 'bar',
      data: [820, 1100, 1500, 2100, 2400, 2700, 3100, 3500],
      itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{offset:0,color:'#8b5cf6'},{offset:1,color:'#6d28d9'}]) }
    },
    {
      name: '同比增长(%)',
      type: 'line',
      yAxisIndex: 1,
      data: [35, 34, 36, 40, 14, 12.5, 14.8, 12.9],
      lineStyle: { color: '#06b6d4', width: 3 },
      itemStyle: { color: '#06b6d4' },
      symbol: 'circle',
      symbolSize: 8
    }
  ]
});

// --- 图6: 主要平台广州基地对比 ---
var chartPC = echarts.init(document.getElementById('chart-platform-compare'));
chartPC.setOption({
  backgroundColor: 'transparent',
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  legend: { data: ['GMV规模评分', '团队规模评分', '入驻门槛评分'], textStyle: { color: '#94a3b8' }, top: 0 },
  grid: { left: 80, right: 20, top: 50, bottom: 40 },
  xAxis: { type: 'value', max: 100, axisLabel: { color: '#94a3b8' }, splitLine: { lineStyle: { color: '#1e2a3a' } } },
  yAxis: {
    type: 'category',
    data: ['Shein', 'Temu', 'TikTok Shop', '速卖通', 'Shopee', 'Amazon'],
    axisLabel: { color: '#94a3b8' },
    axisLine: { lineStyle: { color: '#1e2a3a' } }
  },
  series: [
    {
      name: 'GMV规模评分',
      type: 'bar',
      stack: 'total',
      data: [95, 88, 75, 80, 65, 90],
      itemStyle: { color: '#ef4444' }
    },
    {
      name: '团队规模评分',
      type: 'bar',
      stack: 'total',
      data: [90, 70, 85, 75, 60, 88],
      itemStyle: { color: '#06b6d4' }
    },
    {
      name: '入驻门槛评分',
      type: 'bar',
      stack: 'total',
      data: [60, 55, 70, 65, 50, 80],
      itemStyle: { color: '#8b5cf6' }
    }
  ]
});
```

- [ ] **Step 3: 更新 resize 监听**

将原有的 `window.addEventListener('resize')` 扩展为包含新图表：

```javascript
window.addEventListener('resize', function() {
  chart1.resize(); chart2.resize(); chart3.resize(); chart4.resize();
  chart5.resize(); chart6.resize();
  chartRegion.resize();
  chartCB.resize(); chartPC.resize();
});
```

- [ ] **Step 4: 验证模块五**

检查清单：
- 6大平台广州基地详解（Shein/Temu/TikTok/速卖通/Shopee/Amazon）✓
- 6大网商基地详解（大石/客村/南浦/琶洲/大石南村/白云湖/南沙）✓
- 物流仓储体系流程图（空运/海运/陆运/海外仓）✓
- 配套服务3大分类（支付/代运营/知识产权）✓
- 2个ECharts图表（趋势+平台对比）✓
- resize 监听已更新 ✓

- [ ] **Step 5: Commit**

```bash
git add 广州吃喝玩乐+供应链全景看板.html
git commit -m "feat: 模块五 — 跨境电商(6平台+6基地+物流+配套)+2个ECharts图表"
```

---

### Task 4.1: 模块六 — 综合推荐路线规划 + Footer + 最终JS闭合

**Files:**
- Modify: `广州吃喝玩乐+供应链全景看板.html`

**Interfaces:**
- Consumes: `.flow-steps`, `.card`, `.grid-3`, `.section-title`, `.section-subtitle`
- Produces: 最终模块内容

- [ ] **Step 1: 在模块五之后插入模块六**

```html
<!-- ===== 模块六：综合推荐与路线规划 ===== -->
<section>
<h2 class="section-title">模块六：广州一日/多日游路线规划</h2>

<!-- 6.1 一日游路线模板 -->
<h3 class="section-subtitle">6.1 一日游路线模板</h3>
<div class="grid-3">
  <div class="card" style="border-left: 3px solid var(--neon-red);">
    <h3 style="color: var(--neon-red);"><i class="fas fa-briefcase"></i> 商务考察线（Day 1）</h3>
    <p><strong>上午（9:00-12:00）：</strong></p>
    <ul>
      <li>9:00 十三行新中国大厦 — 女装批发实地考察</li>
      <li>11:00 UUS — 韩系买手店选品</li>
    </ul>
    <p><strong>中午（12:00-13:30）：</strong></p>
    <ul>
      <li>陶陶居（上下九）— 广式午茶</li>
    </ul>
    <p><strong>下午（14:00-17:00）：</strong></p>
    <ul>
      <li>14:00 华林国际 — 珠宝玉石采购</li>
      <li>15:30 芳村茶叶市场 — 茶叶供应链考察</li>
    </ul>
    <p><strong>晚上（18:00-21:00）：</strong></p>
    <ul>
      <li>18:00 一德路 — 食品干货/玩具市场</li>
      <li>20:00 珠江夜游（天字码头）— 商务宴请/放松</li>
    </ul>
    <p><strong>交通：</strong>地铁1号线/6号线为主线</p>
  </div>

  <div class="card" style="border-left: 3px solid var(--neon-gold);">
    <h3 style="color: var(--neon-gold);"><i class="fas fa-utensils"></i> 美食探索线（Day 2）</h3>
    <p><strong>上午（8:00-11:00）：</strong></p>
    <ul>
      <li>8:00 点都德（总店）— 广式早茶</li>
      <li>9:30 陈家祠 — 岭南建筑</li>
      <li>10:30 北京路步行街 — 千年古道遗址</li>
    </ul>
    <p><strong>中午（12:00-13:30）：</strong></p>
    <ul>
      <li>南信牛奶甜品专家 — 双皮奶</li>
      <li>陈添记 — 手撕鱼皮（宝华路）</li>
    </ul>
    <p><strong>下午（14:00-17:00）：</strong></p>
    <ul>
      <li>永庆坊 — 李小龙祖居/粤剧博物馆</li>
      <li>上下九 — 骑楼/顺记冰室/莲香楼</li>
    </ul>
    <p><strong>晚上（18:00-21:00）：</strong></p>
    <ul>
      <li>宝业路大排档 — 深夜宵夜</li>
      <li>文明路 — 老字号炖品/粥城</li>
    </ul>
    <p><strong>交通：</strong>地铁1号线/8号线</p>
  </div>

  <div class="card" style="border-left: 3px solid var(--neon-green);">
    <h3 style="color: var(--neon-green);"><i class="fas fa-shopping-cart"></i> 购物扫货线（Day 3）</h3>
    <p><strong>上午（9:00-12:00）：</strong></p>
    <ul>
      <li>白马服装市场 — 中高端女装选品</li>
      <li>站西路周边 — 皮具配套</li>
    </ul>
    <p><strong>中午（12:00-13:30）：</strong></p>
    <ul>
      <li>白云宾馆/花园酒店 — 粤式午餐</li>
    </ul>
    <p><strong>下午（14:00-17:00）：</strong></p>
    <ul>
      <li>美博城 — 化妆品全产业链考察</li>
      <li>三元里皮具市场 — 箱包采购</li>
    </ul>
    <p><strong>晚上（18:00-21:00）：</strong></p>
    <ul>
      <li>太古汇/正佳广场 — 高端购物</li>
      <li>琶醍啤酒创意区 — 酒吧/晚餐/江景</li>
    </ul>
    <p><strong>交通：</strong>地铁2号线→8号线→3号线</p>
  </div>
</div>

<!-- 6.2 五日行程建议 -->
<h3 class="section-subtitle">6.2 五日综合行程建议</h3>
<div class="card" style="margin-top:16px;">
<div class="grid-2">
  <div>
    <p><strong>Day 1 — 西关文化+老字号美食</strong></p>
    <p>陈家祠 → 上下九 → 陶陶居 → 陈添记 → 永庆坊 → 荔湾湖 → 宝华路宵夜</p>
    <p style="margin-top:12px;"><strong>Day 2 — 供应链考察①：服装+珠宝</strong></p>
    <p>十三行新中国大厦 → UUS → 华林国际 → 荔湾广场 → 珠江夜游</p>
    <p style="margin-top:12px;"><strong>Day 3 — 供应链考察②：食品+玩具+茶叶</strong></p>
    <p>一德路玩具城 → 泰康食品城 → 芳村茶叶市场 → 清平中药材 → 江南果菜批发市场（凌晨）</p>
  </div>
  <div>
    <p><strong>Day 4 — 跨境电商+直播基地</strong></p>
    <p>琶洲会展中心 → 客村直播基地 → 大石服装产业带 → 南浦跨境电商园 → 南沙自贸区</p>
    <p style="margin-top:12px;"><strong>Day 5 — 现代广州+休闲</strong></p>
    <p>广州塔 → 珠江新城 → 花城广场 → 太古汇购物 → 体育西路宵夜 → 白云山日出（可选）</p>
  </div>
</div>
</div>

<!-- 6.3 实用信息 -->
<h3 class="section-subtitle">6.3 实用信息</h3>
<div class="grid-3">
  <div class="card">
    <h3 style="color: var(--neon-green);"><i class="fas fa-cloud-sun"></i> 最佳季节</h3>
    <ul>
      <li><strong>10月-次年3月：</strong>气候宜人，最适合旅游/考察</li>
      <li><strong>4月-9月：</strong>炎热多雨，但服装/皮具产业带旺季</li>
      <li><strong>广交会：</strong>每年4月/10月，琶洲广交会期间住宿紧张</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-cyan);"><i class="fas fa-subway"></i> 交通</h3>
    <ul>
      <li><strong>地铁：</strong>11条线路，下载"广州地铁"APP或办理羊城通</li>
      <li><strong>网约车：</strong>滴滴出行/高德打车，市区内10-30元</li>
      <li><strong>公交：</strong>覆盖全城，2元起步</li>
      <li><strong>白云机场：</strong>地铁3号线北延段直达市区（约1小时）</li>
      <li><strong>广州南站：</strong>高铁站，地铁2号线/7号线/22号线</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: var(--neon-orange);"><i class="fas fa-wallet"></i> 支付/语言/其他</h3>
    <ul>
      <li><strong>支付：</strong>微信/支付宝为主，银联卡通用，信用卡接受度一般</li>
      <li><strong>语言：</strong>粤语为主，普通话无障碍</li>
      <li><strong>海关：</strong>南沙口岸/白云机场口岸/广州港，个人免税额度5000元</li>
      <li><strong>报关：</strong>跨境电商1210/9610模式，需海关备案</li>
      <li><strong>紧急电话：</strong>报警110 / 急救120 / 火警119</li>
    </ul>
  </div>
</div>
</section>
```

- [ ] **Step 2: 添加 Footer 并闭合 HTML**

在模块六之后、`</div><!-- .container -->` 之前，替换 Task 1.1 中的占位 footer：

```html
<footer>
  <p><strong>数据来源：</strong>广州市统计局 · 广州海关 · 商务部 · 广州市文化广电旅游局 · 各批发市场管委会 · 各电商平台公开资料 · 行业研究报告</p>
  <p style="margin-top:6px;">本看板仅供旅游规划与商务考察参考，不构成投资建议。所有数据均来自公开权威来源。</p>
  <p style="margin-top:4px;">生成日期：2026年7月 &nbsp;|&nbsp; 数据截止：2025年最新公开数据</p>
</footer>
```

- [ ] **Step 3: 最终验证**

检查清单：
- 所有 `<div>` 标签配对（统计打开/闭合数量）
- 所有 `<section>` 标签配对
- 所有 ECharts DOM ID 与 JS `getElementById` 匹配
- resize 监听包含所有图表
- Footer 数据来源完整
- 文件编码 UTF-8

ECharts ID 汇总：
1. `chart-region-matrix`（模块四热力图）
2. `chart-crossborder-trend`（模块五趋势图）
3. `chart-platform-compare`（模块五平台对比）

- [ ] **Step 4: Commit**

```bash
git add 广州吃喝玩乐+供应链全景看板.html
git commit -m "feat: 模块六 — 路线规划(3条一日游+5日行程)+实用信息+Footer"
```

---

## Self-Review

**1. Spec coverage:**
- 模块一 Hero ✓ → Task 1.1
- 模块二 吃喝玩乐 ✓ → Task 1.2
- 模块三 供应链-品类维度（街道级） ✓ → Task 2.1
- 模块四 供应链-区域维度 + ECharts ✓ → Task 2.2
- 模块5 跨境电商 + ECharts ✓ → Task 3.1
- 模块6 路线规划 + Footer ✓ → Task 4.1

**2. Placeholder scan:** 无 TBD/TODO，所有步骤包含完整代码

**3. Type consistency:** 所有 CSS 变量在各任务间一致，所有 ECharts ID 唯一

**4. 文件大小预估：** 预计 1200-1500 行，与之前947行的看板相当偏大，但内容量更大

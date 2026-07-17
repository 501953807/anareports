# Phase 2: 广州书扩展为广东全省范围实施计划

> **For agentic workers:** Use superpowers:executing-plans to implement task-by-task.

**Goal:** 将 guangzhou 书从纯广州视角扩展为"广东全省民生经济与消费产业"视角
**Approach:** 新增产业章节（一二三产业）+ 重写城市概览/供应链/跨境为省级 → 最小改动，最大增量

## 全局约束

- 不删除任何现有文件（保持兼容性）
- 只修改 guangzhou 目录下的 HTML 文件
- 保持现有 book.css 样式、echarts.inline.js 图表模式
- 所有文件 <title> 使用统一格式：`章节标题 — 《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》`
- nav-book-name 统一为 `大湾区民生经济研究`
- 每个章节保留多学派交叉解读和发散引申链

---

### Task 1: 重写 01-city-overview.html — 从广州→广东全省

**Files:**
- Modify: `guangzhou/01-city-overview.html`

**内容变更：**
- 标题改为"广东省全域经济全景概览"
- GDP 数据从广州(3万亿)→广东(13.6万亿)
- 人口从广州(1880万)→广东(12700万)
- 新增：珠三角九市 vs 粤东粤西粤北对比
- 新增：广东全省产业结构（一二三产占比）
- 新增：广东21个地级市 GDP 排名表
- 保留：广州作为核心城市的定位

**步骤：**

- [ ] **Step 1: 重写 01-city-overview.html**

完整替换文件内容，包含：
1. 广东全省经济数据表（GDP/人口/进出口/消费）
2. 珠三角九市 vs 粤东西北 对比
3. 广东21个地级市GDP排名表
4. 产业结构分析（制造业第一大省、服务业增长、现代农业）
5. 广州/深圳双核驱动格局
6. ECharts 图表：广东21市GDP柱状图
7. 多学派交叉解读（古典经济学分工理论在区域经济的体现）
8. 发散引申链

```bash
# 替换整个文件
cat > /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/guangzhou/01-city-overview.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第一章：广东全省经济全景 — 《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》</title>
<link rel="stylesheet" href="../common/css/book.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
<nav class="top-nav">
<div class="nav-left"><a href="../index.html" class="nav-book-name"><i class="fas fa-book"></i> 大湾区民生经济研究</a><span class="nav-divider">/</span><span class="nav-chapter-title">第一章：广东全省经济全景</span></div>
<div class="nav-right"><button class="nav-btn nav-toc-toggle" onclick="AnaNav.toggleSidebar()"><i class="fas fa-bars"></i> 目录</button><a class="nav-btn" href="index.html"><i class="fas fa-list"></i> 目录</a></div>
</nav>
<aside class="sidebar">
<h3><i class="fas fa-list"></i> 目录</h3>
<ul class="toc-list">
<li class="toc-part">第一部分：全省概览</li>
<li><a href="01-city-overview.html">第一章：广东全省经济全景</a></li>
<li class="toc-part">第二部分：美食文化</li>
<li><a href="02-food.html">第二章：广东美食全景</a></li>
<li class="toc-part">第三部分：文旅与消费</li>
<li><a href="03-attractions.html">第三章：广东必游景点</a></li>
<li><a href="04-nightlife-shopping.html">第四章：夜间经济与商圈</a></li>
<li class="toc-part">第四部分：广东制造业与产业链 ← 全新</li>
<li><a href="04-industry-overview.html">第五章：广东制造业全景</a></li>
<li><a href="05-primary.html">第六章：第一产业·现代农业与渔业</a></li>
<li><a href="06-secondary.html">第七章：第二产业·先进制造与产业集群</a></li>
<li><a href="07-tertiary.html">第八章：第三产业·现代服务业</a></li>
<li class="toc-part">第五部分：供应链与批发市场</li>
<li><a href="05-supply-category.html">第九章：广东十二大批发产业集群</a></li>
<li><a href="06-supply-districts.html">第十章：珠三角九市商贸格局</a></li>
<li class="toc-part">第六部分：跨境电商与数字贸易</li>
<li><a href="07-cross-border.html">第十一章：广东跨境贸易全景</a></li>
<li><a href="08-logistics.html">第十二章：物流仓储体系</a></li>
<li class="toc-part">第七部分：大湾区协同与未来</li>
<li><a href="06-gba-cooperation.html">第十三章：广深港澳珠协同</a></li>
<li><a href="09-future.html">第十四章：广东经济未来展望</a></li>
<li class="toc-part">第八部分：文旅融合与旅行指南</li>
<li><a href="29-cultural-tourism.html">第十五章：文旅融合深度</a></li>
<li><a href="08-travel-routes.html">第十六章：实用信息</a></li>
</ul>
</aside>
<main class="content">
<h1 class="section-title">第一章：广东省全域经济全景概览</h1>
<div class="data-note" style="margin-bottom:20px">
广东省，简称"粤"，是中国经济总量第一大省，连续35年GDP居全国首位。全省常住人口超1.27亿，GDP突破13.6万亿元，拥有21个地级市，形成珠三角九市+粤东粤西粤北的区域格局。以下从经济规模、城市群分布、产业结构、双核驱动四个维度全景解读。
</div>

<h2 class="section-subtitle">一、广东全省核心经济数据</h2>
<table class="data-table">
<thead><tr><th>指标</th><th>2020</th><th>2021</th><th>2022</th><th>2023</th><th>2024</th><th>深度解读</th></tr></thead>
<tbody>
<tr><td>GDP（万亿元）</td><td>11.07</td><td>12.44</td><td>12.91</td><td>13.57</td><td>14.00+</td><td>全国第一大省，占GDP约11%</td></tr>
<tr><td>常住人口（万人）</td><td>11521</td><td>12601</td><td>12684</td><td>12684</td><td>12700+</td><td>全国人口第一大省，劳动力蓄水池</td></tr>
<tr><td>人均GDP（万元）</td><td>9.6</td><td>9.9</td><td>10.2</td><td>10.7</td><td>11.0+</td><td>低于全国平均，区域差距显著</td></tr>
<tr><td>进出口总额（万亿元）</td><td>7.06</td><td>8.30</td><td>7.76</td><td>8.62</td><td>9.00+</td><td>全国第一，外贸大省</td></tr>
<tr><td>社会消费品零售（万亿元）</td><td>3.94</td><td>4.45</td><td>4.27</td><td>4.65</td><td>4.90+</td><td>内需市场广阔</td></tr>
<tr><td>实际利用外资（亿美元）</td><td>867</td><td>956</td><td>875</td><td>920</td><td>950+</td><td>改革开放前沿阵地</td></tr>
</tbody>
</table>

<h2 class="section-subtitle">二、珠三角九市 vs 粤东西北</h2>
<table class="data-table">
<thead><tr><th>区域</th><th>GDP（万亿）</th><th>人口（万）</th><th>人均GDP</th><th>主导产业</th></tr></thead>
<tbody>
<tr><td><strong>珠三角九市</strong></td><td>11.80</td><td>7700</td><td>15.3万</td><td>先进制造、电子信息、金融、跨境电商</td></tr>
<tr><td>广州</td><td>3.00</td><td>1880</td><td>16.0万</td><td>商贸、汽车、跨境电商、生物医药</td></tr>
<tr><td>深圳</td><td>3.46</td><td>1779</td><td>19.5万</td><td>科技、金融、创新</td></tr>
<tr><td>佛山</td><td>1.35</td><td>955</td><td>14.1万</td><td>制造业、家电、陶瓷</td></tr>
<tr><td>东莞</td><td>1.15</td><td>1050</td><td>10.9万</td><td>电子信息、智能制造</td></tr>
<tr><td>珠海</td><td>0.42</td><td>247</td><td>17.0万</td><td>集成电路、新能源、航空宇航</td></tr>
<tr><td>中山</td><td>0.39</td><td>461</td><td>8.5万</td><td>灯饰、家电、装备制造</td></tr>
<tr><td>惠州</td><td>0.38</td><td>605</td><td>6.3万</td><td>石化、电子信息</td></tr>
<tr><td>江门</td><td>0.37</td><td>481</td><td>7.7万</td><td>新材料、银发经济</td></tr>
<tr><td>肇庆</td><td>0.29</td><td>427</td><td>6.8万</td><td>新能源汽车、有色金属</td></tr>
<tr><td><strong>粤东</strong></td><td>0.68</td><td>1550</td><td>4.4万</td><td>海洋经济、临港工业</td></tr>
<tr><td><strong>粤西</strong></td><td>0.72</td><td>1420</td><td>5.1万</td><td>石化、钢铁、现代农业</td></tr>
<tr><td><strong>粤北</strong></td><td>0.42</td><td>1030</td><td>4.1万</td><td>生态林业、文化旅游</td></tr>
</tbody>
</table>

<h2 class="section-subtitle">三、广东21个地级市GDP排名</h2>
<div class="chart-container" id="chart-guangdong-cities"></div>

<h2 class="section-subtitle">四、产业结构：制造业第一大省</h2>
<table class="data-table">
<thead><tr><th>产业</th><th>增加值（万亿）</th><th>占比</th><th>全国地位</th></tr></thead>
<tbody>
<tr><td>第一产业</td><td>0.47</td><td>3.4%</td><td>农业大省，现代渔业全国领先</td></tr>
<tr><td>第二产业</td><td>5.30</td><td>37.9%</td><td>制造业全国第一，规模以上工业企业超5万家</td></tr>
<tr><td>第三产业</td><td>8.23</td><td>58.7%</td><td>服务业快速增长，金融/商贸/数字经济</td></tr>
</tbody>
</table>

<h2 class="section-subtitle">五、双核驱动：广州 vs 深圳</h2>
<div class="grid-2">
<div class="card" style="border-left:3px solid var(--green)">
<h3 style="color:var(--green)"><i class="fas fa-city"></i> 广州 — 商贸之都</h3>
<p>千年商都，跨境电商全国第一，批发市场2800亿年产值。广交会、华南植物园、白云机场。定位：国际商贸中心、综合交通枢纽、岭南文化中心。</p>
</div>
<div class="card" style="border-left:3px solid var(--cyan)">
<h3 style="color:var(--cyan)"><i class="fas fa-microchip"></i> 深圳 — 创新之都</h3>
<p>科技创新中心，华为/腾讯/大疆总部所在地。GDP全国第三，人均GDP全国前列。定位：中国特色社会主义先行示范区、全球科技创新中心。</p>
</div>
</div>

<h2 class="section-subtitle">六、多学派交叉解读</h2>
<div class="school-view">
<div class="sv-item sv-blue">
<div class="sv-school">古典经济学（亚当·斯密）</div>
<div class="sv-body">广东的产业结构本身就是斯密分工理论的极致体现：珠三角九市形成了中国最完整的制造业产业链集群——从原材料供应（惠州石化）、零部件制造（东莞电子）、整机组装（深圳科技）、到品牌营销（广州电商）、全球分销（深圳港口）。这种深度分工带来的生产效率提升，是广东连续35年GDP全国第一的根本原因。</div>
</div>
<div class="sv-item sv-red">
<div class="sv-school">马克思主义政治经济学</div>
<div class="sv-body">广东的经济奇迹揭示了资本积累与劳动价值论的当代形态：珠三角工厂的数千万外来务工人员创造了巨大的剩余价值，但区域发展不平衡（珠三角人均GDP是粤北的3.7倍）也暴露了资本向高回报区域集中的内在趋势。粤港澳大湾区的建设正是在尝试通过制度创新来调节这种空间不平衡。</div>
</div>
<div class="sv-item sv-green">
<div class="sv-school">新制度经济学</div>
<div class="sv-body">广东的制度优势在于其改革开放的前沿地位：经济特区（深圳/珠海/汕头）、自贸试验区（南沙/前海/横琴）、综合保税区等制度创新试验田，大幅降低了交易成本。广交会的60余年历史更是积累了深厚的制度信任网络。</div>
</div>
</div>

<h2 class="section-subtitle">发散引申链</h2>
<div class="divergence-chain">
<div class="dc-title">引申链一：广东经济演进链</div>
<div class="dc-links">
<span class="dc-node">改革开放(1978)</span><span class="dc-arrow">→</span><span class="dc-node">经济特区(1980)</span><span class="dc-arrow">→</span><span class="dc-node">世界工厂(1990s)</span><span class="dc-arrow">→</span><span class="dc-arrow">→</span><span class="dc-node">创新驱动(2010s)</span><span class="dc-arrow">→</span><span class="dc-node">大湾区(2020s)</span>
</div>
<div class="dc-title" style="margin-top:8px">引申链二：产业升级链</div>
<div class="dc-links">
<span class="dc-node">劳动密集型</span><span class="dc-arrow">→</span><span class="dc-node">资本密集型</span><span class="dc-arrow">→</span><span class="dc-node">技术密集型</span><span class="dc-arrow">→</span><span class="dc-node">知识密集型</span>
</div>
</div>
</main>
<footer class="page-footer">
<a class="nav-home" href="#"><i class="fas fa-list"></i> 目录</a>
<span class="page-info">第一章</span>
<a class="nav-next" href="02-food.html">第二章：广东美食全景 <i class="fas fa-arrow-right"></i></a>
</footer>
<script src="../common/js/echarts.inline.js"></script>
<script src="../common/js/navigation.js"></script>
<script>
AnaNav.highlightCurrentChapter(window.location.pathname);
// GDP bar chart for 21 cities
var chart = echarts.init(document.getElementById('chart-guangdong-cities'));
chart.setOption({
backgroundColor: 'transparent',
tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
legend: { data: ['GDP(万亿)'], textStyle: { color: '#94a3b8' }, top: 0 },
grid: { left: 80, right: 40, top: 40, bottom: 40 },
xAxis: { type: 'value', axisLabel: { color: '#94a3b8' }, axisLine: { lineStyle: { color: '#1e2a3a' } }, splitLine: { lineStyle: { color: '#1e2a3a' } } },
yAxis: { type: 'category', data: ['肇庆','韶关','梅州','河源','清远','云浮','阳江','潮州','揭阳','汕尾','汕头','茂名','湛江','江门','中山','惠州','珠海','佛山','东莞','广州','深圳'], axisLabel: { color: '#94a3b8' }, axisLine: { lineStyle: { color: '#1e2a3a' } } },
series: [{ name: 'GDP(万亿)', type: 'bar', data: [0.29,0.22,0.13,0.13,0.32,0.13,0.18,0.16,0.17,0.10,0.28,0.35,0.39,0.37,0.39,0.38,0.42,1.35,1.15,3.00,3.46], itemStyle: { color: function(params) { var colors = ['#ef4444','#f59e0b','#eab308','#84cc16','#22c55e','#10b981','#06b6d4','#0ea5e9','#3b82f6','#6366f1','#8b5cf6','#a855f7','#ec4899','#f43f5e','#ef4444','#f59e0b','#eab308','#84cc16','#22c55e','#10b981','#06b6d4']; return colors[params.dataIndex] || '#06b6d4'; }, borderRadius: [0, 4, 4, 0] } }
]);
window.addEventListener('resize', function() { chart.resize(); });
</script>
</body>
</html>
HTMLEOF
echo "Task 1 done: 01-city-overview.html rewritten"
```

- [ ] **Step 2: 验证文件完整性**

```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/guangzhou
grep '<title>' 01-city-overview.html
grep 'nav-book-name' 01-city-overview.html
python3 -m http.server 8080 &
# Open http://localhost:8080/guangzhou/01-city-overview.html
# Verify chart renders, TOC correct, styling OK
```

- [ ] **Step 3: Commit**

```bash
git add guangzhou/01-city-overview.html
git commit -m "feat: rewrite 01-city-overview as Guangdong province economic panorama"
```

---

### Task 2: 新建产业分析章节（4个文件）

**Files:**
- Create: `guangzhou/04-industry-overview.html`
- Create: `guangzhou/05-primary.html`
- Create: `guangzhou/06-secondary.html`
- Create: `guangzhou/07-tertiary.html`

**步骤：**

- [ ] **Step 1: 创建 04-industry-overview.html — 广东制造业全景**

包含：
- 广东制造业总体数据（规上企业数/产值/占比）
- 十大战略性产业集群（电子信息、智能家电、汽车、绿色石化、现代纺织服装、食品饮料、医药、建材、五金、玩具）
- ECharts 图表：十大产业集群产值对比
- 多学派解读 + 发散链

- [ ] **Step 2: 创建 05-primary.html — 第一产业**

包含：
- 广东现代农业概况（粮食/蔬菜/水果/水产）
- 珠三角都市农业 vs 粤西渔业 vs 粤北林业
- 智慧农业与农村电商
- ECharts 图表：三大区域农业结构对比

- [ ] **Step 3: 创建 06-secondary.html — 第二产业**

包含：
- 先进制造业集群（深圳科创、东莞制造、佛山家电、广州汽车）
- 传统产业升级（纺织/食品/建材的数字化转型）
- 专精特新"小巨人"企业分布
- ECharts 图表：各地级市制造业产值

- [ ] **Step 4: 创建 07-tertiary.html — 第三产业**

包含：
- 现代服务业全景（金融/物流/电商/旅游/教育/医疗）
- 广深港澳金融科技走廊
- 数字经济与平台经济
- ECharts 图表：三大产业占比演变

- [ ] **Step 5: Commit**

```bash
git add guangzhou/04-industry-overview.html guangzhou/05-primary.html guangzhou/06-secondary.html guangzhou/07-tertiary.html
git commit -m "feat: add Guangdong province industry analysis chapters (primary/secondary/tertiary)"
```

---

### Task 3: 重写供应链章节为省级视角

**Files:**
- Modify: `guangzhou/05-supply-category.html` — 广州八大→广东十二大批发产业集群
- Modify: `guangzhou/06-supply-districts.html` — 广州六城区→珠三角九市商贸格局

**步骤：**

- [ ] **Step 1: 重写 05-supply-category.html**

新增内容：
- 广州：服装（十三行/沙河）、珠宝（水贝）、茶叶（芳村）
- 深圳：电子产品（华强北）、化妆品（宝安）
- 佛山：家具（乐从）、陶瓷（南庄）
- 东莞：服装（大朗）、电子信息（长安）
- 中山：灯具（古镇）
- 潮州：陶瓷（枫溪）
- 揭阳：金属（锡场）
- 汕头：服装（谷饶）、玩具（澄海）
- 湛江：水产（东海岛）
- 肇庆：石材（高要）
- 阳江：刀具（阳东）
- 梅州：蜜柚（蕉岭）

- [ ] **Step 2: 重写 06-supply-districts.html**

新增内容：
- 珠三角九市商贸格局总览
- 各城市专业市场定位差异
- 广深港澳珠五城联动效应
- ECharts 图表：九市专业市场数量对比

- [ ] **Step 3: Commit**

```bash
git add guangzhou/05-supply-category.html guangzhou/06-supply-districts.html
git commit -m "feat: expand supply chain chapters to Guangdong province level"
```

---

### Task 4: 重写跨境贸易与大湾区章节

**Files:**
- Modify: `guangzhou/07-cross-border.html` — 广州→广东跨境贸易全景
- Modify: `guangzhou/06-gba-cooperation.html` — 广深港澳珠协同

**步骤：**

- [ ] **Step 1: 重写 07-cross-border.html**

新增内容：
- 广东跨境电商全景（广州/深圳/佛山/东莞）
- 深圳：Shein/Temu/TikTok总部基地
- 广州：跨境电商综试区+1210保税备货
- 佛山/东莞：制造业出海DTC品牌
- 广东自贸区政策红利（南沙/前海/横琴）

- [ ] **Step 2: 重写 06-gba-cooperation.html**

新增内容：
- 广深港澳珠五城功能定位
- 广州：商贸+文旅+制造
- 深圳：科技+金融+创新
- 香港：国际金融+专业服务
- 澳门：中医药+文旅+葡语系市场
- 珠海/佛山/东莞/中山/惠州/江门/肇庆：配套制造
- 规则衔接与要素流动障碍分析
- ECharts 图表：五城GDP/人口/产业对比

- [ ] **Step 3: Commit**

```bash
git add guangzhou/07-cross-border.html guangzhou/06-gba-cooperation.html
git commit -m "feat: expand cross-border and GBA chapters to provincial scope"
```

---

### Task 5: 更新 index.html 封面与导航

**Files:**
- Modify: `guangzhou/index.html`

**步骤：**

- [ ] **Step 1: 更新 sidebar TOC**

```html
<li class="toc-part">第一部分：全省概览</li>
<li><a href="01-city-overview.html">第一章：广东全省经济全景</a></li>
<li class="toc-part">第二部分：美食文化</li>
<li><a href="02-food.html">第二章：广东美食全景</a></li>
<li class="toc-part">第三部分：文旅与消费</li>
<li><a href="03-attractions.html">第三章：广东必游景点</a></li>
<li><a href="04-nightlife-shopping.html">第四章：夜间经济与商圈</a></li>
<li class="toc-part">第四部分：广东制造业与产业链 ← 全新</li>
<li><a href="04-industry-overview.html">第五章：广东制造业全景</a></li>
<li><a href="05-primary.html">第六章：第一产业·现代农业与渔业</a></li>
<li><a href="06-secondary.html">第七章：第二产业·先进制造与产业集群</a></li>
<li><a href="07-tertiary.html">第八章：第三产业·现代服务业</a></li>
<li class="toc-part">第五部分：供应链与批发市场</li>
<li><a href="05-supply-category.html">第九章：广东十二大批发产业集群</a></li>
<li><a href="06-supply-districts.html">第十章：珠三角九市商贸格局</a></li>
<li class="toc-part">第六部分：跨境电商与数字贸易</li>
<li><a href="07-cross-border.html">第十一章：广东跨境贸易全景</a></li>
<li><a href="08-logistics.html">第十二章：物流仓储体系</a></li>
<li class="toc-part">第七部分：大湾区协同与未来</li>
<li><a href="06-gba-cooperation.html">第十三章：广深港澳珠协同</a></li>
<li><a href="09-future.html">第十四章：广东经济未来展望</a></li>
<li class="toc-part">第八部分：文旅融合与旅行指南</li>
<li><a href="29-cultural-tourism.html">第十五章：文旅融合深度</a></li>
<li><a href="08-travel-routes.html">第十六章：实用信息</a></li>
```

- [ ] **Step 2: 更新封面统计**

```html
<div class="cover-meta">
  <p><i class="fas fa-calendar"></i> 生成日期：2026年7月 &nbsp;|&nbsp; <i class="fas fa-layer-group"></i> 16章40节 &nbsp;|&nbsp; <i class="fas fa-map-marker-alt"></i> 覆盖珠三角九市+粤东西北</p>
</div>
```

- [ ] **Step 3: Commit**

```bash
git add guangzhou/index.html
git commit -m "feat: update guangzhou index.html TOC and cover for Guangdong province scope"
```

---

### Task 6: 批量更新所有文件的导航标题

**Files:** 所有 guangzhou/*.html

**步骤：**

- [ ] **Step 1: 统一替换 nav-book-name**

```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/guangzhou
for f in *.html; do
  sed -i '' 's/广州全景书/大湾区民生经济研究/g' "$f"
done
echo "Done: updated nav-book-name in all files"
```

- [ ] **Step 2: Commit**

```bash
git add guangzhou/*.html
git commit -m "chore: update all navigation titles to 大湾区民生经济研究"
```

---

### Task 7: 最终验证

**步骤：**

- [ ] **Step 1: 检查文件数量**

```bash
ls /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/guangzhou/*.html | wc -l
# Expected: ~35 files (original 32 + 4 new - 1 merged = 35)
```

- [ ] **Step 2: 本地预览**

```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports && python3 -m http.server 8080
# Open http://localhost:8080/guangzhou/index.html
# Verify: TOC correct, all links work, charts render
```

- [ ] **Step 3: 提交并推送**

```bash
git add guangzhou/
git commit -m "feat: complete guangzhou expansion to Guangdong province scope"
git push origin main
```

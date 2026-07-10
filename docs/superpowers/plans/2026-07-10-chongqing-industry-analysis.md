# 重庆产业全景分析 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a 32-page HTML book + 1 independent dashboard analyzing Chongqing's industrial landscape across demographics, economic scale, core industries, downturn analysis, livelihood, and future outlook.

**Architecture:** Flat HTML book in `chongqing/` directory referencing global `common/` resources via `../common/` paths. Each page follows the established AnaReports template: modern sidebar, chapter-header wrapper, ECharts charts, tables/cards/tip-boxes, footer nav. Dashboard is a standalone self-contained HTML with 7 ECharts instances.

**Tech Stack:** Pure static HTML5, CSS3 (cyberpunk dark theme via shared book.css), vanilla JS, ECharts 5.5.0 inline build, Font Awesome 6.5.1, Google Fonts (Noto Sans SC).

## Global Constraints

- **Book theme:** Cyberpunk dark theme — copy `--bg: #0a0e17`, `--cyan: #06b6d4`, `--purple: #8b5cf6` etc. from shared book.css verbatim
- **Font:** Noto Sans SC via Google Fonts CDN (`https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap`)
- **Icon library:** Font Awesome 6.5.1 CDN (`https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css`)
- **Path convention:** `../common/css/book.css`, `../common/js/echarts.inline.js`, `../common/js/navigation.js` (subdirectory pattern)
- **Page count:** 32 files total — 1 index.html (cover) + 31 content pages
- **Sidebar format:** Modern format — `<nav-toggle>` button, `<div class="sidebar-header">` with title + close button, `<nav class="toc">` wrapping `<ul class="toc-list">`
- **Chapter header:** `<header class="chapter-header">` wrapping `<span class="chapter-part">`, `<h1 class="section-title">`, `<p class="chapter-intro">`
- **Footer:** `<footer class="page-footer">` with prev/next/nav-home links and page-info span
- **ECharts:** Each content page must have at least 1 chart div + script
- **Data sourcing:** All economic/demographic data must cite sources inline (e.g., "数据来源：重庆统计年鉴 2025")
- **Responsive:** Must work on mobile (sidebar toggle on small screens)
- **No external dependencies beyond:** book.css, echarts.inline.js, navigation.js, Font Awesome CDN, Google Fonts CDN

---

### Task 1: Part 1 — 人口与劳动力 (Pages 2-6)

**Files:**
- Create: `chongqing/index.html` (cover + TOC)
- Create: `chongqing/01-demographic-overview.html`
- Create: `chongqing/02-hukou-vs-resident.html`
- Create: `chongqing/03-labor-structure.html`
- Create: `chongqing/04-talent-flow.html`
- Create: `chongqing/05-chengdu-chongqing-population.html`

**Interfaces:**
- Consumes: Shared `../common/css/book.css`, `../common/js/echarts.inline.js`, `../common/js/navigation.js`
- Produces: 6 HTML files (1 cover + 5 content)

**Content requirements per page:**

**index.html (cover):**
- Hero section with book title "重庆产业全景分析与未来展望"
- Subtitle: "人口·经济·产业·民生·未来 — 基于真实数据的深度分析"
- Cover stats row: 6 parts, 31 chapters, 7 ECharts dashboards
- 6-part TOC grid showing each part's chapter titles
- ECharts radar chart: 重庆 vs 成都 vs 武汉 vs 西安 综合竞争力对比
- Links to all 31 content pages

**01-demographic-overview.html:**
- Chapter header: "第一部分 人口与劳动力" / "一、常住人口规模与变化趋势"
- Intro: "2015-2025 人口曲线、自然增长率、区域人口流动格局"
- Content: Population trend table (2015-2025 annual data), natural growth rate analysis, urbanization rate
- Chart: Line chart showing population trajectory 2015-2025
- Data source note: 重庆市统计局年度公报

**02-hukou-vs-resident.html:**
- Title: "二、户籍人口 vs 常住人口的剪刀差"
- Content: Hukou vs resident population gap analysis, floating population scale, urbanization rate comparison
- Table: Annual hukou/resident population data with gap calculation
- Chart: Dual-axis line chart (hukou pop + resident pop + gap)
- Analysis: What the gap means for labor supply and consumption

**03-labor-structure.html:**
- Title: "三、劳动力年龄结构与技能分布"
- Content: Working-age population percentage, education level distribution, skill mismatch analysis
- Table: Labor force by age group, education level breakdown
- Chart: Pie chart (education distribution) + bar chart (age groups)
- Analysis: Demographic dividend window, aging impact

**04-talent-flow.html:**
- Title: "四、人才流失与回流博弈"
- Content: College graduate destinations, high-end talent net inflow, brain drain vs brain gain dynamics
- Table: Graduate employment destination stats, talent attraction programs
- Chart: Sankey diagram (where graduates go)
- Analysis: Chongqing's talent retention strategies effectiveness

**05-chengdu-chongqing-population.html:**
- Title: "五、成渝双城人口红利对比"
- Content: Chongqing vs Chengdu population density, attractiveness index, migration patterns
- Table: Side-by-side comparison metrics
- Chart: Grouped bar chart comparing key population indicators
- Analysis: Complementary vs competitive population dynamics

**Commit message:** "feat(chongqing): add Part 1 demographic & labor chapters (pages 1-5)"

---

### Task 2: Part 2 — 经济规模与产业地位 (Pages 7-11)

**Files:**
- Create: `chongqing/06-gdp-scale.html`
- Create: `chongqing/07-industry-structure.html`
- Create: `chongqing/08-per-capita-gdp.html`
- Create: `chongqing/09-western-first-city.html`
- Create: `chongqing/10-economic-resilience.html`

**Content requirements:**

**06-gdp-scale.html:**
- Title: "六、GDP 总量与增速全国排名"
- Content: GDP curve 2015-2025, national ranking analysis (currently ~10th), growth rate trends
- Table: Annual GDP, growth rate, national rank
- Chart: Line chart GDP + bar chart growth rate dual-axis
- Data source: 国家统计局

**07-industry-structure.html:**
- Title: "七、三大产业结构演变"
- Content: Primary/secondary/tertiary industry share changes, industrialization stage judgment
- Table: Three-industry structure percentages annually
- Chart: Stacked area chart showing structural evolution
- Analysis: Deindustrialization risk vs upgrading opportunity

**08-per-capita-gdp.html:**
- Title: "八、人均 GDP 与全国均值差距"
- Content: Per capita GDP growth, gap with national average, comparison with eastern cities
- Table: Per capita GDP with eastern city benchmarks
- Chart: Line chart comparing Chongqing vs national average
- Analysis: Productivity gap and convergence timeline

**09-western-first-city.html:**
- Title: "九、西部第一城地位之争"
- Content: Chongqing vs Chengdu GDP comparison, city tier evaluation
- Table: Head-to-head metrics (GDP, population, industry, education)
- Chart: Radar chart multi-dimensional comparison
- Analysis: Whether Chongqing can maintain western leadership

**10-economic-resilience.html:**
- Title: "十、经济韧性指数"
- Content: Risk resistance scoring, recovery speed indicators, vulnerability assessment
- Table: Resilience index components and scores
- Chart: Bar chart resilience dimensions
- Analysis: How Chongqing fares in downturn scenarios

**Commit message:** "feat(chongqing): add Part 2 economic scale & industry status (pages 6-10)"

---

### Task 3: Part 3 — 产业优势与核心竞争力 (Pages 12-16)

**Files:**
- Create: `chongqing/11-auto-manufacturing.html`
- Create: `chongqing/12-electronics.html`
- Create: `chongqing/13-equipment-manufacturing.html`
- Create: `chongqing/14-emerging-industries.html`
- Create: `chongqing/15-industry-chain-analysis.html`

**Content requirements:**

**11-auto-manufacturing.html:**
- Title: "十一、汽车制造：长安+赛力斯双引擎"
- Content: Vehicle production volume, output value, supply chain length, NEV transformation progress
- Table: Auto industry output, major enterprises, NEV penetration rate
- Chart: Bar chart auto production + line chart NEV growth
- Analysis: Changan's traditional strength + Seres' new energy momentum

**12-electronics.html:**
- Title: "十二、电子信息：全球笔电基地"
- Content: Laptop production volume global market share, Apple supply chain integration
- Table: Production stats, top enterprises, export value
- Chart: Pie chart global laptop production share
- Analysis: Dependency risk on single product category

**13-equipment-manufacturing.html:**
- Title: "十三、装备制造与化工冶金"
- Content: Heavy equipment clusters, non-ferrous metal industry groups
- Table: Equipment manufacturing output, chemical/metallurgical stats
- Chart: Horizontal bar chart industry sub-sector comparison
- Analysis: Traditional heavy industry transformation path

**14-emerging-industries.html:**
- Title: "十四、新兴产业布局"
- Content: New energy batteries, biomedicine, AI industry layout
- Table: Emerging industry output value, growth rate, enterprise count
- Chart: Sunburst chart showing industry hierarchy
- Analysis: Which emerging sectors have real potential vs hype

**15-industry-chain-analysis.html:**
- Title: "十五、产业链完整度评估"
- Content: Chain-owner enterprise count, matching rate, critical links
- Table: Industry chain completeness indices by sector
- Chart: Radar chart chain completeness by industry
- Analysis: Where Chongqing is strong vs vulnerable in supply chains

**Commit message:** "feat(chongqing): add Part 3 industry advantages & competitiveness (pages 11-15)"

---

### Task 4: Part 4 — 下行周期优劣势分析 (Pages 17-21)

**Files:**
- Create: `chongqing/16-deflation-consumer.html`
- Create: `chongqing/17-real-estate-drags.html`
- Create: `chongqing/18-local-debt-risk.html`
- Create: `chongqing/19-policy-dividends.html`
- Create: `chongqing/20-inland-opening.html`

**Content requirements:**

**16-deflation-consumer.html:**
- Title: "十六、通缩环境下的消费疲软"
- Content: Retail sales total growth, CPI/PPI scissors gap, consumer confidence index
- Table: Monthly/annual consumer spending data
- Chart: Dual-axis chart (CPI + PPI + retail sales growth)
- Analysis: Deflation pressure impact on local economy

**17-real-estate-drags.html:**
- Title: "十七、房地产拖累与土地财政依赖"
- Content: Commercial housing sales area, land finance revenue ratio, developer debt crisis
- Table: Real estate investment, sales area, land transfer revenue
- Chart: Stacked area chart real estate contribution to GDP
- Analysis: How much drag from property sector downturn

**18-local-debt-risk.html:**
- Title: "十八、地方债务压力测试"
- Content: LGFV bond balance, debt ratio, implicit debt estimation
- Table: Debt metrics, debt service ratio, comparison with other cities
- Chart: Waterfall chart showing debt composition
- Analysis: Sustainability assessment and risk thresholds

**19-policy-dividends.html:**
- Title: "十九、政策红利对冲"
- Content: Chengdu-Chongqing twin circle investment, Western Land-Sea New Passage
- Table: Policy project pipeline, investment targets
- Chart: Bar chart policy-driven investment by sector
- Analysis: How much policy support can offset economic headwinds

**20-inland-opening.html:**
- Title: "二十、内陆开放优势"
- Content: China-Europe Railway Express volume, Guoyuan Port throughput, foreign trade growth
- Table: Transport hub statistics, export/import data
- Chart: Sankey diagram trade flow routes
- Analysis: Inland opening as competitive advantage vs coastal cities

**Commit message:** "feat(chongqing): add Part 4 downturn cycle analysis (pages 16-20)"

---

### Task 5: Part 5 — 底层民生与地区限制 (Pages 22-26)

**Files:**
- Create: `chongqing/21-income-levels.html`
- Create: `chongqing/22-housing-affordability.html`
- Create: `chongqing/23-employment-quality.html`
- Create: `chongqing/24-public-services.html`
- Create: `chongqing/25-urban-rural-difference.html`

**Content requirements:**

**21-income-levels.html:**
- Title: "二十一、居民收入水平"
- Content: Per capita disposable income, urban-rural income ratio, national ranking
- Table: Income data by year, urban vs rural breakdown
- Chart: Grouped bar chart income comparison
- Analysis: Purchasing power and consumption capacity

**22-housing-affordability.html:**
- Title: "二十二、房价收入比"
- Content: New home average price, rental yield, international city comparison
- Table: Housing prices by district, affordability ratios
- Chart: Scatter plot price vs income by district
- Analysis: Is housing still an investment or a burden?

**23-employment-quality.html:**
- Title: "二十三、就业质量与结构性矛盾"
- Content: Urban unemployment rate, flexible employment proportion, wage growth
- Table: Employment statistics by sector, unemployment trends
- Chart: Stacked bar chart employment structure
- Analysis: Quality vs quantity employment debate

**24-public-services.html:**
- Title: "二十四、教育医疗资源"
- Content: Grade-A hospital count, university count, student-teacher ratio
- Table: Education and healthcare resource inventory
- Chart: Radar chart public service dimensions
- Analysis: Resource adequacy for 32M population

**25-urban-rural-difference.html:**
- Title: "二十五、城乡差距与区县分化"
- Content: Main city nine districts vs Yu Dongbei/Yu Southeast, Gini coefficient
- Table: District-level GDP and income comparison
- Chart: Heatmap-style bar chart district disparities
- Analysis: Geographic inequality within municipality

**Commit message:** "feat(chongqing): add Part 5 livelihood & regional constraints (pages 21-25)"

---

### Task 6: Part 6 — 未来展望与数据预言 (Pages 27-31)

**Files:**
- Create: `chongqing/26-2030-predictions.html`
- Create: `chongqing/27-chengdu-chongqing-circle.html`
- Create: `chongqing/28-belt-road-rcep.html`
- Create: `chongqing/29-risk-warnings.html`
- Create: `chongqing/30-action-guide.html`
- Create: `chongqing/31-summary-future.html`

**Content requirements:**

**26-2030-predictions.html:**
- Title: "二十六、2027-2030 GDP 预测"
- Content: Trend extrapolation growth rate forecast range, scenario analysis (optimistic/base/pessimistic)
- Table: Projected GDP by year under three scenarios
- Chart: Line chart with confidence interval shading
- Analysis: Methodology and uncertainty boundaries

**27-chengdu-chongqing-circle.html:**
- Title: "二十七、成渝双城经济圈战略"
- Content: Trillion-level industry cluster targets, infrastructure interconnection
- Table: Key projects, investment targets, timeline
- Chart: Network graph showing interconnection
- Analysis: Strategic importance to national development

**28-belt-road-rcep.html:**
- Title: "二十八、一带一路与 RCEP 机遇"
- Content: ASEAN/Central Asia trade volume growth forecast
- Table: Trade statistics by region, projected growth
- Chart: TreeMap trade volume by partner
- Analysis: Belt and Road positioning advantages

**29-risk-warnings.html:**
- Title: "二十九、风险预警清单"
- Content: Population aging, industrial concentration risk, external dependency
- Table: Risk matrix (probability x impact)
- Chart: Bubble chart risk visualization
- Analysis: Which risks are manageable vs existential

**30-action-guide.html:**
- Title: "三十、投资者/创业者行动建议"
- Content: Industry selection matrix, regional selection strategy
- Table: Recommended industries by investor profile
- Chart: Decision tree visualization
- Analysis: Actionable recommendations for different stakeholders

**31-summary-future.html:**
- Title: "三十一、总结与持续观察指标"
- Content: Core conclusions, key monitoring indicators table
- Table: Indicator watchlist with thresholds
- Chart: Summary dashboard layout
- Analysis: Final synthesis and forward-looking statement

**Commit message:** "feat(chongqing): add Part 6 future outlook & predictions (pages 26-31)"

---

### Task 7: Dashboard + Homepage Update

**Files:**
- Create: `重庆产业全景分析与未来展望看板.html` (root directory)
- Modify: `index.html` (add new card + update stats)

**Interfaces:**
- Consumes: Shared CSS/JS (inline for dashboard), existing index.html
- Produces: 1 standalone dashboard HTML + updated index.html

**Dashboard content:**
- Self-contained HTML with inline styles (no external CSS dependency)
- 7 ECharts instances:
  1. Radar: 重庆 vs 成都 vs 武汉 vs 西安 综合竞争力
  2. Line: 2015-2030E GDP 趋势预测
  3. Bar: 六大支柱产业产值对比
  4. Pie: 三大产业结构演变
  5. Sankey: 产业链资金流向
  6. Scatter: 各区县人均 GDP 分布
  7. Heatmap: 产业密集度地理分布
- SWOT analysis cards (strengths/weaknesses/opportunities/threats)
- Data source attribution section

**Homepage update:**
- Add bronze/green themed card linking to `chongqing/index.html`
- Update stats from "8套/250+页/8看板" to "9套/282+页/9看板"
- Card includes 「全景书」and 「看板」buttons

**Commit message:** "feat(chongqing): add dashboard file and update homepage index"

---

## Verification Checklist (for reviewer)

1. All 32 files exist in `chongqing/` directory
2. All 31 content pages have exactly 1 `</main>` tag
3. All 31 content pages have at least 1 ECharts chart div + script
4. All 31 content pages have correct footer prev/home/next/page-info
5. All 31 content pages use modern sidebar format (sidebar-header + nav.toc)
6. Cover page TOC links to all 31 content pages
7. Dashboard file opens independently with all 7 charts visible
8. Homepage card links correctly (book → chongqing/index.html, dashboard → Chinese filename)
9. Statistics consistent (9 books/282+ pages/9 dashboards)
10. All economic data cites sources inline
11. Zero legacy sidebar format remnants (<h3>目录</h3>)
12. All page titles follow pattern: "序号、标题 — 重庆产业全景分析与未来展望"

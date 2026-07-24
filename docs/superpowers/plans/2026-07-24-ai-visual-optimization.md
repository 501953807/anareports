# AI影像看板+书籍 2026-07 数据校准与内容深化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement task-by-task.

**Goal:** Phase 1 — Optimize the panoramic dashboard HTML with 2026-07 data, new sections, and business annotations. Phase 2 (separate spec) — Calibrate all 25 book chapters to match dashboard data.

**Architecture:** Single-file HTML dashboard (zero layout changes), 12 existing sections preserved, data refreshed, 3 new modules added, 5 new charts. Book chapters optimized in a separate phase after dashboard approval.

**Tech Stack:** HTML5, CSS3 (existing variables), ECharts 5.5.0 (CDN), Font Awesome 6.5.1 (CDN). No new dependencies.

## Global Constraints

- **Zero layout/architecture changes**: The dashboard's 12-section structure, dark theme (`--bg:#0b1120`), navigation anchors, and CSS variable system are frozen.
- **Data freshness**: All data points must be annotated with `2026-07` collection timestamp and source type (`[实测]`/`[行业]`/`[推演]`).
- **Source file**: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html` — edit in place, no duplicates.
- **Book constraint**: Core thesis and Level-1 outline of ai-visual-production/index.html frozen.
- **No other files touched**: Only the dashboard HTML and its corresponding book directory.

---

## Phase 1: Dashboard Optimization

### Task 1: Data Audit — Inventory all existing data points and flag issues

**Files:**
- Read: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html` (full file)

**Interfaces:**
- Produces: A structured list of every data point in the dashboard, categorized by section, with flags for: outdated pricing, version inaccuracies, internal contradictions, missing source types.

**Steps:**

- [ ] **Step 1: Extract all data points from the dashboard**

Read the full dashboard HTML. Create a structured inventory of every numeric value, tool name, price, rating, market figure, and claim. Organize by the 12 existing sections:

1. 工具矩阵 (lines 94-140): Tool comparison tables (image gen, video gen, 3D, music)
2. 制作产线 (lines 142-185): Production pipeline cost/time table
3. 市场分析 (lines 187-208): Market size trend chart, AI content share chart, platform growth table
4. 性价比矩阵 (lines 210-230): Quadrant scatter, radar chart, free alternative table
5. 提示词工程 (lines 232-266): Prompt framework, style recipes, before/after case
6. 潮玩IP案例 (lines 268-292): IP comparison table, AI design workflow steps
7. 动画短片案例 (lines 294-320): Traditional vs AI cost chart, tool chain diagram
8. 3D建模工具 (lines 322-347): 3D tool comparison table, prototype workflow steps
9. 音乐音效工具 (lines 349-377): Music tool comparison, audio layer diagram
10. 工作流自动化 (lines 379-419): ComfyUI flow, n8n vs Make vs Zapier table
11. 多学派交叉 (lines 421-446): 5 school interpretations
12. 引申链+行动指南 (lines 448-503): 4 divergence chains, 3 action card categories

- [ ] **Step 2: Flag each data point for verification status**

For each data point, assign one of these flags:
- `OK`: Current, verified, correctly sourced
- `PRICE_CHECK`: Pricing may have changed — needs 2026-07 verification
- `VERSION_CHECK`: Tool version may be wrong (e.g., MJ v7 doesn't exist yet, current is v6.1/v7 beta)
- `CONTRADICTION`: Value conflicts with another section or known fact
- `MISSING_SOURCE`: No data source annotation
- `STALE_DATA`: Market/revenue figures likely outdated
- `SUBJECTIVE_SCORE`: Rating like "9.5/10" without methodology

Expected findings:
- Midjourney v7 → should be v6.1 or v7 (beta as of mid-2026)
- Sora $100/mo → verify against OpenAI current pricing
- Runway Gen-3 $128/mo → verify
- Platform growth numbers (B站 +180%, YouTube +250%) → verify YoY
- Market size $85亿 → cross-reference with Gartner 2026
- IP revenue figures (Labubu $2亿+, Molly $1.5亿+) → verify

- [ ] **Step 3: Document the audit results**

Create an inline comment block at the top of the HTML (before `<!-- ===== COVER ===== -->`) with a `<!-- DATA AUDIT -->` marker containing the full inventory. This serves as the changelog anchor.

### Task 2: Refresh all tool pricing and specifications to 2026-07

**Files:**
- Modify: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Interfaces:**
- Consumes: Data audit results from Task 1
- Produces: Updated tool tables with verified 2026-07 pricing, correct version numbers, added `[来源]` tags

**Steps:**

- [ ] **Step 1: Update Image Generation tool table (lines 97-111)**

Replace all tool names, versions, prices, and ratings with 2026-07 verified data. Add a `最后更新` column with `2026-07`. Add source type tags:

```html
<thead><tr><th>工具</th><th>类型</th><th>价格(2026-07)</th><th>图像质量</th><th>文本理解</th><th>可控性</th><th>免费额度</th><th>来源</th><th>数据来源类型</th></tr></thead>
<tbody>
<tr><td><strong>Midjourney v6.1 / v7(beta)</strong></td><td>云端</td><td><span class="paid-badge">$10/$30/$60/月</span></td><td>9.5/10</td><td>9.5/10</td><td>7/10</td><td>无</td><td>Midjourney官网 2026-07</td><td>[行业]</td></tr>
...
</tbody>
```

Apply same pattern to all 10 image generation tools.

- [ ] **Step 2: Update Video Generation tool table (lines 114-124)**

Verify and update: Runway Gen-3 Alpha pricing, Kling 2.0 capabilities, Pika 2.0+, Luma 1.5+, Sora pricing, Haiper updates. Add `最后更新` column.

- [ ] **Step 3: Update 3D Generation tool table (lines 127-137)**

Verify Meshy, CSM, Luma AI 3D, Tripo, Blender AI plugin pricing and capabilities.

- [ ] **Step 4: Update Music/SFX tool table (lines 127-137 continued)**

Verify Suno v4+/v5, Udio, ElevenLabs, AIVA pricing.

- [ ] **Step 5: Update production pipeline cost table (lines 163-173)**

Refresh cost figures for each production stage based on current free/paid tool pricing.

- [ ] **Step 6: Update n8n vs Make vs Zapier comparison (lines 401-410)**

Verify current pricing tiers and free quotas.

### Task 3: Update market data and charts to 2026-07

**Files:**
- Modify: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Interfaces:**
- Consumes: Market research data (Statista 2026, Gartner 2026Q2, IDC)
- Produces: Updated chart data arrays and market tables with 2026 data points

**Steps:**

- [ ] **Step 1: Update cover hero stats (lines 84-90)**

Refresh the 5 cover statistics with 2026-07 figures:
- Tool coverage count
- Analysis板块 count
- ECharts chart count (will increase)
- 2026 global market size
- 2026 growth rate

- [ ] **Step 2: Update market trend chart data (line 556)**

Extend the market trend line chart to include 2026 actual data point and 2027-2031 projections. Update source attribution.

- [ ] **Step 3: Update AI content share pie chart (line 572)**

Refresh the percentage breakdown based on 2026 creator economy data.

- [ ] **Step 4: Update platform growth table (lines 199-207)**

Refresh B站, YouTube, 抖音/TikTok, 小红书 AI content growth rates with 2026 data.

- [ ] **Step 5: Update scatter plot quadrant data (lines 595-610)**

Reposition all tool data points based on refreshed quality scores and 2026 pricing.

### Task 4: Add source type tags and data freshness annotations throughout

**Files:**
- Modify: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Steps:**

- [ ] **Step 1: Add CSS for source type badges**

Add badge styles in the `<style>` block:

```css
.tag-source { display: inline-block; padding: 1px 5px; border-radius: 3px; font-size: 9px; font-weight: 600; margin: 0 2px; }
.tag-measured { background: rgba(16,185,129,.2); color: #10b981; }  /* [实测] */
.tag-industry { background: rgba(6,182,212,.2); color: #06b6d4; }   /* [行业] */
.tag-modeled { background: rgba(245,158,11,.2); color: #f59e0b; }   /* [推演] */
```

- [ ] **Step 2: Add source type column to all data tables**

Every table gets a `数据来源类型` column with appropriate tag.

- [ ] **Step 3: Add data freshness banner under each chart**

After each chart container, add a small note:
```html
<p style="font-size:10px;color:var(--text3);text-align:center;margin-top:2px">数据截至 2026-07 | 来源：XXX | 下次更新：2026-10</p>
```

### Task 5: Add business interpretation, risk warnings, and indicator glossary to each section

**Files:**
- Modify: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Steps:**

- [ ] **Step 1: Add a reusable "解读" block template**

Add a new CSS class for business interpretation blocks:

```css
.interpretation-box { background: rgba(139,92,246,.04); border: 1px dashed var(--purple); border-radius: 6px; padding: 10px 14px; margin: 12px 0; font-size: 12px; color: var(--text2); line-height: 1.7; }
.interpretation-box .interp-title { font-weight: 600; color: var(--purple); margin-bottom: 4px; }
.risk-box { background: rgba(239,68,68,.04); border: 1px solid rgba(239,68,68,.3); border-radius: 6px; padding: 10px 14px; margin: 12px 0; font-size: 11px; color: var(--text2); }
.risk-box .risk-title { font-weight: 600; color: var(--red); margin-bottom: 4px; }
.glossary-box { background: rgba(6,182,212,.04); border: 1px solid rgba(6,182,212,.2); border-radius: 6px; padding: 10px 14px; margin: 12px 0; font-size: 11px; color: var(--text2); }
```

- [ ] **Step 2: Add interpretation + risk + glossary blocks to each of the 12 sections**

For each section, add 1-3 blocks:
- 业务解读 (Business Interpretation): What does this data mean for creators/businesses?
- 风险提示 (Risk Warning): Data staleness, tool iteration risk, copyright compliance
- 指标释义 (Indicator Glossary): How are scores calculated? What does "quality 9.5/10" mean?

### Task 6: Add 5 new charts and 1 new section

**Files:**
- Modify: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Steps:**

- [ ] **Step 1: Add new Section 13 — "AI影像版权与合规指南"**

Insert after the existing Section 12. Content:
- Global AI copyright landscape table (US/EU/CN/JP status)
- Commercial use risk matrix (tool by tool)
- Platform AI-content labeling requirements (B站/YouTube/抖音/小红书)
- Brief legal interpretation from multiple school perspectives

- [ ] **Step 2: Add Chart — Tool release velocity timeline**

New ECharts bar chart showing how frequently each vendor releases major versions (Midjourney: ~6mo, SD: ~3mo, Runway: ~4mo, etc.)

- [ ] **Step 3: Add Chart — China vs Global AI video market comparison**

Dual-axis line chart comparing Chinese vs global market dynamics.

- [ ] **Step 4: Add Chart — Creator income distribution**

Pie/histogram showing income brackets for AI content creators.

- [ ] **Step 5: Add Chart — Free vs Paid long-term cost curve**

Line chart showing cumulative cost over 1/3/5 years for free-only vs hybrid vs fully-paid workflows.

- [ ] **Step 6: Add Chart — Copyright risk heatmap**

Matrix chart showing each tool's commercial copyright risk level.

### Task 7: Add data version history footer and update page footer

**Files:**
- Modify: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Steps:**

- [ ] **Step 1: Replace the footer (lines 507-510)**

Replace simple footer with a structured data version panel:

```html
<div class="footer">
  <p>AI视频图像设计全景看板 v3.0 — 2026-07 全面校准版</p>
  <div class="data-note" style="margin-top:12px">
    <strong>版本历史：</strong>
    <p>v1.0 (2025-06) → 初始版本 | v2.0 (2025-12) → 工具扩展 | v3.0 (2026-07) → 全面数据校准 + 新增版权合规板块 + 5个新图表</p>
    <p style="margin-top:4px"><strong>数据来源：</strong>Statista 2026Q2, Gartner AI Market Forecast 2026, IDC Worldwide AI Spending Guide 2026, 各厂商官网定价, 社区实测数据</p>
    <p><strong>更新频率：</strong>每季度一次全面校准（1月/4月/7月/10月）</p>
  </div>
</div>
```

### Task 8: Generate modification detail清单

**Files:**
- Create: `docs/superpowers/reports/ai-visual-dashboard-changelog.md`

**Steps:**

- [ ] **Step 1: Write the detailed changelog**

Create a markdown document listing every change made, organized by section:

```markdown
# AI视频图像设计全景看板 — 修改明细清单 (v2.0 → v3.0)

## 数据层整改
| 位置 | 原有问题 | 优化方案 |
|------|----------|----------|
| 板块一表1行1 | MJ标注v7不存在 | 改为v6.1/v7(beta) |
| ... | ... | ... |

## 新增模块
| 模块 | 说明 | 位置 |
|------|------|------|
| 版权合规指南 | 全新板块13 | 原板块12之后 |
| ... | ... | ... |

## 新增图表
| 图表 | 类型 | 说明 |
|------|------|------|
| 工具发布速度 | 柱状图 | 各厂商版本迭代频率 |
| ... | ... | ... |
```

### Task 9: Final QA — consistency check across all 12 sections

**Files:**
- Read: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html` (final version)

**Steps:**

- [ ] **Step 1: Cross-section data consistency check**

Verify that every number appears only once with consistent values:
- Market size figures match across all mentions
- Tool prices are identical in every table where the tool appears
- Rating scales are consistent (all out of 10)

- [ ] **Step 2: Visual regression check**

Open the file in browser and verify:
- Layout unchanged (same 12 sections in same order)
- Colors/theme unchanged
- Charts render correctly
- Navigation links work
- Mobile responsive behavior intact

- [ ] **Step 3: Source annotation completeness check**

Every data point has: source name, date (2026-07), and type tag ([实测]/[行业]/[推演])

---

## Phase 2: Book Calibration (deferred until Phase 1 approved)

*Detailed tasks will be created in a follow-up plan after dashboard v3.0 is confirmed.*

### Scope summary for Phase 2:

**A级 (深度重构, 10章):** 01, 04, 05, 08, 10, 12, 17, 20, 23, 24
- Full data alignment with dashboard v3.0
- Multi-school analysis deepening
- Case study expansion
- Strategic recommendation enhancement

**B级 (逻辑梳理, 10章):** 02, 03, 06, 07, 09, 11, 13, 15, 18, 21
- Data consistency fix
- Logical transition补全
- Format unification

**C级 (最小改动, 5章):** 14, 16, 19, 22, 25
- Data calibration only
- Error correction

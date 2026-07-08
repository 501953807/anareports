# 中华古典学术理论全景书 — 重设计

## 问题诊断

当前 `traditional-academics/`（32页）存在以下不足：

1. **内容深度不够**：每章内容偏概述性，缺乏由浅入深的层次递进
2. **排版风格不统一**：赛博朋克深色主题不适合长篇阅读，不符合纸质书体验
3. **图文结合不足**：缺少高质量SVG插图和信息图，读者难以直观理解抽象概念
4. **章节孤立**：六大部分之间缺乏交叉引用，读者无法融会贯通
5. **缺少互动元素**：没有延伸阅读、实践练习和思考引导

## 设计目标

将全书改造为**通俗易懂、图文并茂、由浅入深**的纸质书级电子书体验，同时保留ECharts数据可视化优势。

## 设计方案

### 一、排版风格改造

#### 1.1 主题切换

新增双主题系统（默认浅色纸质书风格，可选深色模式）：

```css
:root {
  /* 纸质书浅色主题（默认） */
  --bg: #FAF9F6;           /* 米白纸张色 */
  --surface: #FFFFFF;      /* 纯白卡片 */
  --surface2: #F5F4F0;     /* 浅灰背景 */
  --border: #E8E6E1;       /* 柔和边框 */
  --text: #2C2C2C;         /* 深灰正文 */
  --text2: #666666;        /* 次要文字 */
  --accent: #B8860B;       /* 金色点缀 */
  --link: #1A5276;         /* 深蓝链接 */
}

[data-theme="dark"] {
  /* 深色模式（可选切换） */
  --bg: #1a1d27;
  --surface: #232733;
  --text: #e2e8f0;
  --text2: #94a3b8;
}
```

#### 1.2 字体与间距

```css
body {
  font-family: 'Noto Serif SC', 'Source Han Serif CN', serif; /* 衬线体 */
  background: var(--bg);
  color: var(--text);
  line-height: 1.9;          /* 宽松行高 */
  font-size: 17px;           /* 适读字号 */
  letter-spacing: 0.02em;    /* 字间距 */
  max-width: 720px;          /* 单栏阅读宽度 */
  margin: 0 auto;            /* 居中排版 */
}
```

#### 1.3 章节标题层级

```css
h1.section-title { font-size: 28px; font-weight: 700; margin: 48px 0 24px; }
h2.section-subtitle { font-size: 20px; font-weight: 600; margin: 36px 0 16px; }
h3 { font-size: 16px; font-weight: 600; margin: 24px 0 12px; }
```

### 二、内容结构重写 — 五段式模板

每章统一采用以下结构：

| 段落 | 标题 | 内容要求 | 篇幅占比 |
|------|------|----------|----------|
| 1 | **故事引入** | 以历史典故、生活场景或现实案例开篇，引发兴趣 | 15% |
| 2 | **概念解析** | 用通俗语言解释核心概念，配SVG插图说明 | 25% |
| 3 | **深入理解** | 理论深化，含ECharts图表、数据表格、对比分析 | 25% |
| 4 | **实践应用** | 现代应用场景、实操方法、生活联系 | 20% |
| 5 | **延伸阅读** | 跨章节关联、推荐阅读、思考题 | 15% |

#### 2.1 每章标准HTML骨架

```html
<main class="content">
  <article class="chapter">
    <!-- 章节元信息 -->
    <header class="chapter-header">
      <span class="chapter-part">第一部分</span>
      <h1 class="section-title">八卦起源与演变概述</h1>
      <p class="chapter-intro">一句话概括本章核心价值</p>
    </header>

    <!-- 段落1：故事引入 -->
    <section class="chapter-section">
      <h2 class="section-subtitle">一、从一则历史故事说起</h2>
      <p>...</p>
      <div class="illustration-svg">[SVG插图]</div>
    </section>

    <!-- 段落2：概念解析 -->
    <section class="chapter-section">
      <h2 class="section-subtitle">二、核心概念详解</h2>
      <table class="data-table">...</table>
      <div class="illustration-svg">[SVG插图]</div>
    </section>

    <!-- 段落3：深入理解 -->
    <section class="chapter-section">
      <h2 class="section-subtitle">三、深入理解</h2>
      <div class="chart-container" id="chart-xxx"></div>
      <script>/* ECharts */</script>
    </section>

    <!-- 段落4：实践应用 -->
    <section class="chapter-section">
      <h2 class="section-subtitle">四、在现代生活中的应用</h2>
      <div class="case-box">[真实案例]</div>
      <ol class="steps-list">[实操步骤]</ol>
    </section>

    <!-- 段落5：延伸阅读 -->
    <section class="chapter-section chapter-extensions">
      <h2 class="section-subtitle">五、延伸阅读与思考</h2>
      <div class="cross-ref-grid">
        <a href="../阴阳五行/06-yinyang-benyuan.html" class="cross-ref-card">
          <i class="fas fa-link"></i>
          <span>与阴阳五行理论的关联</span>
        </a>
        <!-- 更多交叉引用 -->
      </div>
      <div class="reflection-questions">
        <h3>思考题</h3>
        <ul><li>...</li></ul>
      </div>
    </section>
  </article>
</main>
```

### 三、SVG插图系统

#### 3.1 插图清单

| 章节 | SVG插图类型 | 数量 | 说明 |
|------|------------|------|------|
| 八卦(01-05) | 先天/后天八卦方位图 | 2 | 彩色SVG，标注方位和卦名 |
| 八卦(01-05) | 八卦取象比类图 | 1 | 八宫卦象关系网络图 |
| 阴阳五行(06-11) | 阴阳消长循环图 | 1 | 动态SVG展示阴阳流转 |
| 阴阳五行(06-11) | 五行生克循环图 | 1 | 相生顺时针、相克内五角 |
| 阴阳五行(06-11) | 天干地支罗盘图 | 1 | 360度罗盘布局 |
| 中医(12-17) | 人体经络走向图 | 2 | 十二经脉全身标注 |
| 中医(12-17) | 五脏对应关系图 | 1 | 心肝脾肺肾与五行映射 |
| 中医(12-17) | 气血运行图 | 1 | 子午流注时间轴 |
| 易经(18-22) | 六十四卦方圆图 | 1 | 伏羲/文王卦序排列 |
| 易经(18-22) | 卦变关系树图 | 1 | 八宫卦变体系 |
| 道家(23-27) | 道统传承谱系图 | 1 | 老子→庄子→列子等 |
| 道家(23-27) | 道法自然概念图 | 1 | 道-德-仁-义-礼层级 |
| 儒家(28-31) | 儒家传承谱系图 | 1 | 孔子→孟子→朱熹→王阳明 |
| 儒家(28-31) | 五常与五经关系图 | 1 | 仁义礼智信与经典对应 |

#### 3.2 SVG设计规范

```html
<!-- 插图容器 -->
<div class="illustration-svg">
  <svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
    <!-- 矢量图形 -->
  </svg>
  <figcaption class="illustration-caption">图X-X [图名] — 简要说明</figcaption>
</div>

/* CSS */
.illustration-svg {
  text-align: center;
  margin: 32px 0;
  padding: 20px;
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border);
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
}
```

### 四、跨章节关联网络

#### 4.1 关联图谱

```
八卦(01-05) ──┬──→ 阴阳五行(06-11)
             ├──→ 中医基础(12-17)
             └──→ 易经体系(18-22)

阴阳五行(06-11) ──┬──→ 中医基础(12-17)
                  ├──→ 道家理论(23-27)
                  └──→ 儒家理论(28-31)

中医基础(12-17) ──┬──→ 道家理论(23-27)
                  └──→ 易经体系(18-22)

道家理论(23-27) ──┬──→ 儒家理论(28-31)
                  └──→ 易经体系(18-22)
```

#### 4.2 交叉引用卡片样式

```html
<div class="cross-ref-grid">
  <a href="../阴阳五行/06-yinyang-benyuan.html" class="cross-ref-card">
    <div class="cross-ref-icon">☯</div>
    <div class="cross-ref-info">
      <strong>阴阳概念本源</strong>
      <span>八卦的阴阳爻是阴阳思想的符号表达</span>
    </div>
  </a>
</div>

/* CSS */
.cross-ref-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.cross-ref-icon { font-size: 24px; }
.cross-ref-info strong { display: block; font-size: 14px; color: var(--link); }
.cross-ref-info span { font-size: 12px; color: var(--text2); }
```

### 五、新增组件

#### 5.1 思考题区块

```html
<div class="reflection-questions">
  <h3><i class="fas fa-question-circle"></i> 思考题</h3>
  <ol>
    <li>你能在日常生活找到哪些阴阳平衡的例子？</li>
    <li>五行相生相克与你所学的系统论有什么相似之处？</li>
  </ol>
</div>
```

#### 5.2 延伸阅读区块

```html
<div class="further-reading">
  <h3><i class="fas fa-book-open"></i> 进一步阅读</h3>
  <ul>
    <li>《周易译注》黄寿祺、张善文，上海古籍出版社</li>
    <li>《中国哲学简史》冯友兰，北京大学出版社</li>
  </ul>
</div>
```

#### 5.3 关键概念高亮

```html
<p>
  <strong class="key-term">阴阳</strong>
  <span class="key-term-def" title="阴阳是中国古典哲学的核心概念...">ℹ️</span>
  是宇宙间两种最基本的力量...
</p>
```

### 六、文件变更范围

| 文件 | 操作 | 改动内容 |
|------|------|----------|
| `common/css/book.css` | 重写 | 新增纸质书浅色主题 + 深色模式切换 |
| `index.html` | 重写 | 封面改为纸质书风格，新增意境封面图 |
| `01-05` (八卦) | 重写 | 五段式结构 + SVG插图 + 跨章节关联 |
| `06-11` (阴阳五行) | 重写 | 同上 |
| `12-17` (中医) | 重写 | 同上 + 新增经络SVG图 |
| `18-22` (易经) | 重写 | 同上 + 新增卦序SVG图 |
| `23-27` (道家) | 重写 | 同上 + 新增道统谱系SVG图 |
| `28-31` (儒家) | 重写 | 同上 + 新增儒家谱系SVG图 |
| `common/js/theme-toggle.js` | 新建 | 主题切换功能（浅色↔深色） |

### 七、技术实现要点

1. **主题切换**：通过 `<html data-theme="light">` / `<html data-theme="dark">` 控制CSS变量
2. **响应式**：PC端720px单栏，平板端自适应，移动端自动适配
3. **打印友好**：新增 `@media print` 样式，支持PDF导出
4. **性能**：SVG内联（无外部请求），ECharts按需加载
5. **可访问性**：ARIA标签、键盘导航、屏幕阅读器支持

## 验证清单

1. 所有页面使用浅色纸质书主题（默认）
2. 每章严格遵循五段式结构
3. 每章至少2张SVG插图
4. 每章底部有跨章节关联卡片（≥2个）
5. 每章有思考题（≥2道）
6. 每章有延伸阅读推荐（≥2本）
7. ECharts图表保留并融入"深入理解"段落
8. 主题切换功能正常工作
9. 打印/PDF导出效果良好
10. 所有链接正确

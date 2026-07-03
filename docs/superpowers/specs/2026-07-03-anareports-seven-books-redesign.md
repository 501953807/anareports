# AnaReports 七本书多页HTML站点 redesign 设计文档

> **目标：** 将7个单文件HTML看板拆分为多页可查阅的"书籍"形式，基于现有内容持续深化到极限
> **风格：** 赛博朋克深色主题，统一视觉体系
> **受众：** 希望深入查阅各行业全景分析的读者

---

## 一、项目概述

### 1.1 背景
现有7个HTML看板均为单文件架构（内嵌CSS+JS+ECharts），文件体积庞大（50-130KB），内容密度高但不可持续深化。需要将每个看板拆分为多页HTML站点，形成可翻阅的"书籍"形式。

### 1.2 范围
- **7个看板全部转换**：创作者经济、地下钱庄、广州吃喝玩乐、医药产业、新能源汽车、中日经济周期、智能设备
- **每个看板拆分为30-50+页**：基于现有内容持续深化
- **统一导航体系**：共享公共资源，统一视觉风格
- **持续深化到极限**：每个子章节补充数据、案例、操作步骤、历史背景、政策分析

### 1.3 约束
- 纯静态HTML站点，可直接部署到GitHub Pages
- 保持赛博朋克深色主题
- 响应式设计，适配手机端
- 基于现有内容深化，不推倒重来

---

## 二、目录结构设计

### 2.1 顶层结构

```
AnaReports/
├── index.html                    # 总入口：七本书封面墙
├── common/                       # 公共资源
│   ├── css/
│   │   └── book.css              # 统一样式
│   ├── js/
│   │   ├── echarts.inline.js     # ECharts 5.5.0
│   │   └── navigation.js         # 统一导航逻辑
│   └── fonts/                    # （可选）字体缓存
├── creators/                     # 书1：创作者经济（30-50+页）
│   ├── index.html                # 总览 + 目录
│   ├── 01-overview.html          # 第一章
│   └── ...
├── money-laundering/             # 书2：地下钱庄（30-50+页）
│   ├── index.html
│   └── ...
├── guangzhou/                    # 书3：广州吃喝玩乐+供应链
│   ├── index.html
│   └── ...
├── pharma/                       # 书4：医药产业
│   ├── index.html
│   └── ...
├── ev-motorcycle/                # 书5：新能源汽车
│   ├── index.html
│   └── ...
├── china-japan/                  # 书6：中日经济周期
│   ├── index.html
│   └── ...
└── smart-devices/                # 书7：智能手环与药盒
    ├── index.html
    └── ...
```

### 2.2 每个看板内部结构

```
creators/
├── index.html                    # 封面 + 总目录
├── 01-overview.html              # 第一章：全局概览
├── 02-professions.html           # 第二章：十大赚钱行当
├── 03-platforms-video.html       # 第三章：视频类平台
├── 04-platforms-text.html        # 第四章：图文类平台
├── 05-platforms-audio.html       # 第五章：音频类平台
├── 06-platforms-live.html        # 第六章：直播类平台
├── 07-platforms-ecommerce.html   # 第七章：电商/技能类平台
├── 08-monetization-ads.html      # 第八章：广告分成
├── 09-monetization-brand.html    # 第九章：品牌赞助
├── 10-monetization-subscribe.html# 第十章：付费订阅
├── 11-monetization-tip.html      # 第十一章：打赏礼物
├── 12-monetization-ecommerce.html# 第十二章：电商带货
├── 13-monetization-affiliate.html# 第十三章：联盟营销
├── 14-monetization-knowledge.html# 第十四章：知识付费
├── 15-monetization-ip.html       # 第十五章：IP授权
├── 16-income-analysis.html       # 第十六章：收入数据分析
├── 17-roadmap-beginner.html      # 第十七章：新手起步指南
├── 18-roadmap-intermediate.html  # 第十八章：进阶运营
├── 19-roadmap-advanced.html      # 第十九章：规模化运营
├── 20-risks-guide.html           # 第二十章：避坑指南
├── 21-future-trends.html         # 第二十一章：未来趋势
└── 22-case-studies.html          # 第二十二章：典型案例
```

---

## 三、页面设计规范

### 3.1 页面结构

每个内页包含：
1. **顶部导航栏**：
   - 左侧：书名 + 章节标题
   - 右侧：目录按钮 + 上一节/下一节导航
2. **左侧目录面板**（可折叠）：
   - 完整章节列表
   - 当前章节高亮
   - 可展开/收起子章节
3. **主体内容区**：
   - 章节标题
   - 正文内容（表格、列表、卡片等）
   - ECharts 图表（1-3个/页）
   - 案例框、数据框、提示框
4. **底部页脚**：
   - 页码导航（← 上一章 | 目录 | 下一章 →）
   - 返回总入口链接

### 3.2 内容组件

- **数据卡片**：核心指标展示
- **对比表格**：平台/方法/数据对比
- **案例框**：真实人物/企业案例
- **操作步骤**：编号步骤指南
- **提示框**：注意事项、风险提示
- **时间线**：历史事件/发展历程
- **流程图**：操作路径/资金链路
- **ECharts 图表**：柱状图、饼图、折线图、雷达图等

### 3.3 视觉规范

- **背景色**：#0a0e17（赛博朋克深色）
- **强调色**：青色 #06b6d4、紫色 #8b5cf6、红色 #ef4444、绿色 #10b981、橙色 #f59e0b
- **字体**：Noto Sans SC
- **图标**：Font Awesome 6.5.1
- **图表**：Apache ECharts 5.5.0

---

## 四、深化策略

### 4.1 深化维度

每个子章节从以下维度持续深化：

1. **方向性深化**：宏观格局、历史脉络、政策分析、国际比较
2. **操作性深化**：具体使用指南、注册步骤、操作流程、技巧方法
3. **数据性深化**：市场规模、收入分布、平台对比、增长趋势
4. **案例性深化**：真实人物/企业案例、成功与失败故事
5. **前瞻性深化**：趋势预测、风险提示、机会窗口

### 4.2 深化标准

- 每个子章节至少包含：核心概念解释 + 数据支撑 + 案例说明 + 操作指南
- 每个子章节至少包含1-3个ECharts图表
- 每个子章节至少引用3-5个真实数据源
- 每个子章节至少包含2-3个真实案例

### 4.3 终止条件

深化到以下情况时停止：
- 无法找到更多可靠数据来源
- 无法找到更多有意义的案例
- 内容开始出现重复或冗余
- 用户确认"到头了"

---

## 五、实施计划

### 5.1 并行推进策略

7个看板并行推进，每个看板按以下步骤执行：

1. **分析当前单文件** → 提取所有章节板块
2. **设计目录结构** → 确定拆分方案和页码
3. **创建目录和骨架** → 建立 `common/` 目录和各看板子目录
4. **拆分现有内容** → 将当前内容分配到各页
5. **逐页深化** → 在每个子章节下持续深化
6. **统一导航** → 添加顶部导航栏、左侧目录、底部页脚
7. **测试验证** → 确认所有链接可访问、图表正常渲染

### 5.2 优先级

建议按以下顺序推进（从最简单/最成熟开始）：

1. 创作者经济（最新完成，结构最清晰）
2. 地下钱庄（已完成v2.0重写）
3. 中日经济周期
4. 医药产业
5. 智能设备
6. 广州吃喝玩乐
7. 新能源汽车（文件最大，136KB，可能需要最多工作）

### 5.3 工作量估算

- 每个看板：30-50页 × 每页深化 = 约2-4小时/页
- 总计：7个看板 × 40页 × 3小时 = 约840小时
- 建议分批推进，每完成一个看板即部署测试

---

## 六、技术细节

### 6.1 公共资源共享

`common/` 目录存放所有看板共享的资源：
- `css/book.css`：统一样式表
- `js/echarts.inline.js`：ECharts 5.5.0
- `js/navigation.js`：统一导航逻辑（目录展开/折叠、上一页/下一页、面包屑）

### 6.2 页面模板

每个内页基于统一HTML模板：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[章节标题] - [书名]</title>
  <link rel="stylesheet" href="../common/css/book.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <!-- 顶部导航栏 -->
  <nav class="top-nav">...</nav>
  
  <!-- 左侧目录面板 -->
  <aside class="sidebar">...</aside>
  
  <!-- 主体内容 -->
  <main class="content">...</main>
  
  <!-- 底部页脚 -->
  <footer class="page-footer">...</footer>
  
  <script src="../common/js/echarts.inline.js"></script>
  <script src="../common/js/navigation.js"></script>
  <script src="[页面专属JS]"></script>
</body>
</html>
```

### 6.3 响应式断点

- Desktop: > 1200px
- Tablet: 768px - 1200px
- Mobile Large: 480px - 768px
- Mobile Small: < 480px

---

## 七、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 内容深化后页面数量过多 | 管理复杂 | 每个看板独立目录，清晰命名 |
| 公共资源维护困难 | 样式不一致 | 统一CSS变量，集中管理 |
| 深化到极限的判断主观 | 质量不一 | 设定明确的深化标准 |
| 工作量过大 | 进度延误 | 分批推进，每完成一个即部署 |
| 图表渲染性能 | 加载慢 | 按需加载ECharts模块 |

---

## 八、成功标准

1. 7个看板全部转换为多页HTML站点
2. 每个看板30-50+页，内容深化到极限
3. 统一的导航体系和视觉风格
4. 所有链接可正常访问，图表正常渲染
5. 响应式设计，手机端可正常浏览
6. 可直接部署到GitHub Pages

---
name: ai-visual-production-design
description: Design for new AI video/image production book and kanban in second group (academic)
metadata:
  type: project
---

# AI影像创作实战指南 — 看板和书籍设计

## 概述

在 index.html 第二辑·学术与文化研究下新增一个条目：AI视频图像设计。包含一个看板（全景分析）和一个书籍（教学实战）。

## 文件清单

### 书籍 (`ai-visual-production/`)
- `index.html` — 封面+目录（参考 chongqing/index.html 结构）
- `01-tool-overview.html` — 第1章：AI影像工具全景图谱
- `02-prompt-engineering.html` — 第2章：提示词工程基础
- `03-env-setup.html` — 第3章：环境搭建与免费工具配置
- `04-character-design.html` — 第4章：潮玩IP角色设计理念
- `05-character-views.html` — 第5章：AI生成角色三视图
- `06-expression-props.html` — 第6章：表情集与道具设计
- `07-character-output.html` — 第7章：设计稿整合输出
- `08-short-film-plan.html` — 第8章：动画短片策划
- `09-scene-gen.html` — 第9章：场景与角色图像生成
- `10-video-gen.html` — 第10章：从图像到动画的视频生成
- `11-post-production.html` — 第11章：后期合成与音效
- `12-publishing.html` — 第12章：成片输出与发布
- `13-commercial-apps.html` — 第13章：商业应用场景
- `14-monetization.html` — 第14章：内容变现路径

共14章 + 封面 = 15个页面，目标35-40页内容。

### 看板 (root level)
`AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

### BOOK_DATA 条目
```javascript
{
  name: "《AI影像创作实战指南：从工具选型到潮玩IP角色设计与完整动画短片》",
  shortName: "AI影像创作",
  desc: "AI图像/视频工具全景对比、提示词工程、潮玩IP角色设计稿实战、完整动画短片制作全流程教学。",
  group: "academic", icon: "fa-wand-magic-sparkles", color: "purple",
  pages: 38, charts: 15,
  tags: ["AI影像", "角色设计", "动画短片"],
  highlights: [
    { label: "工具", value: "15+" },
    { label: "图表", value: "15" },
    { label: "实战案例", value: "2个" }
  ],
  bookUrl: "ai-visual-production/index.html",
  kanbanUrl: "AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html"
}
```

## 视觉风格约定

### 书籍
- 使用 common/css/book.css 作为基础样式
- 使用 common/js/echarts.inline.js 做图表
- 使用 common/js/navigation.js 做上下页导航
- nav-home 链接指向 `../index.html`
- 封面使用径向渐变背景 + 数据统计卡片
- 每章包含：多学派交叉解读、案例深挖、发散引申链

### 看板
- 暗色赛博朋克主题（--bg, --surface, --card, --cyan, --purple 等 CSS 变量）
- ECharts 图表内联
- 顶部 sticky nav + 品牌标识
- 各板块用 section-title 分隔

## 核心内容要求

### AI工具选型原则
1. **效果优先**：选择当前市场上效果最好的工具
2. **性价比**：优先推荐免费或低成本工具
3. **最小工具集**：用最少的工具完成所有目标
4. **最新版本**：使用2024-2026年最新工具版本

### 图像生成案例：潮玩IP角色设计稿
- 皮克斯/迪士尼风格的现代卡通角色
- 完整产品设计稿：三视图（正面/侧面/背面）、表情集、道具设计
- 类似拉布布/迪士尼公仔的潮玩产品定位

### 视频生成案例：完整动画短片
- 皮克斯风格的现代卡通动画短片
- 约10-15分钟完整短片（分章节展示制作流程）
- 从剧本→分镜→角色设计→场景→动画→后期的全流程

### 工具推荐方向（需根据实际最新情况调整）
- **图像生成**：Midjourney v7 / Flux / 通义万相（免费）/ Stable Diffusion 3
- **视频生成**：可灵Kling（免费额度）/ Runway Gen-3 / Pika 1.5 / Luma Dream Machine
- **工作流**：ComfyUI（开源免费）

## 多学派交叉解读模板

每个主要章节必须包含经济学流派交叉分析，参考现有书籍模式：
- 古典经济学：分工效率、比较优势
- 凯恩斯主义：有效需求、乘数效应
- 马克思主义政治经济学：生产力变革、劳动价值论
- 新制度经济学：交易成本、制度创新
- 行为/演化经济学：认知重构、路径依赖

## 关键约束

- 所有工具必须是2024-2026年最新版本
- 教程步骤必须足够细致，零基础也能跟着操作
- 看板数据必须有真实来源支撑
- 与项目现有看板和书籍保持完全一致的排版样式
- 统一入口在 index.html 的 BOOK_DATA 中

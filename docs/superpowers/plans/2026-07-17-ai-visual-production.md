# AI影像创作实战指南 — 实现计划

> **For agentic workers:** Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 AnaReports 项目第二辑·学术与文化研究下新增AI视频图像设计看板和书籍，包含15个书籍页面+1个看板HTML+index.html集成。

**Architecture:** 遵循现有项目模式——书籍使用 common/css/book.css + echarts.inline.js + navigation.js，看板使用独立暗色赛博朋克主题。BOOK_DATA 驱动 index.html 卡片渲染。

**Tech Stack:** 纯 HTML/CSS/JS，无第三方JS库。ECharts 内联图表。Font Awesome 6.5.1 图标。

## Global Constraints

- 所有工具必须是2024-2026年最新版本，效果最好的免费或低成本工具
- 教程步骤必须足够细致，零基础用户能跟着操作
- 看板数据必须有真实来源支撑（标注数据来源）
- 与项目现有看板和书籍保持完全一致的排版样式
- 统一入口在 index.html BOOK_DATA 中
- 每个书籍章节必须包含：多学派交叉解读、案例深挖/发散引申链
- 每页文件使用 nav-home 链接指向 ../index.html
- 封面 SVG 插图风格统一（皮克斯卡通角色示例）

---

### Task 1: 创建书籍目录结构和基础文件

**Files:**
- Create: `ai-visual-production/index.html`
- Create: `ai-visual-production/01-tool-overview.html`
- Create: `ai-visual-production/02-prompt-engineering.html`
- Create: `ai-visual-production/03-env-setup.html`
- Create: `ai-visual-production/04-character-design.html`
- Create: `ai-visual-production/05-character-views.html`
- Create: `ai-visual-production/06-expression-props.html`
- Create: `ai-visual-production/07-character-output.html`
- Create: `ai-visual-production/08-short-film-plan.html`
- Create: `ai-visual-production/09-scene-gen.html`
- Create: `ai-visual-production/10-video-gen.html`
- Create: `ai-visual-production/11-post-production.html`
- Create: `ai-visual-production/12-publishing.html`
- Create: `ai-visual-production/13-commercial-apps.html`
- Create: `ai-visual-production/14-monetization.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 15个HTML页面，遵循统一模板

**Steps:**
- [ ] **Step 1: 创建 ai-visual-production/ 目录**

```bash
mkdir -p ai-visual-production
```

- [ ] **Step 2: 从 chongqing/index.html 复制书籍目录模板**

读取 `chongqing/index.html` 作为模板参考，创建 `ai-visual-production/index.html`，包含：
- 封面标题：《AI影像创作实战指南：从工具选型到潮玩IP角色设计与完整动画短片》
- 封面副标题：AI图像/视频工具全景对比 · 提示词工程 · 潮玩IP角色设计稿实战 · 完整动画短片制作全流程
- 数据统计卡片：14章 / 38页 / 15+工具 / 2个实战案例
- 太极/创意SVG封面插图（改为AI生成风格的视觉元素，如像素/神经网络抽象图）
- 目录网格：4篇结构展示
- ECharts雷达图展示各技能维度
- 引入 `../common/css/book.css`、`../common/js/echarts.inline.js`、`../common/js/navigation.js`
- footer 包含 nav-home 链接 `href="../index.html"`

- [ ] **Step 3: 创建第1章 01-tool-overview.html**

内容结构：
- 顶部nav：书名 + 章节标题 + 目录按钮 + 上一本书链接
- 侧边栏TOC：4篇完整目录
- 正文：
  - AI影像工具全景概览（数据卡片：市场规模$XX亿、增长率XX%）
  - 图像生成工具矩阵表（Midjourney v7/DALL-E 4/Stable Diffusion 3/Flux/通义万相/文心一格/KREA等，列参数：价格/免费额度/质量/易用性/输出分辨率）
  - 视频生成工具矩阵表（Runway Gen-3/Pika 1.5/Sora/可灵Kling/Luma Dream Machine/Haiper/即梦等）
  - 工作流整合工具（ComfyUI/Automatic1111/InvokeAI等）
  - 免费 vs 付费性价比雷达图
  - 多学派交叉解读（古典经济学-分工效率、马克思主义-生产力变革、新制度经济学-交易成本降低）
  - 案例深挖：Midjourney从v1到v7的进化史
  - 发散引申链

- [ ] **Step 4: 创建第2章 02-prompt-engineering.html**

内容：
- 提示词工程核心方法论（结构化提示词框架）
- 图像生成提示词模板（风格/构图/ lighting/色彩/细节层级）
- 视频生成提示词模板（镜头语言/运动描述/转场/节奏）
- 正面词/负面词词典
- 提示词优化前后对比案例
- 不同风格的提示词配方（皮克斯风/写实风/水彩风/赛博朋克/国风）
- 多学派交叉解读
- 案例深挖：一个爆款AI潮玩角色的提示词拆解

- [ ] **Step 5: 创建第3章 03-env-setup.html**

内容：
- 硬件需求评估（GPU门槛/云端替代方案）
- 免费工具配置指南（逐步截图式文字说明）：
  - 通义万相注册与使用
  - 可灵Kling免费额度使用
  - Stable Diffusion本地部署（WebUI/ComfyUI）
  - Flux本地/云端部署
- 付费工具性价比分析（Midjourney订阅vs按需付费）
- 最小工具集推荐方案（3个免费工具即可入门）
- 多学派交叉解读
- 发散引申链

- [ ] **Step 6: 创建第4-7章（潮玩IP角色设计实战）**

**04-character-design.html** — 设计理念与方法论：
- 潮玩IP角色设计原则（可爱度/辨识度/延展性/商业价值）
- 皮克斯/迪士尼风格特征分析
- 拉布布等成功IP的角色设计拆解
- 角色设计流程：概念→草图→三视图→表情→道具
- 案例深挖：Labubu的设计哲学

**05-character-views.html** — AI生成角色三视图：
- 使用AI工具生成正面/侧面/背面三视图的完整步骤
- 提示词配方：角色一致性技巧（seed控制/参考图上传/LoRA训练）
- 工具选择：Midjourney v7角色生成 / Flux角色设计 / 通义万相
- 实操演示：设计一个皮克斯风格的小熊/小狐狸角色
- 每一步的提示词、参数设置、输出结果展示
- 多学派交叉解读

**06-expression-props.html** — 表情集与道具设计：
- 角色表情集生成（喜/怒/哀/乐/惊/惧/羞涩/傲娇等8-12种表情）
- AI生成表情的一致性控制技术
- 道具设计（角色配件、服装、武器、魔法物品等）
- 场景化角色展示（角色在不同环境中的表现）
- 案例深挖：从表情集到社交媒体表情包的商业化路径

**07-character-output.html** — 设计稿整合输出：
- 潮玩产品稿件标准（尺寸/格式/分辨率要求）
- 整合三视图+表情集+道具为完整设计稿
- 产品渲染图生成（3D效果模拟）
- 使用场景图（角色在真实场景中的表现）
- 包装设计效果图
- 多学派交叉解读

- [ ] **Step 7: 创建第8-12章（完整动画短片制作）**

**08-short-film-plan.html** — 动画短片策划：
- 短片定位：3-5分钟皮克斯风格现代卡通短片
- 剧本创作方法（三幕剧结构/角色弧光/冲突设计）
- 分镜脚本设计（shot list/storyboard）
- 视觉风格设定（color palette/texture reference/lighting mood）
- 案例深挖：皮克斯《包宝宝》的制作流程分析

**09-scene-gen.html** — 场景与角色图像生成：
- 场景设计AI生成工作流（背景/前景/氛围）
- 角色一致性控制在多场景中的应用
- 关键帧图像生成（每个镜头的静态画面）
- 工具链：Midjourney/Flux生成场景 → ComfyUI统一风格
- 实操演示：生成短片的8-12个关键帧

**10-video-gen.html** — 从图像到动画的视频生成：
- 图像转视频工作流详解
- 工具对比与选择（Runway Gen-3/Pika/可灵Kling/Luma）
- 每个关键帧的动画化处理（镜头运动/角色动作/环境动态）
- 视频片段长度控制与拼接
- 实操演示：将8个关键帧转化为8段2-4秒动画片段
- 多学派交叉解读

**11-post-production.html** — 后期合成与音效：
- 视频剪辑与拼接（DaVinci Resolve免费版/剪映）
- 转场效果添加
- 音效与配乐（免费音频资源/AI音乐生成工具如Suno/Udio）
- 字幕添加（AI语音合成/TTS工具）
- 色彩校正与风格统一
- 实操演示：完成一部3-5分钟完整短片

**12-publishing.html** — 成片输出与发布：
- 视频格式与编码标准（H.264/H.265/分辨率/帧率）
- 发布平台选择（B站/YouTube/抖音/小红书）
- 各平台上传优化建议
- AI动画短片的社区运营策略
- 案例深挖：AI动画短片在B站的爆款案例解析

- [ ] **Step 8: 创建第13-14章（进阶与商业化）**

**13-commercial-apps.html** — 商业应用场景：
- AI影像在广告/营销中的应用
- 电商产品图生成
- 游戏/影视前期概念设计
- 教育内容制作
- 个人品牌/IP打造
- 市场分析与趋势预测
- 多学派交叉解读

**14-monetization.html** — 内容变现路径：
- AI潮玩IP周边商品化（手办/盲盒/文具/服饰）
- AI动画短片的广告分成/会员订阅/品牌合作
- AI图像素材出售（Stock照片/模板/预设）
- AI教学课程变现
- 自由职业平台接单（Fiverr/Upwork/国内平台）
- 综合评估与行动指南

- [ ] **Step 9: 验证所有书籍页面的导航完整性**

检查每个页面：
- nav-home 链接指向 `../index.html`
- 上下页导航正确
- TOC侧边栏链接完整
- 首章有"下一本书"链接指向下一本学术书
- 末章有"上一本书"链接指向上本学术书

---

### Task 2: 创建看板HTML文件

**Files:**
- Create: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Interfaces:**
- Consumes: Font Awesome 6.5.1, ECharts 5.5.0
- Produces: 1个完整的看板HTML文件

**Steps:**
- [ ] **Step 1: 创建看板文件，采用暗色赛博朋克主题**

参考 `重庆产业全景研判看板_成渝经济圈_制造业_人口结构.html` 的结构和样式：
- 顶部sticky nav：品牌标识 + 内部锚点导航 + "返回首页"链接（href="index.html"）
- Cover hero区域：标题 + 副标题 + 统计卡片
- 各板块用 section-title 分隔

- [ ] **Step 2: 实现看板各板块**

**板块1：AI影像工具全景矩阵**
- 图像生成工具对比表（10+工具，参数列）
- 视频生成工具对比表（8+工具，参数列）
- 免费工具推荐Top5卡片组
- ECharts柱状图：各工具评分对比

**板块2：AI影像制作产线**
- 完整流程图（eco-diagram组件）：需求→提示词→图像→视频→后期→发布
- 各环节耗时与成本分析表
- 最小工具集方案卡片

**板块3：市场与产业分析**
- AI影像市场规模趋势图（ECharts折线图）
- 创作者经济中AI视觉内容占比
- 主要平台AI内容增长数据
- ECharts饼图：AI影像内容在各平台的分布

**板块4：工具性价比矩阵**
- 四象限图（X轴：价格 Y轴：质量），散点分布各工具
- ECharts雷达图：各工具综合能力对比
- 免费替代方案推荐表

**板块5：潮玩IP角色设计案例**
- 设计流程步骤图（steps-list组件）
- 各阶段工具推荐
- 成功案例展示

**板块6：动画短片制作案例**
- 制作时间线
- 各环节工具链
- 成本分析

**板块7：多学派交叉解读**
- 5个学派卡片（sv-item sv-blue/gold/red/green/purple）
- 古典经济学/凯恩斯主义/马克思主义/新制度经济学/行为演化经济学

**板块8：发散引申链**
- 3-4条引申链（dc-node + dc-arrow组件）

**板块9：投资者/创作者行动指南**
- 高确定性赛道 / 谨慎观察 / 建议规避

- [ ] **Step 3: 添加ECharts图表**

至少6个图表：
1. 工具评分对比柱状图
2. 市场规模趋势折线图
3. 工具性价比四象限散点图
4. 各工具综合能力雷达图
5. AI影像内容平台分布饼图
6. 制作成本构成环形图

- [ ] **Step 4: 验证看板导航**

确保：
- 顶部nav有"返回首页"链接
- 底部footer有版本信息和数据来源
- 内部锚点导航完整

---

### Task 3: 更新 index.html

**Files:**
- Modify: `index.html`

**Steps:**
- [ ] **Step 1: 在 BOOK_DATA 数组中添加新条目**

在 academic group 的现有条目之后添加：
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

- [ ] **Step 2: 验证渲染**

确认新条目在第二辑·学术与文化研究分类下正确显示，卡片样式与其他条目一致。

---

### Task 4: 提交与推送

**Steps:**
- [ ] **Step 1: git add 所有新文件和修改**
- [ ] **Step 2: git commit 带描述性消息**
- [ ] **Step 3: git push origin main**

---

## 关键注意事项

1. **工具信息时效性**：所有AI工具的版本号和功能以2026年最新情况为准。如果某个工具已更新到新版本，使用最新版本信息。

2. **免费优先原则**：教程中每个环节都要提供至少一个免费替代方案。付费工具要标注价格和免费试用期。

3. **步骤详尽程度**：每个操作步骤要精确到按钮级别，例如："打开通义万相官网 → 点击'图像生成' → 在提示词框输入..."

4. **案例一致性**：潮玩IP角色和动画短片使用同一个角色设定（如一只叫"小橘"的皮克斯风格小猫），贯穿全书形成连贯叙事。

5. **数据真实性**：所有市场规模、增长率、用户数等数据必须标注来源（Statista/Gartner/艾瑞咨询等）。

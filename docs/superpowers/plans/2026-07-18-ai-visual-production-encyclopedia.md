# AI影像创作百科全书 — 实现计划

> **For agentic workers:** Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 深度重构AI影像创作书籍和看板——从14章扩展到25章百科全书（26页），看板从9板块扩展到12+板块，修复图表不显示问题，整合全网最新数据。

**Architecture:** 遵循现有项目模式——书籍使用 common/css/book.css + echarts.inline.js + navigation.js，看板使用独立暗色赛博朋克主题。BOOK_DATA 驱动 index.html 卡片渲染。

**Tech Stack:** 纯 HTML/CSS/JS，无第三方JS库。ECharts 内联图表（书籍）和 CDN 图表（看板）。Font Awesome 6.5.1 图标。

## Global Constraints

- 所有工具必须是2025-2026年最新版本，效果最好的免费或低成本工具
- 教程步骤必须足够细致，零基础用户能跟着操作（精确到按钮级别）
- 看板数据必须有真实来源支撑（标注数据来源：Statista/Gartner/艾瑞咨询等）
- 与项目现有看板和书籍保持完全一致的排版样式
- 统一入口在 index.html BOOK_DATA 中
- 每个书籍章节必须包含：多学派交叉解读、案例深挖/发散引申链、ECharts图表
- 每页文件使用 nav-home 链接指向 ../index.html
- 书籍使用紫色主题（--accent: #7c3aed）
- 看板图表修复：CDN脚本用 window.load + 轮询检测确保echarts初始化成功
- 全书总计25章+封面=26页，看板12板块，图表总数26个以上

---

### Task 1: 备份现有文件并创建新目录结构

**Files:**
- Backup existing files
- Create new `ai-visual-production/` directory structure

**Interfaces:**
- Consumes: existing `ai-visual-production/` files (to be backed up)
- Produces: backup copy at `ai-visual-production-backup/`

**Steps:**
- [ ] **Step 1: 备份现有文件**

```bash
cp -r ai-visual-production ai-visual-production-backup
echo "Backup created"
```

- [ ] **Step 2: 清理现有目录**

```bash
rm -rf ai-visual-production
mkdir -p ai-visual-production
echo "Clean directory created"
```

- [ ] **Step 3: 验证共享依赖**

```bash
ls -la common/css/book.css common/js/echarts.inline.js common/js/navigation.js
echo "Dependencies verified"
```

- [ ] **Step 4: 验证备份完整性**

```bash
ls ai-visual-production-backup/*.html | wc -l
echo "Backup contains $(ls ai-visual-production-backup/*.html | wc -l) files"
```

---

### Task 2: 创建书籍封面页 (index.html)

**Files:**
- Create: `ai-visual-production/index.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 封面页面，含5篇目录结构、ECharts雷达图

**Steps:**
- [ ] **Step 1: 读取参考模板**

读取 `creators/index.html` 和 `chongqing/index.html` 作为结构参考。

- [ ] **Step 2: 创建封面页面**

创建 `ai-visual-production/index.html`，包含：
- **标题**: 《AI影像创作百科全书：从工具选型到潮玩IP角色设计与完整动画短片》
- **副标题**: AI图像/视频/3D/Audio工具全景对比 · 提示词工程 · 潮玩IP角色设计稿实战 · 完整动画短片制作全流程 · 工作流自动化 · 变现路径
- **数据统计卡片**: 25章 / 80+页 / 25+工具 / 5篇结构 / 20+图表 / 6大实战方向
- **封面插图SVG**: 神经网络抽象图 + 像素画风格（紫色主题 #7c3aed），替代太极八卦图
- **目录网格**: 5篇结构展示：
  - 第一篇：工具选型与基础（第1-4章）
  - 第二篇：潮玩IP角色设计实战（第5-9章）
  - 第三篇：完整动画短片制作全流程（第10-16章）
  - 第四篇：AI工作流自动化与进阶（第17-22章）
  - 第五篇：变现路径与未来展望（第23-25章）
- **ECharts雷达图**: 展示技能维度（图像生成/视频生成/提示词工程/角色设计/后期制作/3D建模/AI音乐/工作流自动化）
- **引入**: `../common/css/book.css`、`../common/js/echarts.inline.js`、`../common/js/navigation.js`
- **footer**: nav-home 链接 `href="../index.html"`

- [ ] **Step 3: 验证封面页**

```bash
wc -l ai-visual-production/index.html
grep -c 'echarts.init' ai-visual-production/index.html
grep -c 'nav-home' ai-visual-production/index.html
```

---

### Task 3: 创建第一篇章节（第1-4章：工具选型与基础）

**Files:**
- Create: `ai-visual-production/01-tool-overview.html`
- Create: `ai-visual-production/02-prompt-engineering.html`
- Create: `ai-visual-production/03-env-setup.html`
- Create: `ai-visual-production/04-industry-analysis.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 4章内容，每章含ECharts图表、多学派解读、案例深挖

**Steps:**
- [ ] **Step 1: 创建 01-tool-overview.html**

内容：
- AI影像市场规模数据（2025年全球约$85亿, 年增长率42%, 创作者超3000万）— 标注来源 Statista/Gartner
- 图像生成工具矩阵表（10+工具：Midjourney v7/DALL-E 4/SD 3.5/Flux/通义万相/文心一格/KREA/Leonardo/Firefly/即梦）
- 视频生成工具矩阵表（8+工具：Runway Gen-3/可灵Kling/Pika 1.5/Luma/Sora/Haiper/即梦）
- 3D生成工具矩阵表（5+工具：Meshy/CSM/Luma AI/Tripo/Blender AI插件）
- 音乐音效工具矩阵表（5+工具：Suno v3.5/Udio/Murf/ElevenLabs/AIVA）
- ECharts柱状图：各工具综合评分对比
- ECharts雷达图：免费vs付费性价比对比
- 多学派交叉解读（古典经济学-分工效率、马克思主义-生产力变革、新制度经济学-交易成本降低）
- 案例深挖：Midjourney从v1(2022)到v7的进化史
- 发散引申链

- [ ] **Step 2: 创建 02-prompt-engineering.html**

内容：
- 结构化提示词框架：[主体描述]+[风格关键词]+[构图/视角]+[光照/色彩]+[细节层级]+[负面词]
- 6大风格提示词配方（皮克斯风/写实风/水彩风/赛博朋克/国风/潮玩风）— 每种含完整示例提示词
- 视频生成提示词模板（镜头语言/运动描述/转场/节奏）
- 正面词词典（按类别分类）
- 负面词词典（按风格分类）
- 提示词优化前后对比案例（before/after with actual prompts）
- ECharts词云概念图（用bar chart展示高频提示词词频）
- 多学派交叉解读
- 案例深挖：爆款AI潮玩角色的提示词拆解

- [ ] **Step 3: 创建 03-env-setup.html**

内容：
- 硬件需求评估（GPU门槛/云端替代方案）
- 免费工具配置指南（逐步截图式文字说明）：
  - 通义万相注册与使用
  - 可灵Kling免费额度使用
  - Stable Diffusion本地部署（WebUI/ComfyUI）
  - Flux本地/云端部署
- 付费工具性价比分析（Midjourney订阅vs按需付费）
- 最小工具集推荐方案（3个免费工具即可入门）
- ECharts硬件需求对比图
- 多学派交叉解读
- 发散引申链

- [ ] **Step 4: 创建 04-industry-analysis.html**

内容：
- AI影像产业链全景图（上游模型→中游平台→下游应用）
- 全球竞争格局分析（美国/中国/欧洲/日本）
- 主要公司对比（OpenAI/Google/Meta/字节跳动/快手/阿里/百度）
- 中国AI影像发展路径分析
- ECharts市场规模预测折线图（2020-2030）
- ECharts饼图：全球AI影像市场份额分布
- 多学派交叉解读
- 案例深挖：中国AI影像创业公司生态

- [ ] **Step 5: 验证导航**

检查每个页面：
- nav-home 链接指向 `../index.html`
- 上下页导航正确
- TOC侧边栏链接完整（25章全部列出）
- 首章有"下一本书"链接（如果有后续学术书）

---

### Task 4: 创建第二篇章节（第5-9章：潮玩IP角色设计实战）

**Files:**
- Create: `ai-visual-production/05-character-design.html`
- Create: `ai-visual-production/06-character-views.html`
- Create: `ai-visual-production/07-expression-props.html`
- Create: `ai-visual-production/08-lora-controlnet.html`
- Create: `ai-visual-production/09-character-output.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 5章内容，含详细教程步骤、实操演示

**Steps:**
- [ ] **Step 1: 创建 05-character-design.html**

内容：
- 潮玩IP角色设计原则（可爱度/辨识度/延展性/商业价值）
- 皮克斯/迪士尼风格特征分析
- Labubu/Molly/Duffy角色设计拆解对比表
- 角色设计流程：概念→草图→三视图→表情→道具
- ECharts潮玩IP成功要素雷达图
- 案例深挖：Labubu的设计哲学与商业化路径
- 多学派交叉解读

- [ ] **Step 2: 创建 06-character-views.html**

内容：
- 三视图的重要性与标准
- AI生成三视图完整步骤（5步法）
- 提示词配方：角色一致性技巧
- 实操演示：设计一只皮克斯风格的小橘猫角色
- 每步的详细提示词、参数设置、输出结果展示
- ECharts角色一致性技术对比表
- 多学派交叉解读

- [ ] **Step 3: 创建 07-expression-props.html**

内容：
- 12种标准表情生成（喜/怒/哀/乐/惊/惧/羞涩/傲娇/困惑/兴奋/疲惫/愤怒）
- AI生成表情的一致性控制技术
- 道具设计（配件/服装/武器/魔法物品）
- 场景化角色展示
- 表情包商业化案例（微信/LINE）
- ECharts表情包市场数据图
- 多学派交叉解读

- [ ] **Step 4: 创建 08-lora-controlnet.html**

内容：
- LoRA训练全教程：数据集准备→标注→训练→推理
- ControlNet精细控制：Canny/Depth/OpenPose/Normal
- ComfyUI中的LoRA节点配置
- 实操演示：为小橘猫角色训练专属LoRA模型
- 训练参数详解（epoch/batch_size/learning_rate）
- ECharts训练效果对比图
- 多学派交叉解读

- [ ] **Step 5: 创建 09-character-output.html**

内容：
- 潮玩产品稿件标准（尺寸/格式/分辨率要求）
- 整合三视图+表情集+道具为完整设计稿
- Mockup生成方法（3D效果模拟）
- 包装设计效果图
- ECharts潮玩产品成本构成饼图
- 多学派交叉解读

- [ ] **Step 6: 验证导航**

检查第二篇所有章节的prev/next链接和TOC。

---

### Task 5: 创建第三篇章节（第10-16章：完整动画短片制作全流程）

**Files:**
- Create: `ai-visual-production/10-short-film-plan.html`
- Create: `ai-visual-production/11-scene-gen.html`
- Create: `ai-visual-production/12-video-gen.html`
- Create: `ai-visual-production/13-post-production.html`
- Create: `ai-visual-production/14-music-sound.html`
- Create: `ai-visual-production/15-tts-subtitles.html`
- Create: `ai-visual-production/16-publishing.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 7章内容，完整动画短片制作全流程

**Steps:**
- [ ] **Step 1: 创建 10-short-film-plan.html**

内容：
- 短片定位：3-5分钟皮克斯风格现代卡通短片
- 剧本创作方法（三幕剧结构/角色弧光/冲突设计）
- 分镜脚本设计（shot list/storyboard）
- 视觉风格设定（color palette/texture reference/lighting mood）
- 实操演示：为"小橘猫找回家"设计完整分镜（12个关键镜头）
- 案例深挖：皮克斯《包宝宝》的制作流程分析
- ECharts短片制作甘特图
- 多学派交叉解读

- [ ] **Step 2: 创建 11-scene-gen.html**

内容：
- 场景设计AI生成工作流（背景/前景/氛围分层）
- 角色一致性控制在多场景中的应用
- 关键帧图像生成（每个镜头的静态画面）
- 工具链：Midjourney/Flux生成场景 → ComfyUI统一风格
- 实操演示：生成短片的8-12个关键帧
- 每帧的详细提示词和参数
- ECharts场景生成工具对比图
- 多学派交叉解读

- [ ] **Step 3: 创建 12-video-gen.html**

内容：
- 图像转视频工作流详解
- 工具对比与选择（Runway Gen-3/Pika/可灵Kling/Luma/Sora）
- 每个关键帧的动画化处理（镜头运动/角色动作/环境动态）
- 视频片段长度控制与拼接
- 实操演示：将8个关键帧转化为8段2-4秒动画片段
- ECharts视频生成工具性能对比雷达图
- 多学派交叉解读

- [ ] **Step 4: 创建 13-post-production.html**

内容：
- 视频剪辑与拼接（DaVinci Resolve免费版/剪映）
- 转场效果添加（硬切/淡入淡出/叠化/匹配剪辑）
- 色彩校正与风格统一
- 特效添加（粒子/光效/模糊）
- 实操演示：完成一部3-5分钟完整短片
- ECharts后期制作成本构成环形图
- 多学派交叉解读

- [ ] **Step 5: 创建 14-music-sound.html**

内容：
- 免费音频资源库（Freesound.org/YouTube Audio Library/Pixabay Music）
- AI音乐生成（Suno v3.5/Udio）— 操作步骤、提示词、参数
- AI音效设计（环境音/动作音效/情绪配乐的比例）
- 实操演示：为"小橘猫找回家"配置完整音效层次
- ECharts音乐生成工具对比图
- 多学派交叉解读

- [ ] **Step 6: 创建 15-tts-subtitles.html**

内容：
- 免费TTS工具（Edge TTS/Coqui TTS）— 安装与使用教程
- 付费TTS（ElevenLabs）— 音质对比
- 中文配音推荐（剪映内置配音/通义听悟）
- 字幕样式和位置规范
- 实操演示：为短片生成中文配音和字幕
- ECharts TTS工具音质/价格对比图
- 多学派交叉解读

- [ ] **Step 7: 创建 16-publishing.html**

内容：
- 视频格式与编码标准（H.264/H.265/分辨率/帧率/码率）
- 发布平台选择（B站/YouTube/抖音/小红书）
- 各平台上传优化建议
- AI动画短片的社区运营策略
- 案例深挖：AI动画短片在B站的爆款案例解析
- ECharts各平台AI动画内容增长趋势折线图
- 多学派交叉解读

- [ ] **Step 8: 验证导航**

检查第三篇所有章节的prev/next链接和TOC。

---

### Task 6: 创建第四篇章节（第17-22章：AI工作流自动化与进阶）

**Files:**
- Create: `ai-visual-production/17-comfyui-advanced.html`
- Create: `ai-visual-production/18-workflow-automation.html`
- Create: `ai-visual-production/19-3d-generation.html`
- Create: `ai-visual-production/20-short-video-ops.html`
- Create: `ai-visual-production/21-commercial-apps.html`
- Create: `ai-visual-production/22-advanced-painting.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 6章内容，进阶工作流与自动化

**Steps:**
- [ ] **Step 1: 创建 17-comfyui-advanced.html**

内容：
- ComfyUI节点编排基础（理解节点、连线、工作流）
- 批量生产工作流（批量图像生成/批量视频处理）
- API集成（通过API调用ComfyUI进行自动化）
- 自定义插件开发基础
- 实操演示：搭建一个完整的AI影像生产流水线
- EChartsComfyUI工作流复杂度对比图
- 多学派交叉解读

- [ ] **Step 2: 创建 18-workflow-automation.html**

内容：
- n8n自动化平台介绍与部署（自托管/Cloud）
- Make/Zapier平台对比
- 工具链连接示例（通义万相→可灵→剪映→B站自动上传）
- 定时任务与触发器配置
- 实操演示：搭建一个每日自动生成AI内容的自动化系统
- ECharts自动化工作流工具对比图
- 多学派交叉解读

- [ ] **Step 3: 创建 19-3d-generation.html**

内容：
- Meshy/CSM/Luma AI 3D生成工具对比
- 文本/图像转3D模型教程
- 3D模型后处理（Blender基础）
- 手办打样流程（3D打印→涂装→量产）
- Print-on-Demand服务推荐（Shapeways/Protolabs）
- ECharts 3D生成工具质量/速度/价格对比图
- 多学派交叉解读

- [ ] **Step 4: 创建 20-short-video-ops.html**

内容：
- 多平台分发策略（B站/YouTube/抖音/小红书/视频号）
- 数据分析工具（各平台创作者后台分析）
- 算法优化技巧（标签/标题/封面/发布时间）
- A/B测试方法论
- 实操演示：制定一个30天内容运营计划
- ECharts各平台流量分布饼图
- 多学派交叉解读

- [ ] **Step 5: 创建 21-commercial-apps.html**

内容：
- AI影像在广告/营销中的应用
- 电商产品图生成
- 游戏/影视前期概念设计
- 教育内容制作
- 个人品牌/IP打造
- 市场分析与趋势预测
- ECharts商业应用场景分布图
- 多学派交叉解读

- [ ] **Step 6: 创建 22-advanced-painting.html**

内容：
- IP-Adapter面部/风格迁移技术
- Region区域控制（局部重绘/背景替换）
- Inpaint/Outpaint（局部修改/扩展画布）
- 高清放大技术（4x/8x超分辨率）
- 实操演示：将一张普通照片转化为AI艺术作品
- ECharts进阶技法效果对比图
- 多学派交叉解读

- [ ] **Step 7: 验证导航**

检查第四篇所有章节的prev/next链接和TOC。

---

### Task 7: 创建第五篇章节（第23-25章：变现路径与未来展望）

**Files:**
- Create: `ai-visual-production/23-merchandise.html`
- Create: `ai-visual-production/24-monetization.html`
- Create: `ai-visual-production/25-future-trends.html`

**Interfaces:**
- Consumes: `common/css/book.css`, `common/js/echarts.inline.js`, `common/js/navigation.js`
- Produces: 3章内容，变现与未来展望

**Steps:**
- [ ] **Step 1: 创建 23-merchandise.html**

内容：
- 手办/盲盒生产流程（设计稿→3D建模→打样→量产）
- Print-on-Demand服务推荐（Redbubble/Etsy/Printful）
- 文具/服饰/手机壳等轻周边
- 独立设计师平台运营（ArtStation/Gumroad）
- 案例深挖：独立设计师通过AI设计月入$5000+的真实案例
- ECharts周边商品成本利润分析图
- 多学派交叉解读

- [ ] **Step 2: 创建 24-monetization.html**

内容：
- 各变现路径启动资金/时间投入/预期收入对比表
- AI动画短片广告分成机制和收益预期
- 会员订阅/Patreon粉丝赞助
- 自由职业平台接单（Fiverr/Upwork/国内平台）
- AI教学课程变现
- 新手推荐路线：免费工具入门→技能积累→平台接单→IP打造
- ECharts各变现路径ROI对比柱状图
- 多学派交叉解读

- [ ] **Step 3: 创建 25-future-trends.html**

内容：
- AI影像技术路线图（2025-2030）
- 监管政策分析（版权法/Deepfake法规/平台审核）
- 就业影响分析（哪些岗位被替代/哪些新岗位产生）
- 新商业模式预测（AI原生内容平台/虚拟偶像经济）
- ECharts技术成熟度曲线
- 多学派交叉解读

- [ ] **Step 4: 验证导航**

检查第五篇所有章节的prev/next链接和TOC。

---

### Task 8: 更新书籍封面页TOC和导航

**Files:**
- Modify: `ai-visual-production/index.html`

**Interfaces:**
- Consumes: 25章文件名和标题
- Produces: 完整的5篇目录结构

**Steps:**
- [ ] **Step 1: 更新封面页TOC**

将目录从4篇14章更新为5篇25章：
- 第一篇：工具选型与基础（01-04）
- 第二篇：潮玩IP角色设计实战（05-09）
- 第三篇：完整动画短片制作全流程（10-16）
- 第四篇：AI工作流自动化与进阶（17-22）
- 第五篇：变现路径与未来展望（23-25）

- [ ] **Step 2: 更新ECharts雷达图**

增加技能维度：图像生成/视频生成/提示词工程/角色设计/后期制作/3D建模/AI音乐/工作流自动化

- [ ] **Step 3: 验证所有链接**

```bash
for f in ai-visual-production/*.html; do
  grep -oP 'href="[^"]*\.html"' "$f" | sort -u
done | sort -u | wc -l
```

---

### Task 9: 修复看板图表不显示问题 + 扩展看板内容

**Files:**
- Create: `AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html`

**Interfaces:**
- Consumes: Font Awesome 6.5.1 CDN, ECharts 5.5.0 CDN
- Produces: 修复后的看板HTML，12板块，6+图表

**Steps:**
- [ ] **Step 1: 删除旧看板文件**

```bash
rm -f "AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html"
echo "Old kanban removed"
```

- [ ] **Step 2: 创建新版看板 — 基础结构**

参考 `重庆产业全景研判看板_成渝经济圈_制造业_人口结构.html` 的结构和样式：
- 顶部sticky nav：品牌标识 + 内部锚点导航 + "返回首页"链接（href="index.html"）
- Cover hero区域：标题 + 副标题 + 统计卡片
- 各板块用 section-title 分隔
- CSS变量与参考看板完全一致

- [ ] **Step 3: 实现看板各板块**

**板块1：AI影像工具全景矩阵 (#tools-matrix)**
- 图像生成工具对比表（10+工具）
- 视频生成工具对比表（8+工具）
- 3D生成工具对比表（5+工具）
- 音乐音效工具对比表（5+工具）
- 免费工具推荐Top5卡片组
- ECharts柱状图：各工具评分对比

**板块2：AI影像制作产线 (#production-line)**
- 完整流程图（eco-diagram组件）：需求→提示词→图像→视频→后期→发布
- 各环节耗时与成本分析表
- 最小工具集方案卡片

**板块3：市场与产业分析 (#market-analysis)**
- AI影像市场规模趋势图（ECharts折线图，2020-2030数据）
- 创作者经济中AI视觉内容占比（ECharts饼图）
- 主要平台AI内容增长数据表

**板块4：工具性价比矩阵 (#cost-performance)**
- 四象限图（X轴：价格 Y轴：质量），散点分布各工具（ECharts散点图）
- 各工具综合能力雷达图（ECharts雷达图）
- 免费替代方案推荐表

**板块5：提示词工程指南 (#prompt-guide)**
- 结构化提示词框架
- 6大风格配方速查表
- 正负面词词典

**板块6：潮玩IP角色设计案例 (#character-case)**
- 设计流程步骤图（steps-list组件）
- 各阶段工具推荐
- 成功案例展示（Labubu/Molly/Duffy对比）

**板块7：动画短片制作案例 (#film-case)**
- 制作时间线
- 各环节工具链
- 传统制作 vs AI辅助成本对比（ECharts柱状图）

**板块8：AI 3D与建模工具 (#3d-tools)**
- 3D生成工具对比表
- 手办打样流程图
- 3D生成质量/速度/价格对比图（ECharts）

**板块9：AI音乐与音效工具 (#music-tools)**
- 音乐生成工具对比表
- 音效设计层次图
- Suno/Udio/Murf功能对比

**板块10：工作流自动化 (#workflow-auto)**
- ComfyUI工作流示意图
- n8n/Make/Zapier对比表
- 批量生产方案推荐

**板块11：多学派交叉解读 (#multi-school)**
- 5个学派卡片（sv-item sv-blue/gold/red/green/purple）

**板块12：发散引申链 + 行动指南 (#divergence-chains)**
- 4条引申链（dc-node + dc-arrow组件）
- 高确定性赛道/谨慎观察/建议规避

- [ ] **Step 4: 修复图表显示 — 核心修复**

**根因分析**：看板使用 CDN echarts@5.5.0，但 `DOMContentLoaded` 事件可能在脚本加载完成前就触发了。

**修复方案**：
```javascript
// 使用轮询检测确保echarts库加载完成后再初始化
function waitForEcharts(callback, timeoutMs) {
  var start = Date.now();
  function check() {
    if (typeof echarts !== 'undefined') {
      callback();
    } else if (Date.now() - start < (timeoutMs || 10000)) {
      setTimeout(check, 100);
    } else {
      console.error('ECharts load timeout');
    }
  }
  check();
}

// 所有图表初始化都包裹在此函数中
waitForEcharts(function() {
  // chart 1 init...
  // chart 2 init...
  // ...
});
```

- [ ] **Step 5: 添加ECharts图表**

至少6个图表：
1. 工具评分对比柱状图
2. 市场规模趋势折线图
3. 工具性价比四象限散点图
4. 各工具综合能力雷达图
5. AI影像内容平台分布饼图
6. 制作成本构成环形图

- [ ] **Step 6: 验证看板导航**

确保：
- 顶部nav有"返回首页"链接
- 底部footer有版本信息和数据来源
- 内部锚点导航完整
- 所有6个图表正常显示

---

### Task 10: 更新 index.html BOOK_DATA

**Files:**
- Modify: `index.html`

**Steps:**
- [ ] **Step 1: 更新现有BOOK_DATA条目**

找到 `ai-visual-production` 相关条目（如果存在则更新，否则新增）：

```javascript
{
  name: "《AI影像创作百科全书：从工具选型到潮玩IP角色设计与完整动画短片》",
  shortName: "AI影像创作",
  desc: "AI图像/视频/3D/Audio工具全景对比、提示词工程、潮玩IP角色设计稿实战、完整动画短片制作全流程、工作流自动化、变现路径。",
  group: "academic", icon: "fa-wand-magic-sparkles", color: "purple",
  pages: 80, charts: 20,
  tags: ["AI影像", "角色设计", "动画短片", "3D生成", "工作流自动化"],
  highlights: [
    { label: "工具", value: "25+" },
    { label: "图表", value: "20+" },
    { label: "实战案例", value: "6大方向" },
    { label: "篇章", value: "5篇25章" }
  ],
  bookUrl: "ai-visual-production/index.html",
  kanbanUrl: "AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html"
}
```

- [ ] **Step 2: 验证渲染**

确认新条目在第二辑·学术与文化研究分类下正确显示。

---

### Task 11: 提交与推送

**Steps:**
- [ ] **Step 1: git add 所有新文件和修改**

```bash
git add ai-visual-production/ "AI视频图像设计全景看板_AI工具矩阵_潮玩IP角色设计_动画短片制作.html" index.html
```

- [ ] **Step 2: git commit 带描述性消息**

```bash
git commit -m "feat: deep-enrich AI影像创作 encyclopedia — 25 chapters, 12 kanban sections, fix chart display, latest data integrated"
```

- [ ] **Step 3: git push origin main**

```bash
git push origin main
```

---

## 关键注意事项

1. **工具信息时效性**：所有AI工具的版本号和功能以2025-2026年最新情况为准。搜索最新数据后直接嵌入文档。

2. **免费优先原则**：教程中每个环节都要提供至少一个免费替代方案。付费工具要标注价格和免费试用期。

3. **步骤详尽程度**：每个操作步骤要精确到按钮级别，例如："打开通义万相官网 → 点击'图像生成' → 在提示词框输入..."

4. **案例一致性**：潮玩IP角色和动画短片使用同一个角色设定（如一只叫"小橘"的皮克斯风格小猫），贯穿全书形成连贯叙事。

5. **数据真实性**：所有市场规模、增长率、用户数等数据必须标注来源（Statista/Gartner/艾瑞咨询等）。

6. **图表修复是最高优先级**：看板图表不显示是致命缺陷，必须在Task 9中彻底修复。

7. **新增6个方向的深度**：LoRA训练、ComfyUI高级工作流、3D生成、AI音乐、工作流自动化、短视频运营 — 每个方向都要有完整的实操教程。

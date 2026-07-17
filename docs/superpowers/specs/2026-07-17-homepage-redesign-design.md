# AnaReports 首页视觉升级与看板合并设计

> **日期:** 2026-07-17
> **状态:** 已批准

---

## 目标

将 11 本书与 11 个看板合并为统一卡片入口，每个卡片包含「进入书籍」和「查看看板」两个按钮。同时升级首页视觉：粒子背景 + 3D 卡片 + 分类折叠。

## 用户故事

- 访客打开首页 → 看到炫酷的粒子背景和分类标题
- 点击展开/折叠某个分类组
- 每本书对应一个 3D 卡片，hover 时立体倾斜 + 发光
- 卡片内默认展示书籍信息（标题、简介、章节数/页数、关键数据亮点）
- 两个按钮：「📖 进入书籍」跳转书籍 index.html，「📊 查看看板」跳转看板文件
- 全局搜索框可按书名/关键词过滤卡片

## 架构

### 单页结构
```
index.html (重写)
├── Canvas 粒子背景层 (固定定位，pointer-events: none)
├── Hero 区域 (标题 + 统计栏)
├── 搜索框 (可选，filter cards by text)
├── 分类组 × 4
│   ├── details/summary 折叠交互
│   └── books-grid (卡片容器)
│       ├── 卡片 × N (3D perspective + hover tilt)
│       │   ├── card-icon
│       │   ├── card-title (学术书名)
│       │   ├── card-desc (简介)
│       │   ├── card-tags (标签)
│       │   ├── card-meta (页数 + 图表数)
│       │   ├── card-highlights (3-4 关键数据)
│       │   └── card-actions (双按钮)
│       │       ├── 「📖 进入书籍」→ book/index.html
│       │       └── 「📊 查看看板」→ kanban.html
│       └── ...
└── Footer
```

### 卡片数据结构 (JS 驱动)
```js
const BOOK_DATA = [
  {
    name: "《重庆产业格局与未来展望：成渝双城经济圈深度研判》",
    shortName: "重庆产业格局",
    desc: "常住人口与户籍制度深度解析…",
    group: "regional", // regional | academic | macro | industry
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
  // ... 11 books
];
```

### 渲染逻辑
- 页面加载时 JS 遍历 `BOOK_DATA`，按 group 分组渲染到对应分类下
- 分类折叠用 `<details>/<summary>` 原生 HTML 元素
- 搜索框实时 filter 卡片（`dataset.name` 匹配）
- 3D tilt 效果：`mousemove` → 计算鼠标相对卡片中心偏移 → `rotateX/Y`

### 粒子系统
- Canvas 覆盖全屏，`position: fixed; z-index: -1`
- ~80 个节点，每个节点代表一本书或看板数据点
- 节点间距离 < 150px 时画线连接
- 缓慢浮动动画 requestAnimationFrame
- 颜色与卡片 color scheme 一致

## 视觉规范

### 颜色映射
| 分类 | 主色 | 卡片 accent |
|------|------|------------|
| 地域市场分析 | cyan (#06b6d4) | 各书独立色 |
| 学术与文化研究 | red (#ef4444) | 各书独立色 |
| 宏观经济分析 | pink (#ec4899) | 各书独立色 |
| 产业专题研究 | purple (#8b5cf6) | 各书独立色 |

### 3D 卡片参数
- `perspective: 1000px` on container
- `transform-style: preserve-3d` on card
- Hover tilt range: ±8deg
- Hover lift: translateY(-8px)
- Glow shadow: 对应颜色的 box-shadow

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `index.html` | 重写 | 粒子背景 + 3D 卡片 + 分类折叠 + 搜索 |
| (无其他) | — | 看板文件和书籍文件不变 |

## 非目标
- 不修改任何书籍的 index.html
- 不修改任何看板 HTML 文件
- 不添加后端/API，纯静态
- 不引入第三方 JS 库（仅原生 Canvas + CSS）

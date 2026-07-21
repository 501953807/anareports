# CBHunter 多平台电商后台调研与文档产出实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute chrome-devtools-based research across 4 e-commerce platforms (Shopee, TikTok Shop, Temu, Miaoshou ERP) and produce 5 standardized documentation deliverables in project/CBHunter/

**Architecture:** Pure documentation project — no code implementation. Research uses read-only chrome-devtools MCP to extract page structures, form fields,操作流程, and国别差异 from seller backend interfaces.

**Tech Stack:** Chrome DevTools MCP (port 9222), markdown documents, CSV files, browser screenshots

## Global Constraints

- **Browser operation rule:** Only use chrome-devtools MCP with port 9222; NO Playwright calls
- **Read-only constraint:** NO write operations (no saving, publishing, modifying prices, creating campaigns, deleting products/orders)
- **Output directory:** All deliverables go to `project/CBHunter/`
- **MCP tools:** Only chrome-devtools, serena, codegraph enabled; disable playwright
- **Connection failure:** If chrome-devtools port disconnects, STOP research and notify user immediately
- **Platform priority:** Shopee → TikTok Shop → Temu → Miaoshou ERP
- **Shopee coverage:** All SE Asia sites (Singapore, Malaysia, Thailand, Vietnam, Philippines, Indonesia, Brazil, etc.)
- **TikTok Shop coverage:** All open sites (SE Asia + Europe/US)
- **Document style:** Standard Markdown, structured by platform/module, field-level detail

---

## Task 1: Execute Shopee Platform Research

**Files:**
- Create: `project/CBHunter/research/shopee_fields.md`
- Create: `project/CBHunter/screenshots/shopee-*.png` (multiple screenshots)

**Interfaces:**
- Consumes: chrome-devtools MCP connection to Shopee seller center
- Produces: Complete field extraction for Shopee product list, add product, categories, SKUs, pricing, marketing, orders, funds modules

### Step 1: Shopee Product List Page Extraction

- [ ] Select Shopee page (pageId: 2) via chrome-devtools
- [ ] Take screenshot of product list page
- [ ] Extract page text using evaluate_script to get all visible fields
- [ ] Record: column headers, filter options, batch action buttons, status tags
- [ ] Record: product card structure (title, price, stock, sales, SKU info)
- [ ] Note: current shop is Philippines site (cocotrip.ph)

### Step 2: Shopee Add Product Flow

- [ ] Click "添加商品" button to enter product creation flow
- [ ] Capture category selection page structure
- [ ] Extract base information fields (title, description, images, attributes)
- [ ] Extract SKU specification fields (color, size, weight, dimensions)
- [ ] Extract pricing fields (original price, sale price, shipping fee)
- [ ] Extract logistics settings
- [ ] Note platform-specific requirements (Shopee standard product eligibility, Hot Listing)

### Step 3: Shopee Marketing Module

- [ ] Navigate to 营销中心
- [ ] Extract discount activity fields (限时折扣, 满减, 优惠券)
- [ ] Extract flash sale configuration
- [ ] Note SE Asia site-specific campaign rules

### Step 4: Shopee Order & Funds Module

- [ ] Navigate to 订单 module
- [ ] Extract order list fields (order status, filters, actions)
- [ ] Extract transaction details (commission, shipping fee, withdrawal fee)
- [ ] Navigate to 财务 module
- [ ] Extract payment cycle, settlement rules, withdrawal configuration
- [ ] Note currency differences across SE Asia sites

### Step 5: Shopee Category System

- [ ] Document category tree structure (L1/L2/L3)
- [ ] Record category binding rules
- [ ] Note site-specific category differences

**Expected output:** ~2000-3000 words field extraction document

---

## Task 2: Execute TikTok Shop Platform Research

**Files:**
- Create: `project/CBHunter/research/tiktok_fields.md`
- Create: `project/CBHunter/screenshots/tiktok-*.png`

**Interfaces:**
- Consumes: chrome-devtools MCP connection to TikTok Shop seller center
- Produces: Complete field extraction for TikTok Shop product, marketing, order, funds modules

### Step 1: TikTok Shop Page Structure

- [ ] Select TikTok Shop page (pageId: 3)
- [ ] Take screenshot of current order page
- [ ] Document sidebar navigation structure
- [ ] Note global vs SE Asia site differences

### Step 2: TikTok Shop Product Module

- [ ] Navigate to 商品 module
- [ ] Extract product list fields and filters
- [ ] Extract add/edit product flow
- [ ] Record category system and binding rules
- [ ] Record SKU management fields
- [ ] Record pricing template configuration

### Step 3: TikTok Shop Marketing Module

- [ ] Navigate to 营销中心
- [ ] Extract discount activity configuration panels
- [ ] Record watermark settings
- [ ] Note live streaming integration features

### Step 4: TikTok Shop Order & Funds

- [ ] Navigate to 订单 module
- [ ] Extract order list, status, actions
- [ ] Navigate to 资金 module
- [ ] Extract settlement rules, withdrawal configuration

### Step 5: TikTok Shop Site Differences

- [ ] Document SE Asia sites (Singapore, Malaysia, Thailand, Vietnam, Philippines, Indonesia)
- [ ] Document global sites (UK, US, etc.)
- [ ] Record currency, tax, logistics differences per site

**Expected output:** ~2000-3000 words field extraction document

---

## Task 3: Execute Temu Platform Research

**Files:**
- Create: `project/CBHunter/research/temu_fields.md`
- Create: `project/CBHunter/screenshots/temu-*.png`

**Interfaces:**
- Consumes: chrome-devtools MCP connection to Temu seller center
- Produces: Complete field extraction for Temu product, order, funds modules

### Step 1: Temu Page Structure

- [ ] Select Temu page (pageId: 5)
- [ ] Take screenshot of goods list page
- [ ] Document full-managed vs semi-managed model differences

### Step 2: Temu Product Module

- [ ] Extract product list fields
- [ ] Extract add/edit product flow
- [ ] Record category system
- [ ] Record SKU and pricing fields
- [ ] Note Temu-specific requirements (supply chain rules, quality standards)

### Step 3: Temu Order & Funds

- [ ] Extract order management fields
- [ ] Extract settlement and fund flow fields
- [ ] Record commission and fee structure

**Expected output:** ~1500-2000 words field extraction document

---

## Task 4: Execute Miaoshou ERP Research

**Files:**
- Create: `project/CBHunter/research/miaoshou_fields.md`
- Create: `project/CBHunter/screenshots/miaoshou-*.png`

**Interfaces:**
- Consumes: chrome-devtools MCP connection to Miaoshou ERP
- Produces: Multi-platform adaptation reference design

### Step 1: Miaoshou ERP Architecture

- [ ] Select Miaoshou page (pageId: 7)
- [ ] Document overall architecture and platform support
- [ ] Extract multi-platform listing workflow

### Step 2: Miaoshou Field Mapping

- [ ] Record how Miaoshou handles unified vs platform-specific fields
- [ ] Extract batch operation capabilities
- [ ] Record category mapping logic
- [ ] Record SKU synchronization strategy

### Step 3: Reference Design Notes

- [ ] Document what makes Miaoshou's multi-platform approach mature
- [ ] Identify patterns CBHunter should adopt as benchmark

**Expected output:** ~1000-1500 words reference analysis document

---

## Task 5: Write 01_多平台电商后台调研汇总.md

**Files:**
- Create: `project/CBHunter/01_多平台电商后台调研汇总.md`

**Content structure:**
```markdown
# 多平台电商后台调研汇总

## 一、Shopee 卖家中心
### 1.1 前端界面布局
### 1.2 商品模块
#### 1.2.1 商品列表展示页
#### 1.2.2 商品编辑/发布上架流程
#### 1.2.3 商品分类体系
#### 1.2.4 SKU管理
#### 1.2.5 定价模板
### 1.3 营销活动模块
### 1.4 订单管理模块
### 1.5 回款/资金模块
### 1.6 国别差异化点

## 二、TikTok Shop 卖家中心
(same structure)

## 三、TEMU 卖家后台
(same structure)

## 四、妙手 ERP（对标参考）
### 4.1 多平台适配架构
### 4.2 字段映射策略
### 4.3 批量操作设计

## 五、横向对比总结
```

**Requirements:**
- Each platform gets complete chapter
- Every page has all input/display fields listed
- Platform-specific rules documented
- Country/site differences highlighted

---

## Task 6: Write 02_功能开发方案总文档.md

**Files:**
- Create: `project/CBHunter/02_功能开发方案总文档.md`

**Content structure:**
```markdown
# CBHunter 功能开发方案总文档

## 第一部分：架构方案
### 1.1 多平台发布功能：混合架构设计
### 1.2 店铺 - 产品层级 UI/UX 设计方案
### 1.3 多国家市场差异化解决方案

## 第二部分：标准化功能需求
### 2.1 商品模块需求
### 2.2 营销活动模块需求
### 2.3 订单管理模块需求
### 2.4 回款/资金模块需求

## 第三部分：平台差异化扩展设计规范
### 3.1 扩展字段表设计
### 3.2 差异化配置存储方案
### 3.3 动态表单渲染逻辑
```

**Requirements:**
- Answer three core architecture questions
- Include page prototype descriptions
- Document button logic, popup fields, validation rules
- Specify extension field table and storage scheme

---

## Task 7: Write 03_字段标准对照表.csv

**Files:**
- Create: `project/CBHunter/03_字段标准对照表.csv`

**CSV structure:**
```csv
统一字段,Shopee字段,TikTok Shop字段,Temu字段,妙手ERP字段,国别差异化说明
product_title,商品名称,商品标题,商品名,listing_title,菲律宾用英文，泰国用泰文
product_price,售价,价格,供货价,price,币种差异：PHP/SGD/THB/VND/IDR
sku_spec,规格,SKU,规格,sku_spec,印尼需要HS编码
category_l1,一级类目,一级分类,品类,category_l1,各国类目树不同
commission_rate,佣金率,平台佣金,扣点,commission_rate,各国费率不同
tax_type,税种,税费,增值税,tax_type,泰国VAT 7%，印尼PPN 11%
```

**Requirements:**
- Cover all unified fields from research
- Map each platform's equivalent field names
- Document country-differentiated fields separately
- Include notes on special requirements per site

---

## Task 8: Write 04_UIUX交互设计指导.md

**Files:**
- Create: `project/CBHunter/04_UIUX交互设计指导.md`

**Content structure:**
```markdown
# CBHunter UI/UX交互设计指导

## 一、整体布局规范
### 1.1 三栏式布局（导航/列表/详情）
### 1.2 响应式设计原则

## 二、多平台多店铺产品管理页面
### 2.1 平台切换交互
### 2.2 店铺切换交互
### 2.3 商品树状视图
### 2.4 批量操作区

## 三、上架编辑页
### 3.1 基础信息区
### 3.2 图文素材区
### 3.3 SKU管理区
### 3.4 定价区
### 3.5 动态表单渲染

## 四、活动配置页
### 4.1 折扣活动配置
### 4.2 优惠券配置
### 4.3 秒杀配置

## 五、订单资金页
### 5.1 订单列表交互
### 5.2 交易明细展示
### 5.3 资金流水查看
```

**Requirements:**
- Document interaction patterns for each page type
- Specify button operations and logic
- Include popup/dialog field specifications
- Define validation rules

---

## Task 9: Write 05_开发建设指导意见.md

**Files:**
- Create: `project/CBHunter/05_开发建设指导意见.md`

**Content structure:**
```markdown
# CBHunter 开发建设指导意见

## 一、底层数据库设计
### 1.1 核心表结构
### 1.2 平台扩展表设计
### 1.3 国别配置表

## 二、接口层适配层设计
### 2.1 Adapter 模式设计
### 2.2 统一 API 定义
### 2.3 平台 SDK 封装

## 三、动态表单引擎
### 3.1 表单配置 schema
### 3.2 渲染器设计
### 3.3 校验规则引擎

## 四、多币种多费率计算引擎
### 4.1 汇率管理
### 4.2 费率配置
### 4.3 计算流程

## 五、分类树动态加载方案
### 5.1 分类缓存策略
### 5.2 懒加载机制
### 5.3 国别差异化处理
```

**Requirements:**
- Provide concrete database schema suggestions
- Document adapter interface design
- Specify dynamic form engine architecture
- Include multi-currency calculation logic
- Design category tree loading strategy

---

## Self-Review Checklist

After completing all tasks, verify:

- [ ] All 4 platforms researched with field-level detail
- [ ] All 5 deliverable documents created in project/CBHunter/
- [ ] Screenshots saved in project/CBHunter/screenshots/
- [ ] No placeholder content (TBD/TODO)
- [ ] Consistent terminology across documents
- [ ] Country differences properly documented
- [ ] CSV has complete field mappings
- [ ] Architecture recommendations are actionable

---

## Execution Handoff

Plan complete. Two execution options:

**1. Subagent-Driven (recommended)** - Dispatch fresh subagent per platform research task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?

# CBHunter 系统整体功能升级 & 架构重构建设总方案

> **项目**: CBHunter — 多平台跨境电商卖家后台  
> **文档类型**: 系统整体升级与架构重构总方案（唯一收口文档）  
> **版本**: v2.0  
> **日期**: 2026-07-21  
> **核心原则**: 统一底座 + 平台适配器 + 策略数据解耦 + 动态智能选品  
> **整合来源**: 01~10号调研设计文档全部有效内容

---

## 一、系统整体迭代背景

### 1.1 存量系统现状

CBHunter 已完成四平台（Shopee/TikTok Shop/TEMU/妙手ERP）深度调研，形成10份设计文档，覆盖：
- **多平台商品管理**：发布流程、类目体系、SKU/变体、定价模板、图片管理、批量编辑
- **订单/物流/资金**：全平台订单状态映射、物流渠道、多币种结算、合规要求
- **营销中心**：Shopee折扣/秒杀/优惠券/联盟、TikTok CRM/广告/直播、TEMU平台统一下发
- **多店铺同步**：账户→店铺组→站点→多店铺层级管理
- **图库素材**：主图/SKU图片、水印、批量编辑、易可图编辑器集成
- **字段标准**：110+字段的标准/非标准分类、跨平台映射规则
- **选品体系**：64条策略、四层架构、v2智能引擎、16张数据库表

### 1.2 存量系统主要缺陷

| 问题类型 | 具体表现 | 本次处理方式 |
|----------|----------|-------------|
| 平台适配不统一 | 各模块独立实现平台差异逻辑，无统一适配器层 | 统一「底座+适配器」架构 |
| 字段标准碎片化 | 同一概念在不同模块命名不一致（如价格、SKU、状态） | 建立全局字段标准字典 |
| 商品编辑模式混乱 | Shopee独立SPA、TikTok单页、TEMU多步骤、妙手弹窗 | 统一弹窗式编辑架构 |
| SKU模型不兼容 | 两层规格 vs TEMU三层SPU/SKC/SKU | 统一父级+变体组+SKU三层结构 |
| 定价引擎缺失 | Temu供货价/Shopee零售价/多币种混用 | 统一CNY存储+国别格式化 |
| 批量操作能力弱 | 缺少采集箱/待发布池概念 | 引入妙手采集箱模式 |
| 动态表单能力不足 | 类目选择后字段加载逻辑分散 | Schema驱动动态表单引擎 |
| 图片编辑器未集成 | 仅基础上传预览 | iframe组件化集成易可图 |
| 选品能力空白 | 无系统化选品策略和引擎 | 新增股票级量化选品器完整模块 |
| 业务链路断裂 | 选品→品控→定价→上架→出单→回款未闭环 | 打通全链路业务流 |
| UI/UX标准不统一 | 各平台页面布局、色彩、字体、间距各自为政 | 建立全局设计规范体系 |

### 1.3 本次升级目标

1. **归一化合并**：10份文档碎片化能力收口为**一套统一架构、一套统一标准、一套统一业务流程**
2. **补全升级**：旧模块缺陷用调研结果覆盖替换，补齐功能缺失
3. **新模块并入**：将智能量化选品器完整并入系统核心业务链路
4. **全链路闭环**：形成「选品→样品参考→素材库→商品编辑→定价模板→多店铺批量上架→同步管控→订单→回款」完整业务闭环
5. **架构统一**：多平台适配、字段标准、动态表单、批量操作、UI/UX全面统一

### 1.4 功能架构与业务架构

#### 1.4.1 全系统功能架构

```
CBHunter 全域跨境电商运营平台
├── 商品管理中心
│   ├── 商品列表（表格/卡片/树状三视图）
│   ├── 商品编辑（弹窗式，含5个Tab）
│   ├── 批量编辑（标题/图片/SKU/价格/类目）
│   ├── 采集箱/待发布池
│   ├── 素材图库
│   ├── 类目树管理
│   └── 商品草稿
│
├── 订单管理中心
│   ├── 订单列表（统一状态机）
│   ├── 订单详情（抽屉式）
│   ├── 批量出货/退货退款取消
│   ├── 物流设置/运费模板
│   └── 发货台/备货管理（TEMU）
│
├── 资金管理中心
│   ├── 资金概览（多币种统一CNY存储）
│   ├── 结算记录/对账单
│   ├── 收款账户管理
│   ├── 保证金管理
│   └── 借贷计划
│
├── 营销中心
│   ├── Shopee：折扣/秒杀/优惠券/联盟营销
│   ├── TikTok：CRM聊天营销/广告/联盟/直播
│   ├── TEMU：平台统一下发/爆款跟卖/机会商品
│   └── 妙手：折扣模板/自动置顶/加购优惠
│
├── 店铺管理中心
│   ├── 账户→店铺组→站点→多店铺层级
│   ├── 店铺授权/管理
│   ├── 子账号/权限管理
│   └── 跨店同步管控
│
├── 智能选品中心（新增）
│   ├── 选品器主工作区（四栏动态布局）
│   ├── 策略库（64条原生+复合策略）
│   ├── 运算引擎（交/并/差/加权）
│   ├── 智能面板（权重/负向筛选/AI推荐）
│   ├── 结果展示（候选商品池+标杆样例）
│   ├── 策略胜率回溯
│   ├── 策略市场
│   └── AI辅助策略生成
│
├── 数据分析中心
│   ├── 商业看板（各平台数据汇总）
│   ├── 销售趋势分析
│   ├── 流量分析
│   └── 选品胜率分析
│
├── 通知中心
│   ├── 全站消息
│   ├── 规则公告
│   ├── 合规警告
│   └── 系统通知
│
└── 系统设置
    ├── 国别配置
    ├── 汇率配置
    ├── 运费模板
    ├── 类目Schema管理
    ├── 数据源管理
    ├── 用户/角色权限
    └── 平台适配器配置
```

#### 1.4.2 业务架构（全链路闭环）

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CBHunter 业务全链路闭环                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  选品（流量挖掘）                                                    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 64条策略 → 复合组合 → 智能运算 → 候选商品池 → 标杆样例      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  素材（图片/视频收藏）                                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 标杆商品图片/视频 → 一键收藏到素材图库 → 作为编辑参考素材    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  品控（合规检查）                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ RC策略过滤 → 禁限售/知识产权/认证要求 → 合规信息补全         │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  定价（利润计算）                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ PF策略计算 → 成本/运费/佣金/税费/汇率 → CNY统一存储          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  上架（多平台发布）                                                   │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 商品编辑弹窗 → 动态表单 → 平台适配器 → 批量上架 → 多店同步   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  出单（订单处理）                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 订单同步 → 统一状态机 → 批量出货 → 物流同步 → 退货退款处理   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  回款（资金结算）                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 多币种结算 → CNY统一存储 → 佣金扣除 → 提现 → 对账单         │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│  验证（选品胜率回溯）                                                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 商品实际表现 → 命中率/首月销量/毛利率/复购率 → 策略胜率更新  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          ↓                                          │
│              反馈至选品器：优化策略权重和参数                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.4.3 模块依赖关系

```
核心依赖链：
  店铺管理 → 商品管理 → 订单管理 → 资金管理
       ↘    素材图库 ← 选品引擎          ↘
        → 权限管理 ← 数据源管理           → 物流管理

选品引擎依赖：
  策略库 → 运算引擎 → 数据源映射 → 数据采集层
       ↗              ↘
  权重系统            负向筛选
       ↘              ↗
  胜率统计 ← 选品任务执行结果
```

---

## 二、全局统一技术架构

### 2.1 总体分层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CBHunter 前端应用层                           │
│  React + TypeScript | Zustand/Redux | Ant Design / Element Plus     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    共享UI组件层                               │   │
│  │  商品列表 | 订单卡片 | 资金面板 | 动态表单引擎 | 筛选器        │   │
│  │  CurrencyDisplay | CategorySelector | FieldRenderer           │   │
│  │  OrderStatusBadge | PlatformIcon | BatchOperationBar          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    业务逻辑层（统一底座）                      │   │
│  │                                                             │   │
│  │  商品管理 | 订单管理 | 资金管理 | 营销管理 | 物流管理          │   │
│  │  店铺管理 | 权限管理 | 通知中心 | 数据看板 | 素材图库          │   │
│  │  选品引擎 | 策略市场 | 胜率分析 | AI辅助生成                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    平台适配器层                              │   │
│  │  ShopeeAdapter | TikTokShopAdapter | TemuAdapter | MiaoshouAdapter │ │
│  │                                                             │   │
│  │  • 字段映射（platform_extensions JSONB）                      │   │
│  │  • 流程编排（发布/编辑/状态机）                                │   │
│  │  • 国别配置（currency/tax/logistics/category_tree）            │   │
│  │  • 权限策略（跨境店/本地店/全托管/半托管）                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    数据层（Unified Data Model）               │   │
│  │  标准字段 | 扩展字段(JSONB) | 国别差异字段 | 平台元数据         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 核心设计原则

| 原则 | 说明 |
|------|------|
| **统一底座** | 通用业务流程和UI交互在底座层实现，不重复开发 |
| **平台适配器** | 各平台特有概念通过适配器注入，底座不感知平台差异 |
| **数据解耦** | 策略层与数据源层彻底解耦，D级策略可正常配置组合 |
| **Schema驱动** | 动态表单由JSON Schema驱动，类目选择后自动加载差异化字段 |
| **国别隔离** | 货币/汇率/税费/物流/类目按国别配置，不硬编码在前端 |
| **只读优先** | Chrome DevTools MCP只读爬取公域数据，涉及资金和发布需人工确认 |
| **增量升级** | 保留v1有效内容，只做补全、修正、重构、新增 |

### 2.3 多平台适配架构

```typescript
interface PlatformAdapter {
  // 字段映射：统一商品对象 → 平台特定字段
  mapFieldsToPlatform(product: UnifiedProduct): PlatformSpecificFields;
  
  // 平台特有字段Schema
  getPlatformExtensions(): PlatformExtensionSchema;
  
  // 验证规则
  validate(product: UnifiedProduct): ValidationResult;
  
  // 提交到平台
  submitToPlatform(data: PlatformSpecificFields): Promise<SubmitResult>;
  
  // 同步平台变更回CBHunter
  syncFromPlatform(platformData: any): UnifiedProduct;
  
  // 国别配置
  getCountryConfigs(countryCode: string): CountryConfig;
}
```

**适配器职责边界**：
- 适配器**只负责**字段映射、流程编排、国别配置、权限策略
- 适配器**不直接访问**业务数据表，通过统一数据模型交互
- 新增平台只需实现适配器接口，**无需修改底座代码**

### 2.4 平台适配器完整接口定义（来自05_开发建设指导意见）

> 以下为 `IPlatformAdapter` 完整方法签名，涵盖商品、类目、订单、营销、资金、权限、弹窗编辑七大能力域。各平台适配器必须实现全部方法。

```typescript
// 平台适配器基础接口（完整版）
interface IPlatformAdapter {
    // === 平台元信息 ===
    getPlatformCode(): string;
    getPlatformName(): string;

    // === 商品操作 ===
    getProductList(params: ProductQueryParams): Promise<ProductPage>;
    getProductDetail(productId: string): Promise<ProductDetail>;
    createProduct(product: UnifiedProduct): Promise<PlatformProductResult>;
    updateProduct(productId: string, product: Partial<UnifiedProduct>): Promise<PlatformProductResult>;
    deleteProduct(productId: string): Promise<boolean>;

    // === 类目系统 ===
    getCategoryTree(countryCode: string): Promise<CategoryNode[]>;
    getCategoryFields(categoryId: string, countryCode: string): Promise<FieldSchema[]>;

    // === 订单操作 ===
    getOrderList(params: OrderQueryParams): Promise<OrderPage>;
    getOrderDetail(orderId: string): Promise<OrderDetail>;
    shipOrder(orderId: string, trackingNumber: string): Promise<boolean>;

    // === 营销操作 ===
    createCampaign(campaign: CampaignConfig): Promise<CampaignResult>;
    getVoucherList(): Promise<Voucher[]>;
    getFlashSaleEligibility(): Promise<FlashSaleEligibility>;

    // === 资金操作 ===
    getIncomeSummary(): Promise<FinanceSummary>;
    getTransactionHistory(params: FinanceQueryParams): Promise<TransactionPage>;

    // === 权限检查 ===
    checkPermission(module: string): Promise<PermissionResult>;

    // === 弹窗编辑支持 ===
    getEditFormSchema(countryCode: string): Promise<FormSchema>;
    validateEditPayload(payload: any): Promise<ValidationResult>;
}
```

**Shopee Adapter 实现要点**：
```typescript
class ShopeeAdapter implements IPlatformAdapter {
    private baseUrl = 'https://api.shopee.cn';
    private region: string; // PH/SG/MY/TH/VN/ID

    async getCategoryTree(countryCode: string): Promise<CategoryNode[]> {
        const cacheKey = `shopee:category:${countryCode}`;
        return this.cache.getOrFetch(cacheKey, () =>
            this.api.get('/portal/product/category/tree')
        );
    }

    async getProductList(params: ProductQueryParams): Promise<ProductPage> {
        // 处理Shopee特有的SSP/Hot Listing标签
        const response = await this.api.get('/portal/product/list/all', { params });
        return this.mapToUnifiedProduct(response.data);
    }

    async createProduct(product: UnifiedProduct): Promise<PlatformProductResult> {
        // Shopee四步上架流程：基本信息→销售资料→运费→其他
        const basicInfo = this.extractBasicInfo(product);
        const salesInfo = this.extractSalesInfo(product);
        const shipping = this.extractShipping(product);
        const other = this.extractOther(product);
        return this.api.post('/portal/mtsku/new', { basicInfo, salesInfo, shipping, other });
    }
}
```

**TikTok Shop Adapter 实现要点**：
```typescript
class TikTokShopAdapter implements IPlatformAdapter {
    private baseUrl = 'https://seller.tiktokshopglobalselling.com';
    private region: string; // PH/SG/MY/TH/VN/ID/UK/US

    async checkPermission(module: string): Promise<PermissionResult> {
        // TikTok跨境账号部分模块无权限，需检测并返回友好权限结果
        try {
            await this.api.get(`/promotion`);
            return { allowed: true };
        } catch (error) {
            if (error.status === 403) {
                return {
                    allowed: false,
                    reason: '跨境店铺账号缺少此模块权限',
                    requirement: '需要主账号管理员授权'
                };
            }
            throw error;
        }
    }

    async getSPSScore(): Promise<number> {
        // 获取卖家体验分，用于CRM门槛判断（SPS≥3.5+GMV>0）
        const response = await this.api.get('/crm/stats');
        return response.data.spsScore;
    }

    async getChatPlanTemplates(): Promise<ChatPlanTemplate[]> {
        // 一次性计划 + 自动计划模板
        const [oneTime, auto] = await Promise.all([
            this.api.get('/crm/templates/one-time'),
            this.api.get('/crm/templates/auto')
        ]);
        return [...oneTime, ...auto];
    }
}
```

**TEMU Adapter 实现要点**：
```typescript
class TemuAdapter implements IPlatformAdapter {
    private baseUrl = 'https://agentseller.temu.com';

    async getProductList(params: ProductQueryParams): Promise<ProductPage> {
        // Temu SPU/SKC/SKU三层结构
        const response = await this.api.get('/goods/list', { params });
        return this.mapTemuProduct(response.data);
    }

    mapTemuProduct(data: any): UnifiedProduct {
        return {
            spuId: data.spuId,
            skcId: data.skcId,
            supplyPriceCny: data.supplyPriceCny,
            priceStatus: data.priceStatus,
            suggestedRetailPrice: data.suggestedRetailPrice,
            warehouseGroup: data.warehouseGroup,
            stockingLogic: data.stockingLogic,
        };
    }

    async getComplianceStatus(): Promise<ComplianceStatus> {
        // Temu强制合规项：资质/实拍图/合规信息
        return {
            qualification: await this.checkQualification(),
            livePhotos: await this.checkLivePhotos(),
            complianceInfo: await this.checkComplianceInfo()
        };
    }

    async getInventoryData(spuId: string): Promise<InventoryData> {
        // 仓内库存 + 卖家仓库存 + 销售趋势
        const [warehouse, seller, trend] = await Promise.all([
            this.api.get(`/inventory/warehouse/${spuId}`),
            this.api.get(`/inventory/seller/${spuId}`),
            this.api.get(`/sales/trend/${spuId}`)
        ]);
        return { warehouse, seller, trend };
    }
}
```

**商品对象到平台对象的映射器**：
```typescript
class ProductMapper {
    toShopee(product: UnifiedProduct, shop: Shop): ShopeeProduct {
        return {
            title: product.title,
            description: product.description,
            images: product.images,
            categoryPath: product.categoryPath,
            skus: product.skus.map(sku => ({
                sellerSkuCode: sku.sellerSkuCode,
                price: this.convertCurrency(sku.priceCny, shop.currencyCode),
                stock: sku.stockQty,
                attributes: sku.variantAttributes
            })),
            sspId: product.extensions?.sspId,
            hotListingStatus: product.extensions?.hotListingStatus
        };
    }

    toTikTok(product: UnifiedProduct, shop: Shop): TikTokProduct {
        return {
            title: product.title,
            description: product.description,
            images: product.images,
            videos: product.videoUrl ? [product.videoUrl] : [],
            categoryPath: product.categoryPath,
            skus: product.skus.map(sku => ({
                sellerSkuCode: sku.sellerSkuCode,
                price: this.convertCurrency(sku.priceCny, shop.currencyCode),
                stock: sku.stockQty
            }))
        };
    }

    toTemu(product: UnifiedProduct, shop: Shop): TemuProduct {
        return {
            title: product.title,
            description: product.description,
            images: product.images,
            categoryPath: product.categoryPath,
            spuId: product.spuId || this.generateSPUId(),
            skcId: product.skcId || this.generateSKCId(),
            skus: product.skus.map(sku => ({
                skuId: sku.skuId,
                supplyPriceCny: sku.supplyPriceCny || sku.priceCny,
                dimensions: sku.dimensions,
                weightG: sku.weightG,
                stock: sku.stockQty,
                isSensitive: sku.isSensitive
            }))
        };
    }
}
```

### 2.5 动态表单引擎实现（来自05_开发建设指导意见）

> 动态表单引擎采用 Schema Parser → Field Renderer → Validator → Submitter 四层架构，由 JSON Schema 驱动渲染。

```
┌─────────────────────────────────────────────────────────────┐
│                    Dynamic Form Engine                       │
├─────────────────────────────────────────────────────────────┤
│  Schema Parser → Field Renderer → Validator → Submitter     │
├─────────────────────────────────────────────────────────────┤
│  Platform Schema Registry                                   │
│  - Shopee: category → fields mapping                        │
│  - TikTok: category → fields mapping                        │
│  - Temu: category → fields mapping                          │
│  - Country Config: locale-specific fields                   │
└─────────────────────────────────────────────────────────────┘
```

**表单Schema定义示例**：
```json
{
  "formVersion": "1.0",
  "platform": "shopee",
  "country": "PH",
  "steps": [
    {
      "stepId": "basic_info",
      "title": "基本信息",
      "fields": [
        { "fieldId": "images", "type": "image_upload", "required": true, "maxCount": 9 },
        { "fieldId": "video", "type": "video_upload", "maxSize": 30, "format": "mp4" },
        { "fieldId": "title", "type": "text_input", "maxLength": 180, "required": true },
        { "fieldId": "category", "type": "category_selector", "level": 3 },
        { "fieldId": "description", "type": "textarea", "maxLength": 5000 }
      ]
    },
    {
      "stepId": "sales_info",
      "title": "销售资料",
      "dependsOn": { "fieldId": "category", "notEmpty": true },
      "dynamicFields": true,
      "fields": [
        { "fieldId": "skus", "type": "dynamic_array", "items": { "type": "object" } },
        { "fieldId": "attributes", "type": "dynamic_category_attributes" }
      ]
    },
    {
      "stepId": "shipping",
      "title": "运费",
      "fields": [
        { "fieldId": "shippingChannel", "type": "select", "dataSource": "platform_config.shipping_channels" },
        { "fieldId": "weight", "type": "number", "min": 0 },
        { "fieldId": "dimensions", "type": "dimension_input" }
      ]
    },
    {
      "stepId": "other",
      "title": "其他",
      "fields": [
        { "fieldId": "certifications", "type": "dynamic_certifications" },
        { "fieldId": "customFields", "type": "dynamic_array" }
      ]
    }
  ]
}
```

**DynamicFormEngine TypeScript 实现**：
```typescript
class DynamicFormEngine {
    private schemaRegistry: Map<string, FormSchema>;

    renderForm(schemaId: string, context: FormContext): ReactNode[] {
        const schema = this.schemaRegistry.get(schemaId);
        if (!schema) throw new Error(`Schema not found: ${schemaId}`);

        return schema.steps.map(step => {
            if (step.dependsOn && !this.evaluateCondition(step.dependsOn, context)) {
                return <Placeholder message="在您选择了商品类目后更新" />;
            }

            const staticFields = step.fields
                .filter(f => !f.dynamicFields)
                .map(field => this.renderField(field, context));

            let dynamicFields = [];
            if (step.dynamicFields && context.categoryId) {
                dynamicFields = this.loadCategoryFields(
                    context.platformCode,
                    context.countryCode,
                    context.categoryId
                );
            }

            return <StepPanel title={step.title}>
                {[...staticFields, ...dynamicFields]}
            </StepPanel>;
        });
    }

    validateForm(schema: FormSchema, formData: FormData): ValidationResult {
        const errors: ValidationError[] = [];
        for (const step of schema.steps) {
            for (const field of step.fields) {
                const value = formData[field.fieldId];
                if (field.required && !value) {
                    errors.push({ fieldId: field.fieldId, message: `${field.label} 是必填项` });
                    continue;
                }
                if (value && !this.validateType(field.type, value)) {
                    errors.push({ fieldId: field.fieldId, message: `${field.label} 格式不正确` });
                }
                if (field.maxLength && String(value).length > field.maxLength) {
                    errors.push({ fieldId: field.fieldId, message: `${field.label} 最多${field.maxLength}个字符` });
                }
                if (field.min !== undefined && Number(value) < field.min) {
                    errors.push({ fieldId: field.fieldId, message: `${field.label} 不能小于${field.min}` });
                }
                if (field.platformValidation) {
                    const platformError = field.platformValidation(value, formData);
                    if (platformError) {
                        errors.push({ fieldId: field.fieldId, message: platformError });
                    }
                }
            }
        }
        return { valid: errors.length === 0, errors };
    }
}
```

**类目属性动态加载器**：
```typescript
class CategoryFieldLoader {
    async loadCategoryFields(
        platformCode: string,
        countryCode: string,
        categoryId: string
    ): Promise<FieldSchema[]> {
        const cacheKey = `${platformCode}:${countryCode}:fields:${categoryId}`;
        return this.cache.getOrFetch(cacheKey, async () => {
            const adapter = this.adapterFactory.getAdapter(platformCode);
            const fields = await adapter.getCategoryFields(categoryId, countryCode);
            const localeFields = this.getLocaleSpecificFields(platformCode, countryCode);
            return [...fields, ...localeFields];
        });
    }

    private getLocaleSpecificFields(platformCode: string, countryCode: string): FieldSchema[] {
        const fields: FieldSchema[] = [];
        // Shopee菲律宾站：NCC认证
        if (platformCode === 'shopee' && countryCode === 'PH') {
            fields.push({ fieldId: 'ncc_certification', type: 'text_input', label: 'NCC认证型号' });
        }
        // Temu全托管：强制合规字段
        if (platformCode === 'temu') {
            fields.push(
                { fieldId: 'qualification_doc', type: 'file_upload', label: '商品资质文件', required: true },
                { fieldId: 'live_photo', type: 'image_upload', label: '商品实拍图', required: true, minCount: 3 },
                { fieldId: 'compliance_info', type: 'textarea', label: '商品合规信息', required: true }
            );
        }
        return fields;
    }
}
```

### 2.6 多币种多费率计算引擎（来自05_开发建设指导意见）

> 定价引擎统一以CNY存储，展示层按站点货币格式化。费用计算引擎处理佣金、支付手续费、退款扣除等。

**汇率管理服务**：
```typescript
class ExchangeRateService {
    private rateCache: Map<string, { rate: number; updatedAt: Date }>;

    async getExchangeRate(fromCurrency: string, toCurrency: string): Promise<number> {
        if (fromCurrency === toCurrency) return 1;
        const cacheKey = `${fromCurrency}_${toCurrency}`;
        const cached = this.rateCache.get(cacheKey);
        // 5分钟缓存
        if (cached && (Date.now() - cached.updatedAt.getTime()) < 5 * 60 * 1000) {
            return cached.rate;
        }
        const rate = await this.financeApi.getExchangeRate(fromCurrency, toCurrency);
        this.rateCache.set(cacheKey, { rate, updatedAt: new Date() });
        return rate;
    }

    async convertAmount(amount: number, fromCurrency: string, toCurrency: string): Promise<number> {
        const rate = await this.getExchangeRate(fromCurrency, toCurrency);
        return Math.round(amount * rate * 100) / 100;
    }
}
```

**费用计算引擎**：
```typescript
interface FeeCalculationResult {
    productAmountLocal: number;
    shippingFee: number;
    platformCommission: number;
    paymentFee: number;
    refundDeduction: number;
    totalFee: number;
    netAmount: number;
    currencyCode: string;
}

class FeeCalculator {
    async calculate(order: Order, shop: Shop): Promise<FeeCalculationResult> {
        const currencyCode = shop.currencyCode;
        const productAmount = this.sumOrderItems(order.items);
        const shippingFee = await this.calculateShippingFee(order.shippingChannel, order.items, shop.countryCode);
        const platformCommission = this.calculateCommission(productAmount, shop.platformCode, shop.countryCode);
        const paymentFee = this.calculatePaymentFee(productAmount, order.paymentMethod, shop.countryCode);
        const refundDeduction = order.returnRefundId
            ? await this.getRefundDeduction(order.returnRefundId) : 0;
        const totalFee = platformCommission + paymentFee + refundDeduction;
        const netAmount = productAmount - totalFee;
        return { productAmountLocal: productAmount, shippingFee, platformCommission, paymentFee, refundDeduction, totalFee, netAmount, currencyCode };
    }

    private calculateCommission(amount: number, platformCode: string, countryCode: string): number {
        // 各平台各站点佣金率不同
        const commissionRates: Record<string, Record<string, number>> = {
            shopee: { PH: 0.05, SG: 0.06, MY: 0.05, TH: 0.05 },
            tiktok: { PH: 0.04, SG: 0.05 },
            temu: { CN: 0.08 }
        };
        const platformRate = commissionRates[platformCode]?.[countryCode] ?? 0.05;
        return Math.round(amount * platformRate * 100) / 100;
    }

    private calculatePaymentFee(amount: number, paymentMethod: string, countryCode: string): number {
        // COD手续费2%，电子钱包1%
        if (paymentMethod === 'COD') return Math.round(amount * 0.02 * 100) / 100;
        if (['SPayLater', 'MariBank Savings'].includes(paymentMethod)) return Math.round(amount * 0.01 * 100) / 100;
        return 0;
    }
}
```

**多币种显示格式化**：
```typescript
class CurrencyFormatter {
    format(amount: number, currencyCode: string, locale?: string): string {
        const symbols: Record<string, string> = {
            PHP: '₱', SGD: 'S$', MYR: 'RM', THB: '฿',
            VND: '₫', IDR: 'Rp', GBP: '£', USD: '$', CNY: '¥'
        };
        const symbol = symbols[currencyCode] || currencyCode;
        const localeMap: Record<string, string> = {
            PHP: 'fil-PH', SGD: 'en-SG', MYR: 'ms-MY',
            THB: 'th-TH', VND: 'vi-VN', IDR: 'id-ID',
            GBP: 'en-GB', USD: 'en-US', CNY: 'zh-CN'
        };
        return new Intl.NumberFormat(localeMap[currencyCode], {
            style: 'currency',
            currency: currencyCode,
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }
}
// 示例输出：₱429.00 / S$12.50 / RM 25.00 / ฿150.00 / ₫50,000.00 / Rp 150.000,00 / £25.00 / $12.50 / ¥14.80
```

### 2.7 安全与合规要求（来自05_开发建设指导意见）

#### 2.7.1 数据安全

| 措施 | 说明 |
|------|------|
| 敏感数据加密 | 平台授权Token、用户密码使用AES-256加密存储 |
| HTTPS传输 | 所有API通信强制HTTPS |
| 输入校验 | 前后端双重校验，防止SQL注入/XSS |
| 速率限制 | API限流，防止恶意爬取 |
| 审计日志 | 记录所有敏感操作 |

#### 2.7.2 只读优先原则

| 原则 | 实施 |
|------|------|
| 默认只读 | 所有平台适配器默认只读模式 |
| 写操作确认 | 涉及发布、修改、删除的操作必须有二次确认弹窗 |
| 权限隔离 | 子账号权限继承自平台授权，CBHunter不额外赋予写权限 |
| 操作日志 | 所有写操作记录完整日志，可追溯 |
| 资金保护 | 资金相关操作（提现、转账）必须人工确认，禁止自动执行 |

#### 2.7.3 各平台合规要求

| 平台 | 合规要求 |
|------|----------|
| Shopee | 商品资质、实拍图（部分类目）、NCC/Anatel认证（按国别） |
| TikTok Shop | 内容审核、直播规范、广告合规 |
| TEMU | 强制资质上传、实拍图、合规信息、建议零售价合规 |
| 通用 | GDPR（欧盟站点）、各国电商法规、税务合规 |

### 2.8 性能优化策略（来自05_开发建设指导意见）

#### 2.8.1 前端性能

| 优化项 | 措施 |
|--------|------|
| 懒加载 | 商品图片懒加载、类目树按需加载 |
| 虚拟滚动 | 长列表使用虚拟滚动（react-virtuoso） |
| 缓存策略 | 类目树、平台配置、汇率数据缓存 |
| 代码分割 | 按平台/模块分割代码，减少首屏加载 |
| PWA | 支持离线访问基础功能 |

#### 2.8.2 后端性能

| 优化项 | 措施 |
|--------|------|
| 数据库索引 | 核心查询字段建立索引 |
| 查询优化 | N+1查询避免、批量查询 |
| 缓存策略 | Redis缓存热点数据 |
| 异步处理 | 耗时操作（发布、同步）异步处理 |
| 分页查询 | 所有列表接口支持分页 |

#### 2.8.3 平台API限流应对

| 策略 | 说明 |
|------|------|
| 请求队列 | 平台API请求排队，避免并发超限 |
| 指数退避 | API限流时指数退避重试 |
| 本地缓存 | 平台数据本地缓存，减少重复请求 |
| 增量同步 | 仅同步变更数据，避免全量拉取 |

---

## 三、全业务模块整合升级详情

### 3.1 商品管理模块

#### 3.1.1 统一商品数据模型

```
Product（商品主表）
├── standard_fields（标准字段，JSONB）
│   ├── title: string              // 商品名称，最多180字符
│   ├── description: text          // 商品描述，最多5000字符
│   ├── images: array              // 主图+附图，最多9张
│   ├── video_url: string          // 视频，Max 30MB MP4
│   ├── category_path: string[]    // 三级类目路径 L1/L2/L3
│   ├── brand: string              // 品牌
│   ├── listing_status: enum       // 上架状态
│   └── created_at / updated_at
├── sku_table（SKU子表）
│   ├── sku_id: string             // 平台SKU ID / Model ID
│   ├── seller_sku_code: string    // 商家货号 / 规格货号
│   ├── variant_attrs: jsonb       // 规格属性（规格一/规格二）
│   ├── price_cny: decimal         // 统一CNY存储
│   ├── stock_qty: integer         // 库存数量
│   ├── dimensions: jsonb          // 长宽高（cm），TEMU必填
│   ├── weight_g: integer          // 重量（g），TEMU必填
│   ├── images: array              // SKU级别图片
│   └── status: enum               // 提交成功/待审核等
├── platform_extension（平台扩展字段，JSONB）
│   ├── platform_code: shopee/tiktok temu
│   ├── ssp_id / hot_listing_status / smart_diagnosis_status  // Shopee
│   ├── sps_score / crm_enabled / live_stream_id              // TikTok
│   ├── spu_id / skc_id / supply_price_cny / price_status     // TEMU
│   ├── warehouse_group / stocking_logic / daily_posting_quota  // TEMU
│   ├── qualification_status / compliance_info_status          // TEMU
│   └── custom_fields: jsonb
└── country_config（国别配置）
    ├── currency_code: string        // PHP/SGD/MYR/THB/VND/IDR/TWD/GBP/USD/CNY
    ├── currency_symbol: string      // ₱/S$/RM/฿/₫/Rp/NT$/£/$/¥
    ├── tax_rate: decimal            // 各国税率不同
    ├── logistics_channels: jsonb    // 各站点物流渠道不同
    ├── payment_methods: jsonb       // 各站点支付方式不同
    └── shop_region: enum            // 本地店/跨境店/全托管/半托管
```

#### 3.1.2 统一底座 + 平台差异化处理

| 维度 | 统一底座处理 | 平台适配器差异 |
|------|-------------|---------------|
| **商品创建流程** | 选类目→基本信息→销售资料→运费→其他→预览发布 | Shopee四步/TEMU两步/TikTok单页/妙手标签页 |
| **类目系统** | 三级类目树（L1/L2/L3） | 各平台类目树独立维护，选择后动态加载字段 |
| **SKU管理** | 父级商品+变体组+SKU三层结构 | Shopee/TikTok两层规格；TEMU三层SPU→SKC→SKU |
| **定价** | 统一CNY存储 | Shopee/TikTok零售价(站点币)；TEMU供货价(CNY)；妙手货源价+售价 |
| **图片** | 主图+SKU图片管理 | 各平台最多9张；妙手支持批量编辑10张 |
| **状态机** | 草稿→待审核→已发布→已下架 | 各平台状态值不同，适配器做映射 |
| **合规** | 统一合规检查入口 | TEMU强制合规最严，Shopee/TikTok相对宽松 |

#### 3.1.3 编辑模式统一：弹窗式编辑

```
产品列表页
└── 编辑弹窗（ElDialog / Ant Design Modal）
    ├── 左侧：步骤导航（Shopee风格）或 标签页（妙手风格）
    ├── 右侧：表单内容区
    │   ├── 基本信息标签页（标题/描述/图片/视频/类目/品牌）
    │   ├── 销售资料标签页（SKU/变体/定价/库存/分类属性）
    │   ├── 图片管理标签页（主图+SKU图片+批量编辑）
    │   ├── 物流设置标签页（运费模板/重量尺寸/物流渠道）
    │   └── 其他属性标签页（自定义字段/合规信息/认证要求）
    └── 底部操作栏：保存草稿 | 创建/更新 | 发布
        └── iframe: 图片编辑器组件（可配置接入易可图或自研）
```

**优势**：
1. 批量操作友好：弹窗内可直接编辑多个商品
2. 上下文保持：用户不离开列表页，操作效率高
3. 模块化扩展：图片编辑器作为独立iframe组件嵌入
4. 平台适配灵活：各平台适配器可独立控制弹窗内的字段显示

#### 3.1.4 动态表单引擎

```
类目选择 → 加载类目属性Schema → 渲染动态表单
                ↓
        平台适配器注入额外字段
                ↓
        国别配置注入本地化字段
                ↓
        表单验证规则生成
                ↓
        提交 → 平台适配器校验 → 提交到平台
```

**关键实现点**：
- Schema驱动：每个类目的属性定义存储为JSON Schema
- 平台适配器注入：Shopee注入SSP/Hot Listing字段，TEMU注入SPU/SKC/供货价字段
- 国别配置注入：货币、税费、物流渠道按站点动态切换
- 验证规则自动生成：根据Schema和平台规则生成前端验证

#### 3.1.5 SKU/变体管理设计

**支持两种模式**：

1. **简单模式（Shopee/TikTok/妙手风格）**：
   - 规格一、规格二两行定义
   - SKU生成规则：货源ID + 规格1 + 规格2，分隔符可配
   
2. **三层模式（TEMU风格）**：
   - SPU → SKC → SKU
   - CBHunter内部统一用父级商品+变体组+SKU三层结构

**SKU图片管理**：
- 主图：商品级，最多9张
- SKU图片：SKU级别，支持拖拽排序
- 批量上传：支持Excel导入SKU图片映射

**超限保护**：超过100个SKU时提示而非自动删除

#### 3.1.6 批量编辑功能设计

| 功能 | 实现方式 |
|------|----------|
| 批量标题优化 | AI自动优化/关键词随机组合 |
| 批量图片编辑 | 调用图片编辑器批量处理（最多10张） |
| 批量SKU修改 | 表格内直接编辑 |
| 批量价格调整 | 公式计算（如统一加价10%） |
| 批量类目设置 | 类目选择器 |
| Excel粘贴支持 | 产品标题搜索支持逗号分隔和Excel复制粘贴 |

#### 3.1.7 采集箱/待发布池

参考妙手ERP的采集箱设计：
- 7种采集方式：链接采集、1688跨境热卖、导入采集、关键词采集、整店采集、插件采集、店铺互采
- 采集箱页面：筛选（关联货源/货源店铺/店铺/货源价格/标记/产品标题）、批量操作（批量发布/设置类目/设置售价/批量编辑/引用模板/分组/创建产品）
- 状态标签：全部/未发布/定时发布/已发布
- 三态管理：未发布→定时发布→已发布

### 3.2 订单管理模块

#### 3.2.1 统一订单数据模型

```
Order（订单主表）
├── order_id: string               // 平台原始订单号
├── buyer_name: string             // 买家名称
├── order_items: jsonb             // 订单商品明细
│   ├── product_title: string
│   ├── sku_spec: string           // 规格/颜色
│   ├── quantity: integer
│   └── amount: decimal            // 金额
├── total_amount: decimal          // 总金额（统一CNY存储）
├── payment_method: string         // 支付方式（适配器映射）
├── order_status: enum             // 统一状态机
│   ├── pending_payment            // 待付款
│   ├── pending_ship               // 待出货/To Process
│   ├── shipping                   // 运送中/To Ship
│   ├── completed                  // 已完成
│   └── cancelled_refunded         // 退货退款取消/Cancelled
├── shipping_channel: string       // 物流渠道
├── tracking_number: string        // 运单号
├── dispatch_deadline: datetime    // 发货截止时间
├── platform_code: string          // shopee/tiktok temu
├── country_code: string           // PH/SG/MY/TH/VN/ID/TW/US/UK
├── shop_id: string                // 店铺ID
└── created_at / updated_at
```

#### 3.2.2 订单状态映射表

**统一状态机完整映射**：

| 统一状态 | Shopee | TikTok Shop | TEMU |
|----------|--------|-------------|------|
| 待付款 | Pending Payment | Pending Payment | — |
| 待审单 | — | To Process（TikTok独有审单环节） | 待审核备货 |
| 待出货 | To Ship | To Ship | 申请备货 |
| 已发货 | Shipped | Shipped | 已发货/在途 |
| 已完成 | Completed | Completed | 履约完成 |
| 待评价 | — | To Review（TikTok独有评价环节） | — |
| 退货退款取消 | Refund/Return Cancelled | Cancelled/Refund/Return | 退货申请/退货包裹管理 |
| 已取消 | — | Cancelled | — |

**TikTok Shop订单状态完整流转**：
```
Pending Payment → To Process（审单）→ To Ship → Shipped → Completed
                         ↓              ↓
                    Cancelled      Refund/Return
                         ↓
                    To Review（待评价）→ Completed（评价后）
```

**Shopee订单支付方式枚举**：
- MariBank Savings、货到付款 COD、SPayLater、线上支付、线下支付、钱包余额
- 各站点支付方式不同，country_config.payment_methods 存储站点级配置

**Shopee物流渠道枚举**：
- Express International（快速渠道）、Standard International（标准国际）、FBP（Fulfilled by Shopee）
- 物流设置路径：`/portal/all-settings/shipping/shipping-channel`

**TEMU订单管理子模块（13项）**：
退货申请、退货包裹管理、收货/入库异常处理、保税仓退货管理、发货台、申请备货、商家自发货、平台发货、物流轨迹、运单管理、司机管理、地址管理、对账结算

**TEMU商品管理子模块（30+项）**：
商品列表、创建商品、商品体检、商品优化事项、供货价管理、库存管理（仓内可用/预占用/暂不可用/已发货/待审核备货/卖家仓建议）、商品条码管理、质量管理（体检中心/送检包裹/样品管理/拍摄退样/精修任务/说明书制作/零售价合规中心）、合规信息、敏感属性、SPU/SKC管理

**TEMU站点选择器**：全球 / 美国 / 欧区

**TEMU商品优化事项完整清单**：
- 高价商品流量下降中
- 建议零售价待填写
- 商品分类错误待修正
- 流量扶持待领取
- 传视频得免费流量加权
- 申报价格待关注

### 3.3 资金管理模块

#### 3.3.1 多币种统一处理

| 平台 | 结算货币 | 存储方式 | 显示方式 |
|------|----------|----------|----------|
| Shopee | 站点本地币（PHP/SGD/MYR等） | 统一CNY存储 | 按站点格式化 |
| TikTok | 站点本地币 | 统一CNY存储 | 按站点格式化 |
| TEMU | CNY | CNY存储 | CNY显示 |
| 妙手 | 多币种 | 统一CNY存储 | 按站点格式化 |

**汇率处理**：
- 统一CNY存储，显示层按站点格式化
- 汇率按日更新，支持手动覆盖
- TEMU固定CNY，无需汇率转换

#### 3.3.2 资金模块字段

```
FinanceRecord（资金记录）
├── record_id: string
├── shop_id: string
├── platform_code: string
├── country_code: string
├── amount_cny: decimal            // 统一CNY
├── amount_local: decimal          // 站点本地币
├── currency_code: string
├── transaction_type: enum         // 收入/退款/佣金/服务费/保证金
├── settlement_date: date          // 结算日期
├── source_order_id: string        // 关联订单
├── description: string            // 备注
└── created_at
```

### 3.4 物流管理模块

#### 3.4.1 各平台物流差异

| 平台 | 物流模式 | 物流渠道 | 特殊要求 |
|------|----------|----------|----------|
| Shopee | 卖家/FBP混合 | Express International / Standard International | 海外免退服务 |
| TikTok | 卖家/SLS混合 | 平台推荐物流渠道 | 跨境时效因站点不同 |
| TEMU | 平台仓配送 | 备货仓组 | JIT/VMI模式、司机/地址管理 |
| 妙手 | 对接多物流 | 物流单号 | 发货天数配置 |

#### 3.4.2 TEMU备货逻辑

- 仓内库存：可用/预占用/暂不可用/已发货/待发货/待审核/实物库存
- 卖家仓库存：建议目标库存天数、建议目标库存、建议生产/采购量
- 备货逻辑：JIT（按单采购）/ VMI（供应商管理库存）
- 发品额度：每日400个

### 3.5 营销中心模块

#### 3.5.1 各平台营销活动

| 平台 | 营销活动 | 说明 |
|------|----------|------|
| Shopee | 折扣活动、店内秒杀、8种优惠券、联盟营销 | 最丰富，含回购买家券/关注礼券 |
| TikTok | 聊天营销(CRM)、广告营销、联盟、直播/短视频 | CRM门槛：SPS≥3.5+GMV>0 |
| TEMU | 平台统一下发、爆款跟卖、机会商品推荐 | 全托管模式，营销由平台主导 |

#### 3.5.2 TikTok CRM特色

- **一次性计划7种**：分享热销商品、新品上市公告、推广直播促销、粉丝转化、推动复购、赢回不活跃客户、邀请评价反馈
- **自动计划6种**：推广直播、开播提醒、降价提醒、购物车挽回、结账挽回、售后感谢
- **数据统计**：聊天GMV、聊天订单数、聊天转化客户数

### 3.6 素材图库模块

#### 3.6.1 图片管理统一设计

- 主图：商品级，最多9张
- SKU图片：SKU级别，支持拖拽排序
- 批量上传：支持Excel导入SKU图片映射
- 图片编辑器：组件化iframe嵌入，分三阶段实现

#### 3.6.2 图片编辑器集成方案

```
ImageEditorComponent
├── 基础版（内置）
│   ├── 上传/预览
│   ├── 裁剪/旋转
│   ├── 尺寸修改
│   └── 水印添加
└── 增强版（可选集成易可图）
    ├── iframe嵌入 yiketu.com/photo/editor
    ├── 批量编辑（最多10张）
    ├── AI设计/智能抠图
    └── 主图模板
```

#### 3.6.3 易可图图片编辑器功能清单

| 功能模块 | 具体功能 |
|----------|----------|
| **基础调整** | 调整、裁剪旋转、修改尺寸、图片校正 |
| **添加元素** | 文字、标记、形状线条、马赛克、标注笔、放大镜 |
| **主图模板** | 电商主图模板库 |
| **色彩处理** | 色彩调整 |
| **水印** | 水印添加 |
| **素材库** | 电商素材、边框、组件 |
| **AI功能** | AI设计、智能抠图、图片变清晰、商品堆品、logo检测 |
| **高级工具** | 消除笔、图片翻译、拼图、切图、无损放大、POD设计、单位转化、商品标尺、涂鸦 |

### 3.7 多店铺同步模块

#### 3.7.1 店铺层级结构

```
账户
├── 店铺组（按平台分组）
│   ├── Shopee店铺组
│   │   ├── 菲律宾站店铺
│   │   ├── 泰国站店铺
│   │   └── ...
│   ├── TikTok Shop店铺组
│   │   ├── 菲律宾站跨境店
│   │   ├── 新加坡站本地店
│   │   └── ...
│   ├── TEMU店铺组
│   │   ├── 美国站全托管
│   │   ├── 欧区半托管
│   │   └── ...
│   └── 妙手ERP授权店铺组
```

#### 3.7.2 跨店同步逻辑

- 同一商品可同步到多个授权店铺
- 不同站点差异化定价（汇率+本地化）
- 批量上架到多个店铺
- 库存同步：跨店铺库存统一管理

---

## 四、多平台、多店铺、多国市场差异化统一解决方案

### 4.1 平台差异化统一处理机制

```
┌─────────────────────────────────────────────────────────────┐
│                    统一商品对象（UPO）                       │
│  标准字段 + 扩展字段(JSONB) + 国别配置                      │
├─────────────────────────────────────────────────────────────┤
│  平台适配器层                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Shopee    │  │TikTok    │  │TEMU      │  │Miaoshou  │   │
│  │Adapter   │  │Adapter   │  │Adapter   │  │Adapter   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│        ↓              ↓              ↓              ↓       │
│  平台API/爬虫    平台API/爬虫    平台API/爬虫    ERP同步    │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 国别市场差异化处理

| 差异维度 | 处理方式 |
|----------|----------|
| **货币/汇率** | country_config表存储，显示层格式化，统一CNY存储 |
| **类目体系** | 各平台类目树独立维护，选择后动态加载字段 |
| **支付方式** | 各站点支付方式不同，适配器映射到统一状态机 |
| **物流渠道** | 各站点物流渠道不同，适配器注入配置 |
| **税费** | 各国税率不同，country_config存储 |
| **合规要求** | 各平台合规强度不同，适配器验证规则 |
| **店铺权限** | 跨境店/本地店/全托管/半托管权限差异 |

### 4.3 平台特有功能处理

#### Shopee特有
- SSP编号、Hot Listing标签、Smart Diagnosis
- New Item 90天流量扶持、Advance Fulfillment预发货库存
- 8种优惠券类型、联盟营销佣金

#### TikTok Shop特有
- SPS评分体系（影响CRM解锁/商品排名/活动报名）
- CRM配额、聊天营销计划
- 直播/短视频关联、跨境店铺标识

#### TEMU特有
- SPU/SKC/SKU三层结构
- 全托管供货价模式、建议零售价合规
- 备货仓组、JIT/VMI模式
- 强制合规、体检中心、质量管理中心

#### 妙手ERP特有
- 货源价格、主货号、产品ID
- 采集箱、批量发布、AI选品
- 易可图图片编辑器集成

### 4.4 平台后台导航URL参考（调研原始数据收口）

> **用途**：为爬虫采集器、页面跳转链接、自动化测试提供精确URL基准。所有URL来自Chrome DevTools MCP只读爬取调研。

#### 4.4.1 Shopee商家后台 (`seller.shopee.cn`)

| 一级菜单 | 子模块 | URL路径 | 说明 |
|----------|--------|---------|------|
| 商品 | 全球商品 | `/portal/product/mtsku/list` | 全球商品列表 |
| 商品 | 店铺商品 | `/portal/product/list` | 当前店铺商品 |
| 商品 | 添加商品 | `/portal/product/mtsku/category` | 分类选择入口 |
| 商品 | 实际创建页 | `/portal/mtsku/new` | 商品创建页 |
| 商品 | 商品卡片字段 | — | SSP编号、Hot Listing标签、Opportunity New Product、Model ID、Available Stock、In-transit Advance Stock、L30D Sales、L30D Impression、CTR、CVR、Rating、Review Count、Created At、Updated At |
| 营销中心 | 折扣活动 | `/portal/marketing/list/discount` | 套装优惠/我的折扣/分类折扣 |
| 营销中心 | 店内秒杀 | `/portal/marketing/shop-flash-sale/list` | Flash Sale选时段→添加商品 |
| 营销中心 | 优惠券 | `/portal/marketing/vouchers/list` | 8种优惠券类型 |
| 营销中心 | 跨境活动 | `/portal/marketing/cmt-cb/list` | 跨境活动报名 |
| 营销中心 | 联盟营销 | `/portal/web-seller-affiliate/dashboard` | 商品级佣金设置 |
| 订单 | 我的订单 | `/portal/sale/order` | 订单列表 |
| 订单 | 批量出货 | `/portal/sale/mass/ship` | 批量发货 |
| 订单 | 退货退款取消 | `/portal/sale/returnrefundcancel` | 退货/退款/取消管理 |
| 财务 | 我的收入 | `/portal/finance/income` | 需额外密码验证 |
| 财务 | Shopee官方钱包 | `/portal/finance/cncb-wallet` | 钱包余额 |
| 财务 | 收款账户 | `/portal/finance/wallet/cards` | 收款账户管理 |
| 物流设置 | 物流渠道 | `/portal/all-settings/shipping/shipping-channel` | Express International/Standard International/FBP |

**Shopee国别差异表**：
| 站点 | 货币 | 语言 | 差异维度 |
|------|------|------|----------|
| 菲律宾 PH | PHP ₱ | English/Filipino | COD/SPayLater支持 |
| 新加坡 SG | SGD S$ | English | 无COD |
| 马来西亚 MY | MYR RM | English/Malay | GrabPay支付 |
| 泰国 TH | THB ฿ | Thai | PromptPay支付 |
| 越南 VN | VND ₫ | Vietnamese | MoMo/ZaloPay |
| 印尼 ID | IDR Rp | Indonesian | GoPay/OVO |
| 台湾 TW | TWD NT$ | Chinese | 本地物流为主 |
| 英国 UK | GBP £ | English | VAT税务合规 |
| 美国 US | USD $ | English | FDA/CPSC合规 |

**Shopee类目树示例**：时尚配饰 → 包袋 → 手提包 → 通勤手提包 / 购物袋 / 水桶包

#### 4.4.2 TikTok Shop卖家后台 (`seller.tiktokshopglobalselling.com`)

| 一级菜单 | 子模块 | URL路径 | 说明 |
|----------|--------|---------|------|
| 订单 | 全部订单 | `/order?selected_sort=6&tab=all` | 订单列表默认页 |
| 订单 | 待付款 | `/orders?status=toPay&shop_region=PH` | 按状态+站点筛选 |
| 订单 | To Process | `/orders?status=toProcess&shop_region=PH` | 审单环节 |
| 订单 | To Ship | `/orders?status=toShip&shop_region=PH` | 待发货 |
| 订单 | Completed | `/orders?status=completed&shop_region=PH` | 已完成 |
| 营销 | CRM聊天 | `/crm?shop_region=PH` | 聊天营销（需SPS≥3.5+GMV>0） |
| 营销 | 联盟营销 | `/affiliate/landing` | 联盟推广 |
| 商品 | 商品列表 | `/goods/list` | 商品管理列表 |
| 商品 | 创建商品 | `/goods/create` | 商品创建页 |

**TikTok Shop多站点差异**：
| 区域 | 站点 | 域名特点 | 差异维度 |
|------|------|----------|----------|
| 东南亚 | PH/SG/MY/TH/VN/ID | seller.tiktokshopglobalselling.com 统一入口 | 各站点支付方式/物流时效不同 |
| 全球站 | UK/US | 同一域名 | VAT/销售税、FDA/CE合规要求更高 |
| 跨境店 vs 本地店 | 权限差异 | 跨境店需要跨境资质，本地店需要当地营业执照 |

**TikTok CRM聊天营销完整模板清单**：
- **一次性计划模板（7个）**：分享热销商品、新品公告、直播促销、粉丝转化、复购推动、不活跃客户赢回、评价邀请
- **自动计划模板（6个）**：直播推广、开播提醒、降价提醒、购物车挽回、结账挽回、售后感谢
- **配额管理**：本周总配额、剩余配额
- **数据统计**：聊天GMV、聊天订单数、聊天转化客户数

#### 4.4.3 TEMU卖家后台 (`agentseller.temu.com`)

| 一级菜单 | 子模块 | URL路径 | 说明 |
|----------|--------|---------|------|
| 商品 | 商品列表 | `/goods/list` | 商品管理主入口 |
| 商品 | 创建商品 | `/goods/create` | 两步式创建（分类→基本信息） |
| 销售管理 | 子模块 | — | 退货申请、退货包裹管理、收货/入库异常处理、保税仓退货管理、发货台、申请备货、商家自发货、平台发货、物流轨迹、运单管理、司机管理、地址管理、对账结算（共13项） |
| 商品管理 | 子模块 | — | 商品列表、创建商品、商品体检、商品优化事项、供货价管理、库存管理、商品条码管理、质量管理（体检中心/送检包裹/样品管理/拍摄退样/精修任务/说明书制作/零售价合规中心）、合规信息、敏感属性、SPU/SKC管理（共30+项） |
| 物流 | 发货台 | — | 跨镜买货系统 |
| 物流 | 司机/地址管理 | — | 仓库物流人员管理 |
| 物流 | 收货入库异常 | — | 异常处理流程 |

**TEMU站点选择器**：全球 / 美国 / 欧区

**TEMU库存分类**：
- 仓内可用库存、仓内预占用库存、仓内暂不可用库存、已发货库存、待审核备货库存
- 卖家仓：建议目标库存天数、建议目标库存、建议生产/采购量

#### 4.4.4 妙手ERP (`seller.kuajingmaihuo.com`)

| 功能模块 | 说明 |
|----------|------|
| 采集方式 | 链接采集、1688跨境热卖、导入采集、关键词采集、整店采集、插件采集、店铺互采（共7种） |
| 采集设置 | 平台隔离配置、SKU生成规则、标题优化模式、描述设置 |
| 产品编辑 | 双层弹窗架构（批量编辑弹窗 + iframe易可图编辑器） |
| 批量编辑 | 标签页切换：标题管理/关键词/属性/图片/描述 |
| 三态管理 | 未发布→定时发布→已发布 |

**妙手ERP已知坑点（工程防护）**：
- 页面重定向不稳定，需增加重试机制
- TEMU图片加载慢，需增加懒加载和占位图
- SKU超限自动删除，CBHunter应改为提示而非自动删除
- 品牌信息过滤不准确，需增加品牌白名单
- 多标题匹配冲突，需增加标题去重逻辑

---

## 五、选品引擎与主系统全链路融合方案

### 5.1 选品器完整体系

选品器作为系统**顶层流量挖掘模块**，包含：

#### 5.1.1 64条原生策略完整规格（8大类、64条）

##### 5.1.1.1 爆款驱动策略（BS-01~BS-08，共8条）

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| BS-01 | 平台榜单Top N | 筛选各平台公域榜单前N名商品 | TopN值(10/50/100) | 类目限定、站点限定 | TikTok/Shopee/Temu/Amazon/Lazada/AliExpress | A级 | TikTok/Shopee/Temu公域Bestseller页面 | 简单 | 日更 | 免费 | 短期可落地 | 平台官方Bestseller API |
| BS-02 | 飙升榜入选 | 近7天/30天销量增速前N的商品 | 时间窗口(7d/14d/30d)、增速阈值 | 最低增速%、最低销量绝对值 | TikTok/Shopee/Amazon | A级 | TikTok飙升榜页面+Shopee热销榜 | 简单 | 日更 | 免费 | 短期可落地 | 平台趋势数据API |
| BS-03 | 新品爆款 | 上架30天内销量突破阈值的商品 | 上架天数≤30、最低销量 | 新品定义天数、销量门槛 | TikTok/Shopee/Amazon | A级 | 公域商品详情页上架时间+销量字段 | 中等 | 日更 | 免费 | 短期可落地 | 平台新品标识API |
| BS-04 | 类目冠军 | 某类目下销量/销售额第一的商品 | 类目路径、时间窗口 | 类目粒度(L1/L2/L3) | TikTok/Shopee/Temu/Amazon | A级 | 各平台类目排行榜页面 | 简单 | 日更 | 免费 | 短期可落地 | 类目排行榜API |
| BS-05 | 多平台爆款交叉 | 同时在≥2个平台热销的同类商品 | 平台数量≥2、相似度阈值 | 标题/类目相似度算法 | TikTok/Shopee/Temu/Amazon | A级 | 跨平台公域爬虫比对 | 困难 | 周更 | 免费(需算力) | 中期可落地 | 第三方选品工具数据接口 |
| BS-06 | 季节性爆款预判 | 基于历史季节性规律预测下一周期爆款 | 季节周期、历史年份 | 往年销量增长阈值 | 全平台 | C级 | 用户导入历史销量CSV | 中等 | 月更 | 免费 | 短期可落地 | 平台季节性指数API |
| BS-07 | 直播爆款 | 直播期间销量激增的商品 | 直播时段、销量增幅 | 最低增幅%、直播场次 | TikTok | A级 | TikTok LIVE公域页面+商品链接 | 困难 | 实时 | 免费 | 中期可落地 | TikTok LIVE数据API |
| BS-08 | 短视频爆款 | 短视频带货销量突出的商品 | 视频播放量、转化率 | 最低播放量、最低转化率 | TikTok | A级 | TikTok短视频公域页+商品橱窗 | 困难 | 日更 | 免费 | 中期可落地 | TikTok视频带货API |

##### 5.1.1.2 蓝海挖掘策略（BL-01~BL-08，共8条）

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| BL-01 | 低竞争高需求 | 搜索量大但商品数少的类目/关键词 | 搜索量下限、商品数上限 | 供需比阈值 | TikTok/Shopee/Amazon | A级 | 公域搜索建议+搜索结果页商品计数 | 简单 | 日更 | 免费 | 短期可落地 | 平台搜索指数API |
| BL-02 | 空白类目发现 | 平台类目树中存在但未充分开发的节点 | 类目层级、商品密度 | 最低商品数、最低销量 | Shopee/Temu/Amazon | A级 | 各平台类目树页面+类目下商品列表 | 中等 | 周更 | 免费 | 短期可落地 | 平台类目开放API |
| BL-03 | 跨站蓝海迁移 | A平台热销但B平台尚未大量出现的商品 | 源平台、目标平台、时间差 | 上架时间差、商品数差 | TikTok→Shopee/Temu→Amazon等 | A级 | 跨平台公域商品库比对 | 困难 | 周更 | 免费(需算力) | 中期可落地 | 第三方趋势监测工具 |
| BL-04 | 长尾关键词选品 | 针对长尾搜索词找对应商品 | 关键词长度、搜索量 | 搜索量范围、竞争度 | TikTok/Shopee/Amazon | A级 | 搜索框联想词+搜索结果页 | 简单 | 日更 | 免费 | 短期可落地 | 平台关键词工具API |
| BL-05 | 小众人群定制 | 面向特定人群/场景的细分商品 | 人群标签、场景标签 | 人群规模、购买力 | 全平台 | D级 | 无数据源，预留配置 | 无法获取 | 静态人工 | 免费 | 长期规划 | 用户画像数据购买 |
| BL-06 | 地域差异化 | 某国别热销但其他国别未覆盖 | 源国别、目标国别 | 销量差距、国别数量 | Shopee多站点/TikTok多站点 | A级 | 多站点公域榜单交叉比对 | 中等 | 周更 | 免费 | 短期可落地 | 平台国别热度API |
| BL-07 | 价格带空白 | 某价格区间商品少但需求存在 | 价格区间、需求指标 | 最低需求数、最高供给数 | TikTok/Shopee/Amazon | A级 | 价格筛选功能+结果计数 | 简单 | 日更 | 免费 | 短期可落地 | 平台价格分布API |
| BL-08 | 评论空白机会 | 高需求但现有商品评论数低的品类 | 评论数上限、销量下限 | 供需比、评论密度 | Amazon/Shopee/TikTok | A级 | 公域商品详情页评论数+销量 | 简单 | 日更 | 免费 | 短期可落地 | 平台评论数据API |

##### 5.1.1.3 利润导向策略（PF-01~PF-08，共8条）

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| PF-01 | 毛利率筛选 | 售价-成本≥目标毛利率 | 成本价、目标毛利率% | 最低毛利率、售价区间 | 全平台 | C级 | 用户导入成本表(Excel/CSV) | 中等 | 静态人工 | 免费 | 短期可落地 | 供应链API对接 |
| PF-02 | 运费占比控制 | 运费占售价比例≤阈值 | 重量、体积、目的国 | 最高运费占比% | Shopee/TikTok/Temu | A级+B级 | 公域商品尺寸爬取+物流费率估算/卖家后台运费模板 | 中等 | 日更 | 免费 | 短期可落地 | 平台物流费率API |
| PF-03 | 平台佣金优化 | 选择佣金率低的类目/站点 | 类目佣金率、站点 | 最高佣金率% | Shopee/TikTok/Temu | B级 | 卖家后台佣金规则页/平台开放平台佣金API | 简单 | 月更 | 免费 | 短期可落地 | 平台佣金API |
| PF-04 | 汇率波动对冲 | 优先结算货币稳定的站点 | 币种、汇率波动率 | 最大波动率% | 全平台 | C级 | 用户手动配置汇率表 | 简单 | 周更 | 免费 | 短期可落地 | 实时汇率API |
| PF-05 | 退货率控制 | 筛选退货率低的类目 | 类目退货率、历史数据 | 最高退货率% | Amazon/Shopee | A级+C级 | 公域类目数据+用户导入退货率表 | 中等 | 月更 | 免费 | 中期可落地 | 平台退货率API |
| PF-06 | 体积重优化 | 轻小件优先，降低物流成本 | 长宽高、重量 | 最大体积重、最低售价 | 全平台 | A级 | 公域商品详情页尺寸/重量字段 | 简单 | 日更 | 免费 | 短期可落地 | 平台商品尺寸API |
| PF-07 | 关税规避选品 | 避开高关税品类/材质 | 材质、HS编码 | 最高关税率% | 全平台 | C级 | 用户导入关税税率表 | 中等 | 月更 | 免费 | 短期可落地 | HS编码API对接 |
| PF-08 | 批量采购折扣 | 1688/供应链批量价利润测算 | 阶梯价格、MOQ | 最低批量、最高单价 | 全平台 | C级 | 用户导入供应商阶梯报价表 | 中等 | 月更 | 免费 | 短期可落地 | 1688/API对接 |

##### 5.1.1.4 竞争分析策略（CP-01~CP-08，共8条）

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| CP-01 | 卖家集中度 | 头部卖家占比过高的类目回避 | 前10卖家销量占比 | 最高集中度% | TikTok/Shopee/Amazon | A级 | 公域商品列表页卖家信息爬取 | 中等 | 周更 | 免费 | 短期可落地 | 平台卖家数据API |
| CP-02 | 价格战规避 | 同商品最低价过低、利润空间不足 | 最低价、平均价、成本 | 最低利润率、价格离散度 | 全平台 | A级 | 公域搜索同款商品比价 | 中等 | 日更 | 免费 | 短期可落地 | 平台价格监控API |
| CP-03 | 品牌壁垒检测 | 识别品牌垄断类目 | 品牌数量、市场份额 | 单一品牌占比阈值 | Amazon/Shopee | A级 | 公域商品详情页品牌字段 | 简单 | 周更 | 免费 | 短期可落地 | 品牌数据库对接 |
| CP-04 | 新进入者友好度 | 近期新店上架速度快的类目 | 新店数量、上架频率 | 新店占比、平均评分 | TikTok/Shopee | A级 | 公域店铺页+新品上架时间 | 困难 | 周更 | 免费 | 中期可落地 | 平台卖家画像API |
| CP-05 | 差评机会分析 | 竞品差评中暴露的改进点 | 差评关键词、频次 | 差评率、改进点数量 | Amazon/Shopee/TikTok | A级 | 公域评论详情页+NLP分析 | 困难 | 周更 | 免费(需NLP算力) | 中期可落地 | 平台评论API+AI分析 |
| CP-06 | listing质量差距 | 现有商品主图/标题/描述质量低 | 图片数量、标题长度、描述完整度 | 最低质量标准 | 全平台 | A级 | 公域商品详情页结构化爬取 | 中等 | 周更 | 免费 | 短期可落地 | 平台商品详情API |
| CP-07 | 广告竞争度 | 竞价广告少的类目竞争较低 | 广告商品占比、CPC | 最高广告占比、最低CPC | Amazon/Shopee/TikTok | B级 | 卖家后台广告数据/平台广告API | 中等 | 日更 | 付费 | 中期可落地 | 平台广告API |
| CP-08 | 跟卖风险预警 | 识别易被跟卖的标准化商品 | 商品标准化程度、品牌 | 跟卖风险等级 | Amazon/Temu | A级 | 公域商品比对+品牌标识检测 | 中等 | 周更 | 免费 | 短期可落地 | 平台跟卖监控API |

##### 5.1.1.5 趋势洞察策略（TR-01~TR-08，共8条）

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| TR-01 | 社交媒体热点 | TikTok/Instagram热点话题关联商品 | 话题标签、热度 | 最低热度、时间窗口 | TikTok/Instagram | A级 | 公域话题页+热门视频商品链接 | 中等 | 日更 | 免费 | 短期可落地 | 社交媒体API |
| TR-02 | 搜索趋势上升 | 平台内搜索量持续上升的关键词 | 关键词、时间序列 | 增长率%、连续周数 | TikTok/Shopee/Amazon | A级 | 公域搜索建议+趋势页面 | 简单 | 日更 | 免费 | 短期可落地 | 平台搜索趋势API |
| TR-03 | 节日/事件营销 | 基于节假日、大型活动提前选品 | 节日日历、活动日历 | 提前天数、品类匹配 | 全平台 | D级 | 无数据源，用户配置节日表 | 无法获取 | 静态人工 | 免费 | 长期规划 | 平台活动日历API |
| TR-04 | KOL带货风向 | 头部KOL近期推荐的商品类型 | KOL列表、推荐品类 | KOL粉丝量、推荐频次 | TikTok | A级 | 公域KOL主页+带货商品橱窗 | 困难 | 日更 | 免费 | 中期可落地 | KOL数据API |
| TR-05 | 众筹/预售热度 | Kickstarter/Indiegogo等众筹平台热门品类 | 项目类别、筹款额 | 最低筹款额、时间窗口 | 全平台 | C级 | 用户导入众筹平台数据 | 中等 | 月更 | 免费 | 短期可落地 | 众筹平台API |
| TR-06 | 谷歌趋势验证 | Google Trends验证商品需求趋势 | 关键词、地区、时间 | 兴趣值、上升曲线 | 全平台 | A级 | 公域Google Trends网页 | 简单 | 日更 | 免费 | 短期可落地 | Google Trends API |
| TR-07 | 行业新闻追踪 | 电商行业新闻/政策变化带来的机会 | 关键词、新闻源 | 新闻数量、情感倾向 | 全平台 | D级 | 无数据源，预留配置 | 无法获取 | 事件触发 | 免费 | 长期规划 | RSS/API新闻聚合 |
| TR-08 | 竞品上新监控 | 监控竞品店铺新品上架动态 | 竞品店铺列表、监控频率 | 上架间隔、品类匹配 | TikTok/Shopee/Amazon | A级 | 公域店铺页面+新品上架时间 | 困难 | 日更 | 免费 | 中期可落地 | 平台店铺监控API |

##### 5.1.1.6 合规与风控策略（RC-01~RC-08，共8条）

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| RC-01 | 禁限售规避 | 避开各平台禁限售类目/商品 | 类目黑名单、关键词黑名单 | 匹配规则 | 全平台 | A级 | 公域平台规则页/卖家后台规则中心 | 简单 | 月更 | 免费 | 短期可落地 | 平台规则API |
| RC-02 | 知识产权风险 | 检测商标、专利、版权风险 | 品牌词、图案、专利号 | 风险匹配度 | Amazon/Shopee | C级 | 用户导入黑名单/知识产权局公开数据库 | 中等 | 月更 | 免费 | 短期可落地 | 知识产权局API |
| RC-03 | 认证要求检查 | 目标国别强制认证要求（CE/FCC/FDA等） | 目的国、商品品类 | 认证类型清单 | 全平台 | B级 | 卖家后台认证要求/平台规则页 | 简单 | 月更 | 免费 | 短期可落地 | 平台合规API |
| RC-04 | 税务合规 | VAT/GST/销售税影响定价 | 目的国、税率 | 最高税率、含税售价 | 全平台 | C级 | 用户导入税务表/第三方税务SaaS | 中等 | 月更 | 免费/付费 | 短期可落地 | 税务API对接 |
| RC-05 | 物流限制规避 | 避开液体、粉末、电池等敏感物流商品 | 商品属性、物流渠道 | 敏感属性清单 | 全平台 | A级 | 公域物流规则页/平台物流政策 | 简单 | 月更 | 免费 | 短期可落地 | 平台物流规则API |
| RC-06 | 平台政策变动监控 | 监控平台规则变化对现有商品的影响 | 规则类型、变动频率 | 影响等级 | 全平台 | B级 | 卖家后台公告/平台公告API | 中等 | 周更 | 免费 | 中期可落地 | 平台公告API |
| RC-07 | 退货政策匹配 | 不同国家别退货政策差异 | 目的国、退货期限 | 最长退货期、运费承担 | 全平台 | B级 | 卖家后台政策页/平台政策API | 简单 | 月更 | 免费 | 短期可落地 | 平台政策API |
| RC-08 | 环保合规 | EU/美国环保法规（包装法、EPR等） | 目的国、商品材质 | 法规清单 | EU站点 | C级 | 用户导入法规表/官方公报 | 困难 | 月更 | 免费 | 中期可落地 | 法规数据库API |

##### 5.1.1.7 复购类策略（RP-01~RP-08，共8条）—— v2新增

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| RP-01 | 复购率选品 | 筛选历史复购率高的商品/类目 | 复购率下限、时间窗口 | 最低复购率%、观察周期 | Shopee/TikTok | B级+C级 | 卖家后台订单复购数据/妙手ERP同步 | 中等 | 月更 | 免费(需授权) | 中期可落地 | 平台复购率API |
| RP-02 | 周期消耗品选品 | 识别周期性补货商品（美妆、食品、耗材） | 消耗周期天数、补货频次 | 最低消耗频次、最高复购间隔 | 全平台 | A级+B级 | 公域类目属性+评论中"回购"/"用完又买"关键词/NLP | 困难 | 周更 | 免费(需NLP) | 中期可落地 | 平台复购数据API |
| RP-03 | 老客回购潜力款 | 面向已有粉丝/老客的二次转化商品 | 粉丝基数、历史购买频次、客单价 | 最低粉丝数、回购概率阈值 | TikTok/Shopee | B级 | 店铺粉丝数据+订单复购分析 | 困难 | 月更 | 免费(需授权) | 长期规划 | 平台CRM+复购预测API |
| RP-04 | 低流失商品筛选 | 筛选退货率低、差评少、复购稳定的商品 | 退货率、差评率、复购率 | 最高退货率%、最低好评率% | Amazon/Shopee/TikTok | A级+B级 | 公域退货率/评论+卖家后台退货数据 | 中等 | 月更 | 免费 | 中期可落地 | 平台用户留存API |
| RP-05 | 稳定日销款 | 非爆款但长期稳定出单的商品（现金流型） | 日均销量、销售稳定性、时间窗口 | 最低日均销量、销量波动率 | TikTok/Shopee/Amazon | A级 | 公域近30天/90天销量趋势 | 简单 | 日更 | 免费 | 短期可落地 | 平台销售趋势API |
| RP-06 | 季节循环爆款 | 每年固定周期反复爆发的商品（圣诞装饰、Ramadan用品等） | 季节周期、历史年份、类目 | 往年爆发日期、销量峰值 | 全平台 | C级+A级 | 用户导入历史季节性数据+公域当年趋势验证 | 中等 | 年更(季节性) | 免费 | 短期可落地 | 平台季节性指数API |
| RP-07 | 订阅制/定期购商品 | 适合设置自动补货提醒的消耗品类目 | 品类标签、补货周期、客单价 | 最低客单价、最高补货周期天数 | 全平台 | D级+A级 | 预留配置+公域同类目商品评论分析 | 无法获取 | 静态人工 | 免费 | 长期规划 | 第三方订阅电商数据 |
| RP-08 | 高LTV商品识别 | 客户终身价值高的商品（高复购×高客单×长生命周期） | LTV公式参数、复购率、客单价、生命周期 | 最低LTV值、复购率权重 | 全平台 | B级+C级 | 卖家后台LTV数据/用户导入订单+成本表 | 困难 | 月更 | 免费(需授权) | 长期规划 | 平台用户价值分析API |

##### 5.1.1.8 生命周期类策略（LC-01~LC-08，共8条）—— v2新增

| 策略ID | 策略名称 | 策略描述 | 参数配置 | 阈值调节 | 适配平台 | 数据级别 | 精准渠道来源 | 获取难易度 | 更新频率 | 数据成本 | 落地可行性 | 未来升级方案 |
|--------|----------|----------|----------|----------|----------|----------|-------------|-----------|----------|----------|------------|-------------|
| LC-01 | 新品期机会 | 上架30天内快速起量的商品，抢占早期红利 | 上架天数≤30、日销量增速 | 最低日增速%、观察天数 | TikTok/Shopee | A级 | 公域商品详情页上架时间+近7天销量 | 中等 | 日更 | 免费 | 短期可落地 | 平台新品流量扶持API |
| LC-02 | 成长期加速 | 搜索量/销量持续上升但未饱和的类目 | 搜索增速、销量增速、竞争密度 | 最低增速%、最大竞争密度 | TikTok/Shopee/Amazon | A级 | 公域搜索趋势+商品列表竞争度 | 中等 | 周更 | 免费 | 短期可落地 | 平台趋势API+竞争度API |
| LC-03 | 成熟期利润优化 | 市场已成熟但仍有利润空间的细分差异化商品 | 价格带、差异化特征、利润率 | 最低毛利率%、差异化评分 | 全平台 | A级+B级 | 公域价格分布+卖家后台利润数据 | 中等 | 周更 | 免费 | 中期可落地 | 平台利润分析API |
| LC-04 | 衰退期预警 | 识别销量下滑、评论负向增加、竞品减少的品类 | 销量变化率、评论情感趋势、竞品数量变化 | 最高销量下滑率%、最低评论增长 | 全平台 | A级 | 公域销量趋势+评论情感分析 | 困难 | 周更 | 免费(需NLP) | 中期可落地 | 平台商品生命周期API |
| LC-05 | 品类生命周期研判 | 判断某类目整体处于导入/成长/成熟/衰退哪一阶段 | 类目销量曲线、新品上架数、竞争者进入退出率 | 阶段判定阈值、时间窗口 | 全平台 | A级+C级 | 公域类目趋势+用户导入行业报告 | 困难 | 月更 | 免费 | 长期规划 | 行业数据SaaS |
| LC-06 | 爆款生命周期管理 | 监控已选爆款的生命周期阶段，动态调整运营策略 | 当前阶段、各阶段阈值 | 各阶段切换阈值 | 全平台 | A级+B级 | 公域销量趋势+卖家后台销售数据 | 中等 | 周更 | 免费 | 中期可落地 | 平台商品状态API |
| LC-07 | 跨生命周期迁移 | 在某平台已进入成熟期的商品，迁移到另一平台仍处于新品/成长期 | 源平台阶段、目标平台阶段、时间差 | 阶段差阈值、平台适配性 | TikTok→Shopee/Temu→Amazon | A级 | 跨平台公域商品库+生命周期算法比对 | 困难 | 周更 | 免费(需算力) | 中期可落地 | 第三方趋势监测工具 |
| LC-08 | 反周期选品 | 在品类衰退期反向进入——通过差异化/低价/新渠道翻盘 | 衰退速度、差异化空间、成本优势 | 最大可接受衰退率、最低差异化分 | 全平台 | A级+C级 | 公域趋势+用户导入成本/渠道数据 | 困难 | 月更 | 免费 | 长期规划 | 平台品类健康度API |

##### 5.1.1.9 全量策略统计（v2更新）

| 大类 | 策略数量 | A级 | B级 | C级 | D级 |
|------|----------|-----|-----|-----|-----|
| 爆款驱动策略 | 8 | 7 | 0 | 1 | 0 |
| 蓝海挖掘策略 | 8 | 6 | 0 | 1 | 1 |
| 利润导向策略 | 8 | 2 | 1 | 4 | 1 |
| 竞争分析策略 | 8 | 4 | 2 | 1 | 1 |
| 趋势洞察策略 | 8 | 3 | 0 | 2 | 3 |
| 合规与风控策略 | 8 | 2 | 3 | 2 | 1 |
| 复购类策略 | 8 | 4 | 4 | 3 | 1 |
| 生命周期类策略 | 8 | 8 | 3 | 2 | 0 |
| **合计** | **64** | **36** | **13** | **16** | **7** |

**说明**：
- A级策略（36条）：可直接通过公域数据自动化执行
- B级策略（13条）：需店铺授权后可同步获取
- C级策略（16条）：需人工导入或表格补录
- D级策略（7条）：商业逻辑成立，预留功能点位待未来迭代
- v2新增16条策略（8条复购类 + 8条生命周期类），覆盖存量经营和商品生命周期维度

##### 5.1.1.10 策略参数化配置示例（BS-01 JSON）

```json
{
  "strategy_id": "BS-01",
  "strategy_name": "平台榜单Top N",
  "category": "爆款驱动",
  "data_feasibility": "A",
  "platforms": ["tiktok", "shopee", "temu", "amazon", "lazada", "aliexpress"],
  "parameters": {
    "top_n": {"type": "integer", "default": 50, "min": 10, "max": 500},
    "time_window": {"type": "enum", "values": ["7d", "14d", "30d"], "default": "7d"},
    "category_filter": {"type": "category_path", "required": false},
    "country_filter": {"type": "array", "values": ["PH", "SG", "MY", "TH", "VN", "ID", "US", "UK"], "required": false}
  },
  "thresholds": {
    "min_sales": {"type": "integer", "default": 0},
    "min_rating": {"type": "decimal", "default": 0, "max": 5},
    "max_price": {"type": "decimal", "default": null},
    "min_price": {"type": "decimal", "default": null}
  },
  "data_source": {
    "type": "crawler",
    "url_pattern": "/bestseller?category={category}&time={time_window}",
    "refresh_frequency": "daily",
    "status": "active"
  }
}
```

##### 5.1.1.11 策略组合运算示例

**示例1：蓝海爆款组合**

目标：找到TikTok菲律宾站近7天榜单Top50、且搜索量上升、竞争度低的商品

策略组合：`BS-01 (榜单Top50) ∩ TR-02 (搜索趋势上升) ∩ BL-01 (低竞争高需求)`

运算结果：
- 输入：BS-01返回50个商品，TR-02返回200个商品，BL-01返回300个商品
- 交集运算后：约15个商品
- 输出：标杆样例商品列表（仅作为选品参考方向）

**示例2：利润导向的爆款筛选**

目标：Shopee多站点热销商品中，毛利率≥30%、运费占比≤10%的品类

策略组合：`BS-01 (榜单Top100) ∩ PF-01 (毛利率≥30%) ∩ PF-02 (运费占比≤10%)`

运算结果：
- 输入：BS-01返回100个商品，PF-01需用户导入成本数据，PF-02需物流估算
- 加权评分：0.4×BS-01 + 0.3×PF-01 + 0.3×PF-02
- 输出：按综合得分排序的商品候选池

**示例3：多级嵌套复合策略**

目标：合规前提下，寻找跨平台蓝海爆款

策略组合：`[(BS-01 ∩ BL-03) ∩ (RC-01 ∪ RC-02)] ∩ PF-01`

嵌套结构：
```
根节点（交集）
├── 子节点1（交集）
│   ├── BS-01 (榜单Top50)
│   └── BL-03 (跨站蓝海迁移)
├── 子节点2（并集）
│   ├── RC-01 (禁限售规避)
│   └── RC-02 (知识产权风险)
└── PF-01 (毛利率≥30%)
```

##### 5.1.1.12 与股票选股器对标映射

| 股票选股器概念 | 跨境选品对应 | 说明 |
|---------------|-------------|------|
| 选股条件（PE<20、ROE>15%） | 原生策略（BS-01、PF-01） | 可参数化配置的基础筛选单元 |
| 条件组合（且/或/非） | 复合策略运算（交集/并集/差集） | 多策略自由组合 |
| 自定义公式（A*B+C） | 加权评分策略 | 多策略加权求和排序 |
| 策略保存/复用 | 复合策略持久化 | 保存为独立策略实体 |
| 回测验证 | 历史数据模拟运算 | 用历史榜单验证策略有效性 |
| 条件池/拖拽 | UI交互设计 | 见第7.7节选品器UI/UX规范 |
| 实时行情更新 | 数据源定时刷新 | 见5.1.3策略数据解耦四层架构 |

##### 5.1.1.13 策略-数据源映射矩阵

| 策略ID | 策略名称 | 数据源ID | 数据源类型 | 数据级别 | 状态 |
|--------|----------|----------|-----------|----------|------|
| BS-01 | 平台榜单Top N | DS-TIKTOK-BESTSELLER / DS-SHOPEE-BESTSELLER / DS-TEMU-BESTSELLER | crawler | A | active |
| BS-02 | 飙升榜入选 | DS-TIKTOK-RISING / DS-SHOPEE-HOT | crawler | A | active |
| BS-03 | 新品爆款 | DS-COMMON-NEW-ITEMS | crawler | A | active |
| BS-04 | 类目冠军 | DS-COMMON-CATEGORY-RANKING | crawler | A | active |
| BS-05 | 多平台爆款交叉 | DS-CROSS-PLATFORM-COMPARISON | crawler | A | active |
| BS-06 | 季节性爆款预判 | DS-USER-IMPORT-HISTORY | import | C | active |
| BS-07 | 直播爆款 | DS-TIKTOK-LIVE-GOODS | crawler | A | reserved |
| BS-08 | 短视频爆款 | DS-TIKTOK-VIDEO-GOODS | crawler | A | reserved |
| BL-01 | 低竞争高需求 | DS-TIKTOK-SEARCH-SUGGEST | crawler | A | active |
| BL-02 | 空白类目发现 | DS-COMMON-CATEGORY-TREE | crawler | A | active |
| BL-03 | 跨站蓝海迁移 | DS-CROSS-PLATFORM-COMPARISON | crawler | A | active |
| BL-04 | 长尾关键词选品 | DS-COMMON-SEARCH-SUGGEST | crawler | A | active |
| BL-05 | 小众人群定制 | null | none | D | reserved |
| BL-06 | 地域差异化 | DS-COMMON-COUNTRY-RANKING | crawler | A | active |
| BL-07 | 价格带空白 | DS-COMMON-PRICE-FILTER | crawler | A | active |
| BL-08 | 评论空白机会 | DS-COMMON-REVIEW-COUNT | crawler | A | active |
| PF-01 | 毛利率筛选 | DS-USER-IMPORT-COST | import | C | active |
| PF-02 | 运费占比控制 | DS-SHIPPING-TEMPLATE / DS-COMMON-DIMENSION | api/import | B+C | active |
| PF-03 | 平台佣金优化 | DS-PLATFORM-COMMISSION | api | B | active |
| PF-04 | 汇率波动对冲 | DS-USER-IMPORT-EXCHANGE | import | C | active |
| PF-05 | 退货率控制 | DS-COMMON-RETURN-RATE + DS-USER-IMPORT | crawler/import | A+C | active |
| PF-06 | 体积重优化 | DS-COMMON-DIMENSION | crawler | A | active |
| PF-07 | 关税规避选品 | DS-USER-IMPORT-TARIFF | import | C | active |
| PF-08 | 批量采购折扣 | DS-USER-IMPORT-SUPPLIER | import | C | active |
| CP-01 | 卖家集中度 | DS-COMMON-SELLER-LIST | crawler | A | active |
| CP-02 | 价格战规避 | DS-COMMON-PRICE-COMPARISON | crawler | A | active |
| CP-03 | 品牌壁垒检测 | DS-COMMON-BRAND-FIELD | crawler | A | active |
| CP-04 | 新进入者友好度 | DS-COMMON-STORE-PAGE | crawler | A | active |
| CP-05 | 差评机会分析 | DS-COMMON-REVIEW-NLP | crawler+NLP | A | active |
| CP-06 | listing质量差距 | DS-COMMON-LISTING-QUALITY | crawler | A | active |
| CP-07 | 广告竞争度 | DS-PLATFORM-ADS-API | api | B | active |
| CP-08 | 跟卖风险预警 | DS-COMMON-BRAND-DETECTION | crawler | A | active |
| TR-01 | 社交媒体热点 | DS-SOCIAL-MEDIA-HOT | crawler | A | active |
| TR-02 | 搜索趋势上升 | DS-COMMON-SEARCH-TREND | crawler | A | active |
| TR-03 | 节日/事件营销 | null | none | D | reserved |
| TR-04 | KOL带货风向 | DS-TIKTOK-KOL-GOODS | crawler | A | reserved |
| TR-05 | 众筹/预售热度 | DS-USER-IMPORT-CROWDFUNDING | import | C | active |
| TR-06 | 谷歌趋势验证 | DS-GOOGLE-TRENDS | crawler | A | active |
| TR-07 | 行业新闻追踪 | null | none | D | reserved |
| TR-08 | 竞品上新监控 | DS-COMMON-STORE-NEW-ITEMS | crawler | A | reserved |
| RC-01 | 禁限售规避 | DS-PLATFORM-RULES | api/crawler | B | active |
| RC-02 | 知识产权风险 | DS-USER-IMPORT-IP-BLACKLIST | import | C | active |
| RC-03 | 认证要求检查 | DS-PLATFORM-CERTIFICATION | api | B | active |
| RC-04 | 税务合规 | DS-USER-IMPORT-TAX / DS-THIRD-PARTY-TAX | import/api | C | active |
| RC-05 | 物流限制规避 | DS-PLATFORM-LOGISTICS-RULES | crawler | A | active |
| RC-06 | 平台政策变动监控 | DS-PLATFORM-ANNOUNCEMENT | api | B | active |
| RC-07 | 退货政策匹配 | DS-PLATFORM-RETURN-POLICY | api | B | active |
| RC-08 | 环保合规 | DS-USER-IMPORT-ENV-REGULATION | import | C | active |
| RP-01 | 复购率选品 | DS-SELLER-REPURCHASE-DATA | api/import | B+C | active |
| RP-02 | 周期消耗品选品 | DS-COMMON-COMMENT-NLP | crawler+NLP | A+B | active |
| RP-03 | 老客回购潜力款 | DS-SELLER-CRM-DATA | api | B | reserved |
| RP-04 | 低流失商品筛选 | DS-COMMON-RETURN-RATE + DS-SELLER-RETURN | crawler/api | A+B | active |
| RP-05 | 稳定日销款 | DS-COMMON-DAILY-SALES-TREND | crawler | A | active |
| RP-06 | 季节循环爆款 | DS-USER-IMPORT-HISTORY + DS-COMMON-SEASONAL | import/crawler | C+A | active |
| RP-07 | 订阅制/定期购商品 | null | none | D | reserved |
| RP-08 | 高LTV商品识别 | DS-SELLER-LTV-DATA | api/import | B+C | reserved |
| LC-01 | 新品期机会 | DS-COMMON-NEW-ITEM-TREND | crawler | A | active |
| LC-02 | 成长期加速 | DS-COMMON-GROWTH-TREND | crawler | A | active |
| LC-03 | 成熟期利润优化 | DS-COMMON-PRICE-DIST + DS-SELLER-PROFIT | crawler/api | A+B | active |
| LC-04 | 衰退期预警 | DS-COMMON-DECLINE-TREND | crawler+NLP | A | reserved |
| LC-05 | 品类生命周期研判 | DS-COMMON-CATEGORY-LIFECYCLE + DS-USER-IMPORT | crawler/import | A+C | reserved |
| LC-06 | 爆款生命周期管理 | DS-COMMON-PRODUCT-LIFECYCLE + DS-SELLER-SALES | crawler/api | A+B | active |
| LC-07 | 跨生命周期迁移 | DS-CROSS-PLATFORM-LIFECYCLE | crawler | A | reserved |
| LC-08 | 反周期选品 | DS-COMMON-DECLINE + DS-USER-IMPORT-COST | crawler/import | A+C | reserved |

##### 5.1.1.14 数据源采集方式矩阵

| 数据级别 | 采集方式 | 实现技术 | 适用场景 | 限制 |
|----------|----------|----------|----------|------|
| A级 | 公域爬虫 | Chrome DevTools MCP / Playwright只读 | 榜单、搜索量、评论数 | 受反爬限制，需控制频率 |
| B级 | 官方API | 平台开放平台API / 妙手ERP授权 | 销量、订单、广告数据 | 需店铺授权，有调用限额 |
| C级 | 人工导入 | Excel/CSV上传 + 表单填写 | 成本价、关税、行业数据 | 依赖用户主动性 |
| D级 | 预留 | 暂无 | 纯策略配置项 | 等待数据源开发 |

##### 5.1.1.15 数据源热替换机制

当某个数据源失效或升级时：
```
旧数据源 DS-A（爬虫，A级）
  → 映射到策略 BS-01
  → 数据源失效

新数据源 DS-B（API，B级）
  → 注册新数据源
  → 更新映射：BS-01 → DS-B（优先级更高）
  → 旧映射标记为 deprecated

策略 BS-01 本身无需任何修改
```

##### 5.1.1.16 D级策略生命周期

```
创建D级策略（无数据源）
  → 正常入库、显示、配置、组合
  → 运算时标记"数据缺失"
  ↓
用户手动导入数据（升级为C级）
  → 更新数据源映射
  → 策略自动生效
  ↓
开发爬虫/API（升级为A/B级）
  → 注册新数据源
  → 更新映射优先级
  → 策略自动升级为自动化执行
```

##### 5.1.1.17 策略版本管理工作流

复合策略支持版本迭代：
```
CS-001 v1.0（初始版本）
  → 用户调整参数后保存 v1.1
  → 添加新的子策略节点保存 v2.0
  → 每次变更生成新版本
  → 旧版本可回溯、对比、恢复
```

核心特性：
- **无限嵌套**：复合策略可作为子节点继续组合
- **权重可调**：每个节点支持独立权重（0-1）
- **运算切换**：节点间可切换交集/并集/差集
- **永久保存**：所有策略组合可保存为独立策略实体
- **复用迭代**：已保存策略可再次作为组件使用
- **另存为新策略**：支持一级复合策略、多级嵌套策略、导出模板三种方式

##### 5.1.1.18 策略与数据解耦核心设计实体

**原生策略（BaseStrategy）**：
```
BaseStrategy
├── strategy_id: 唯一标识（如 BS-01）
├── strategy_name: 策略名称
├── category: 所属大类（爆款/蓝海/利润/竞争/趋势/合规/复购/生命周期）
├── data_feasibility: 数据可行性等级（A/B/C/D）
├── platforms: 适配平台列表
├── parameters: 可参数化配置项（JSON Schema）
├── thresholds: 阈值调节项（JSON Schema）
├── data_source_ref: 关联的数据源引用（可为空，D级策略为空）
├── status: 启用/停用
└── created_at / updated_at
```

**复合策略（CompositeStrategy）**：
```
CompositeStrategy
├── composite_id: 唯一标识
├── name: 策略名称
├── operator: 运算类型（intersection/union/difference/weighted）
├── children: 子节点列表（可递归嵌套）
│   ├── type: base 或 composite
│   ├── ref_id: 引用原生策略或复合策略ID
│   └── weight: 权重（0-1，加权模式用）
├── parent_id: 父复合策略ID（多级嵌套用）
├── saved_as_new: 是否另存为新策略
└── version: 策略版本号（支持迭代）
```

**数据源注册表（DataSourceRegistry）**：
```
DataSourceRegistry
├── 数据源ID
├── 数据源名称
├── 数据源类型（crawler/api/import/manual）
├── 适配平台列表
├── 采集URL/接口配置
├── 字段映射规则（原始字段 → 标准字段）
├── 刷新频率
├── 健康状态
└── 元数据（认证信息、限流规则等）
```

**策略-数据源映射表（StrategyDataSourceMapping）**：
```
StrategyDataSourceMapping
├── 策略ID
├── 数据源ID（可为空，D级策略）
├── 映射字段（策略参数 → 数据源字段）
├── 优先级（同一策略可映射多个数据源时的优先级）
└── 状态（active/paused/deprecated）
```

关键特性：
- 同一策略可映射多个数据源（如BS-01映射TikTok/Shopee/Temu各自榜单）
- 数据源下线时，策略不受影响，仅标记"数据不可用"
- 新增数据源时，只需注册新数据源并建立映射，**无需修改策略定义**

#### 5.1.2 数据可行性分级体系

| 级别 | 定义 | 落地方式 | 升级路径 |
|------|------|----------|----------|
| A级 | 公开展示数据 | Chrome DevTools MCP只读爬取/爬虫 | 自动化定时采集、API对接 |
| B级 | 店铺授权后数据 | 妙手ERP授权同步/官方API | 直连平台开放平台API |
| C级 | 人工/表格补录 | Excel/CSV导入、表单填写 | 第三方SaaS数据购买、OCR识别 |
| D级 | 纯策略预留 | 仅作为配置项存在 | 待数据源开发后激活 |

**v2五维数据资产标注**：每条策略标注精准渠道来源、获取难易度、更新频率、数据成本、落地可行性。

#### 5.1.3 策略数据解耦四层架构

```
策略配置层（Strategy Layer）
  - 原生策略库 | 复合策略库 | 权重配置 | 阈值设置
  - 完全独立，不依赖数据源是否存在

运算引擎层（Engine Layer）
  - 交集/并集/差集/加权运算 | 结果排序 | 去重
  - 仅读取策略配置，不直接访问数据

数据源映射层（Data Source Layer）
  - 策略ID → 数据源ID | 字段映射 | 采集方式 | 频率
  - 数据源可独立开发、替换、升级

数据采集层（Collection Layer）
  - A级：爬虫 | B级：API | C级：导入 | D级：无
```

### 5.2 智能量化选品引擎（v2）

#### 5.2.1 动态权重系统

六维权重维度：销量(w_sales)、利润(w_profit)、竞争度(w_competition)、趋势(w_trend)、复购(w_repurchase)、合规(w_compliance)。

**权重调节交互**：用户拖拽滑块调整权重 → 实时重新计算综合得分 → 商品排名即时刷新。

```
销量权重: ████████░░ 0.30
利润权重: ██████████ 0.35
竞争度权重: ████░░░░░░ 0.15
趋势权重: ██████░░░░ 0.10
复购权重: ███░░░░░░░ 0.07
合规权重: ██░░░░░░░░ 0.03
─────────────────────────
综合得分 = Σ(w_i × score_i)
```

**预设模板**：
- 爆款优先：销量0.40、利润0.10、竞争度0.15、趋势0.20、复购0.10、合规0.05
- 利润优先：销量0.15、利润0.40、竞争度0.10、趋势0.10、复购0.15、合规0.10
- 蓝海优先：销量0.15、利润0.15、竞争度0.40、趋势0.15、复购0.10、合规0.05
- 稳健经营：销量0.20、利润0.20、竞争度0.15、趋势0.10、复购0.25、合规0.10
- 合规优先：销量0.15、利润0.15、竞争度0.10、趋势0.10、复购0.10、合规0.40
- 自定义：用户自由调配

#### 5.2.2 智能负向筛选（NF-01~NF-08）

| 负向规则ID | 规则名称 | 说明 | 数据来源 |
|-----------|----------|------|----------|
| NF-01 | 排除高退货率 | 自动排除退货率超过阈值的类目/商品 | 卖家后台退货率+公域评论 |
| NF-02 | 排除低利润 | 排除扣除所有成本后利润率低于阈值的商品 | 成本表+售价+运费+佣金 |
| NF-03 | 排除高竞争 | 排除头部卖家集中度超过阈值的类目 | 公域商品列表+卖家分析 |
| NF-04 | 排除违规风险 | 排除触碰禁限售/知识产权红线的商品 | 平台规则+品牌数据库 |
| NF-05 | 排除价格战 | 排除最低价已无利润空间的标准化商品 | 公域比价 |
| NF-06 | 排除衰退品 | 排除处于生命周期衰退期的商品 | 销量趋势+NLP评论分析 |
| NF-07 | 排除低评分 | 排除评分低于阈值的商品 | 公域评论星级 |
| NF-08 | 排除同质化 | 排除搜索结果高度雷同的商品 | 标题相似度+图片相似度 |

**正负向组合运算**：最终商品池 = (正向策略结果 ∩ 负向排除结果) ∪ 白名单商品

示例：
```
正向：BS-01(榜单Top50) ∩ BL-01(低竞争) ∩ PF-01(毛利率≥30%)
负向：NF-01(退货率<5%) + NF-05(非价格战) + NF-04(无违规风险)
白名单：手动添加的必选商品
结果：同时满足正向条件、不被任何负向规则排除、且在白名单中
```

#### 5.2.3 SelectionEngine TypeScript接口

```typescript
/**
 * 选品引擎核心接口 — 策略与数据彻底解耦
 */
interface SelectionEngine {
  /**
   * 执行复合策略运算
   * @param compositeStrategy 复合策略树
   * @param userConfig 用户参数配置覆盖
   * @returns 运算结果
   */
  execute(compositeStrategy: CompositeStrategy, userConfig?: Record<string, any>): Promise<SelectionResult>;

  /**
   * 验证策略树合法性
   */
  validate(strategyTree: CompositeStrategy): ValidationResult;

  /**
   * 模拟运算（不实际采集数据，用于UI预览）
   */
  simulate(strategyTree: CompositeStrategy): SimulationResult;

  /**
   * 历史回测（用历史数据验证策略有效性）
   */
  backtest(strategyTree: CompositeStrategy, period: DateRange): BacktestResult;
}

interface SelectionResult {
  products: CandidateProduct[];        // 候选商品列表
  totalMatched: number;                // 匹配总数
  dataMissing: DataMissingReport[];    // 数据缺失报告
  executionTime: number;               // 执行耗时(ms)
  strategyTrace: OperationTrace[];     // 每层运算追踪
}

interface DataMissingReport {
  strategyId: string;
  strategyName: string;
  dataFeasibility: 'A' | 'B' | 'C' | 'D';
  message: string;                     // "该策略当前无数据源，已跳过"
}

interface OperationTrace {
  nodeId: string;
  operator: 'intersection' | 'union' | 'difference' | 'weighted';
  inputCounts: number[];
  outputCount: number;
  durationMs: number;
  dataMissing: DataMissingReport[];
}

interface ValidationResult {
  valid: boolean;
  errors: string[];                    // 校验错误信息
  warnings: string[];                  // 警告信息（如D级策略无数据源）
}

interface SimulationResult {
  estimatedMatchCount: number;         // 预估命中数
  confidence: 'low' | 'medium' | 'high';
  assumptions: string[];               // 估算假设说明
}

interface BacktestResult {
  period: DateRange;
  hitRate: number;                     // 命中率
  avgFirstMonthSales: number;          // 平均首月销量
  avgGrossMargin: number;              // 平均毛利率
  bestCase: { candidates: number; sold: number };
  worstCase: { candidates: number; sold: number };
  trend: 'up' | 'down' | 'stable';
}
```

#### 5.2.4 运算流程

```
输入：复合策略树 + 各叶子节点参数配置
  ↓
步骤1：遍历策略树，收集所有叶子节点（原生策略）
  ↓
步骤2：按叶子节点data_source_ref查询可用数据源
  ↓
步骤3：对每个叶子节点执行数据采集（A/B/C级）或标记缺失（D级）
  ↓
步骤4：从底层向上逐层执行运算
  ├─ 叶子节点：返回商品集合（或空集合+缺失标记）
  ├─ 交集节点：取各子节点结果的交集
  ├─ 并集节点：取各子节点结果的并集
  ├─ 差集节点：从父节点中排除子节点
  └─ 加权节点：对商品按各策略得分加权求和
  ↓
步骤5：汇总运算结果，标记数据缺失情况
  ↓
输出：候选商品池 + 数据完整性报告
```

#### 5.2.5 相似策略推荐引擎

当用户构建或查看一个策略时，系统自动推荐相似或互补的策略：

```
当前策略：BS-01(榜单Top50) + BL-01(低竞争)

系统推荐：
├── 相似策略：
│   ├── "TikTok菲律宾包袋爆款" (历史命中率高)
│   └── "Shopee马来站3C配件蓝海" (结构类似)
├── 互补策略：
│   ├── PF-01(毛利率筛选) — 补充利润维度
│   ├── CP-02(价格战规避) — 补充竞争维度
│   └── RP-05(稳定日销款) — 补充复购维度
└── 风险预警：
    ├── RC-01(禁限售规避) — 该类目存在合规风险
    └── LC-04(衰退期预警) — 部分商品已进入衰退期
```

**实现技术**：pgvector/Milvus向量检索 + LLM语义分析，基于策略类别、参数、历史命中率计算相似度。

#### 5.2.6 策略效果回溯与胜率分析

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| 命中率 | 候选商品中实际出单的比例 | 有销量商品数 / 候选商品总数 |
| 平均首月销量 | 候选商品上线首月平均销量 | Σ首月销量 / 候选商品数 |
| 平均毛利率 | 候选商品实际毛利率 | Σ(售价-成本)/售价 |
| 策略ROI | 使用该策略的时间投入产出比 | 商品GMV / 运营时间 |
| 复购率 | 候选商品的30天/60天/90天复购率 | 复购订单数 / 总订单数 |
| 生命周期评分 | 商品存活到当前阶段的比例 | 存活商品数 / 初始候选数 |

**胜率分析视图**：
```
策略 CS-001 历史表现（近90天）
├── 执行次数: 12次
├── 平均命中商品数: 23个
├── 平均首月出单率: 67%
├── 平均毛利率: 34.2%
├── 最佳一次: 45个候选，32个出单
├── 最差一次: 8个候选，2个出单
├── 胜率趋势图: [📈 近30天上升]
└── 归因分析:
    ├── 有利因素: 权重配置合理、数据源稳定
    ├── 不利因素: TR-07数据缺失导致偏差、PF-01成本数据过期
    └── 优化建议: 提高PF-01权重至0.35，补充RP-05策略
```

#### 5.2.7 AI辅助复合策略生成

```
输入：用户描述选品目标
  "我想在TikTok菲律宾站找包袋类目的蓝海爆款，要求毛利率30%以上"

AI生成策略树：
{
  "name": "TikTok菲律宾包袋蓝海利润款",
  "operator": "intersection",
  "children": [
    {"ref_id": "BS-01", "config": {"top_n": 50, "country": "PH"}},
    {"ref_id": "BL-01", "config": {"min_search_volume": 500, "max_product_count": 200}},
    {"ref_id": "PF-01", "config": {"target_margin": 0.30}},
    {"ref_id": "RP-05", "config": {"min_daily_sales": 5}},
    {"negative_filters": ["NF-01", "NF-04"]}
  ],
  "weights": {
    "w_sales": 0.25,
    "w_profit": 0.30,
    "w_competition": 0.20,
    "w_trend": 0.10,
    "w_repurchase": 0.10,
    "w_compliance": 0.05
  }
}

输出：
✅ 策略已生成，可直接运行
💡 建议叠加LC-02(成长期加速)观察趋势
⚠️ 注意：PF-01需要导入成本数据才能生效
```

#### 5.2.8 v2高级动态策略引擎总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CBHunter 选品选股器 v2                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   策略配置层      │  │   智能运算引擎    │  │   结果展示层      │  │
│  │  Strategy Config  │→│   Smart Engine   │→│  Result Display  │  │
│  │                  │  │                  │  │                  │  │
│  │ • 原生策略库(64)  │  │ • 交集/并集/差集 │  │ • 标杆样例商品    │  │
│  │ • 复合策略库      │  │ • 加权评分排序    │  │ • 类目分布       │  │
│  │ • 参数阈值配置    │  │ • 去重/合并       │  │ • 趋势图表       │  │
│  │ • 策略嵌套树      │  │ • 动态权重调配    │  │ • 联动操作入口    │  │
│  │ • 负向筛选规则    │  │ • 负向过滤        │  │ • 实时预览       │  │
│  │ • 策略胜率数据    │  │ • 策略衍生推荐    │  │ • 波动分析       │  │
│  │ • AI辅助生成     │  │ • 回测验证        │  │ • 策略回溯       │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │
│           │                     │                     │             │
│           └─────────────┬───────┴─────────────────────┘             │
│                         ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              v2 新增：策略智能服务层                           │    │
│  │         Strategy Intelligence Service Layer                   │    │
│  │                                                             │    │
│  │  • 权重优化建议引擎                                           │    │
│  │  • 相似策略推荐引擎（pgvector/Milvus向量检索）                 │    │
│  │  • 策略一键衍生引擎                                           │    │
│  │  • 负向规则自动推导                                           │    │
│  │  • 策略胜率统计与归因                                         │    │
│  │  • AI复合策略生成器（LLM API）                                │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                         ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    数据源映射层                               │    │
│  │              Data Source Mapping Layer                       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                         ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    数据采集层                                 │    │
│  │                Collection Layer                              │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 5.2.9 v2技术栈更新

| 层级 | 技术选型 | 理由 |
|------|----------|------|
| 前端框架 | React + TypeScript | 与CBHunter现有架构一致 |
| 状态管理 | Zustand / Redux Toolkit | 策略配置状态持久化 |
| 运算引擎 | 纯TypeScript实现 | 前后端共用，便于测试 |
| 数据源调度 | Node.js Worker线程 | 异步采集，不阻塞UI |
| 数据库 | PostgreSQL JSONB | 存储策略树、配置、映射 |
| 缓存 | Redis | 缓存采集结果，减少重复请求 |
| AI服务 | LLM API | 策略生成、相似推荐、归因分析 |
| 向量检索 | pgvector / Milvus | 策略相似度检索 |

#### 5.2.10 与现有CBHunter系统融合点

**打通素材图库**：选品结果中的标杆商品图片/视频可一键收藏到CBHunter素材图库，作为后续商品发布时的参考素材，支持批量下载、分类管理。

**打通商品发布模块**：选品结果可直接转化为待发布商品草稿，复用01_多平台电商后台调研汇总中的字段映射，通过02_功能开发方案总文档中的弹窗式编辑流程上架。

**打通SKU定价模块**：利润导向策略（PF系列）的计算结果可自动填充SKU定价表，结合国别汇率配置生成多币种售价，支持一键应用到批量商品。

**打通多店铺同步**：选品结果可按店铺维度分发，同一商品不同站点差异化定价，跨店铺库存同步，批量上架到多个授权店铺。

**v2新增：策略市场与共享**：用户可将自研策略发布到公共策略市场，支持按类目、平台、胜率排序浏览他人策略，一键订阅他人策略并加入自己的策略库，策略贡献者可获得积分/收益分成。

#### 5.2.11 开发优先级（v2 P0~P12）

| 阶段 | 内容 | 周期 |
|------|------|------|
| P0 | 原生策略库CRUD + D级策略配置 + 64条策略入库 | 2周 |
| P1 | 基础运算引擎（交集/并集/差集/加权） | 2周 |
| P2 | A级数据源接入（TikTok/Shopee/Temu公域） | 3周 |
| P3 | 复合策略嵌套 + 保存/复用 + 版本管理 | 2周 |
| P4 | B级API数据源接入 | 3周 |
| P5 | C级Excel导入 + D级预留激活 + 复购/生命周期策略 | 2周 |
| P6 | UI/UX交互完善（股票选股器范式） | 3周 |
| P7 | 动态权重系统 + 预设模板 | 2周 |
| P8 | 负向筛选规则 + 正负向组合运算 | 2周 |
| P9 | 策略胜率统计 + 回测数据追踪 | 3周 |
| P10 | 策略一键衍生 + 相似策略推荐 | 2周 |
| P11 | AI辅助复合策略生成 | 3周 |
| P12 | 策略市场与共享 | 2周 |

#### 5.2.12 基础运算类型

| 运算类型 | 符号 | 说明 | 示例 |
|----------|------|------|------|
| 交集 | ∩ | 同时满足多个策略条件 | BS-01 ∩ BL-01 = 榜单Top50且低竞争的类目 |
| 并集 | ∪ | 满足任一策略条件即可 | BS-01 ∪ TR-02 = 爆款或趋势上升商品 |
| 差集 | \ | 排除满足特定条件的商品 | BS-01 \ CP-01 = 爆款但非高集中度类目 |
| 加权评分 | Σ(w×s) | 多策略加权求和排序 | 0.3×BS-01 + 0.2×BL-01 + 0.5×PF-01 |

#### 5.2.13 策略一键衍生

7种衍生方向：参数微调、平台迁移、类目限定、国别限定、周期缩放、组合叠加、负向增强。

衍生流程：
```
用户选择策略BS-01
  → 点击「衍生策略」
  → 系统展示7种衍生方向
  → 用户勾选需要的衍生方式
  → 自动生成新策略CS-DERIVE-001
  → 支持继续对该衍生策略做二次衍生
```

衍生方式明细：

| 衍生方式 | 说明 | 示例 |
|----------|------|------|
| 参数微调 | 在原策略基础上调整阈值 | BS-01(Top50) → BS-01'(Top30) |
| 平台迁移 | 将策略应用到其他平台 | TikTok榜单 → Shopee榜单 |
| 类目限定 | 增加类目过滤条件 | 全类目爆款 → 包袋类目爆款 |
| 国别限定 | 增加国别过滤条件 | 全站点 → 仅菲律宾站 |
| 周期缩放 | 改变时间窗口 | 7天飙升 → 30天飙升 |
| 组合叠加 | 自动推荐可叠加的策略 | BS-01 → 推荐叠加BL-01+PF-01 |
| 负向增强 | 为现有策略自动添加排除规则 | 爆款筛选 → 排除高退货率 |

### 5.3 选品→上架→出单→回款全链路闭环

```
选品器（流量挖掘）
  ↓ 标杆样例商品
素材图库（图片/视频收藏）
  ↓ 一键转化为草稿
商品编辑（统一底座+平台适配器）
  ↓ 动态表单+批量编辑
定价模板（利润策略计算结果填充）
  ↓ 多店铺差异化定价
批量上架（采集箱→待发布→已发布）
  ↓ 多店铺同步管控
订单管理（统一状态机）
  ↓ 物流同步
资金结算（多币种统一CNY存储）
  ↓ 回款
选品胜率回溯（验证选品策略有效性）
```

---

## 六、新旧功能冲突解决与收口规范

### 6.1 保留无需改动模块

| 模块 | 说明 |
|------|------|
| 统一底座框架 | 已设计的商品/订单/资金/营销/物流/店铺/权限/通知/数据看板架构 |
| 字段标准字典 | 110+字段的标准/非标准分类和跨平台映射规则 |
| 动态表单引擎 | Schema驱动的动态表单设计 |
| 国别配置表 | country_config表设计 |
| 平台适配器接口 | PlatformAdapter接口定义 |

### 6.2 需要局部重构优化模块

| 模块 | 重构内容 |
|------|----------|
| 商品编辑模式 | 从各平台独立SPA统一为弹窗式编辑 |
| SKU管理 | 从两层规格统一为父级+变体组+SKU三层结构 |
| 定价引擎 | 从多币种分散存储统一为CNY存储+国别格式化 |
| 订单状态机 | 从各平台独立状态统一为映射表 |
| 图片管理 | 引入SKU图片管理和批量编辑功能 |
| 批量操作 | 引入采集箱/待发布池概念 |

### 6.3 需要补齐的模块

| 模块 | 补齐内容 |
|------|----------|
| 选品器 | 完整新增64条策略+引擎+UI+数据库 |
| 素材图库 | 打通选品标杆商品收藏 |
| 商品草稿 | 选品结果转化为待发布草稿 |
| 定价模板 | 利润策略计算结果自动填充 |
| 多店铺批量上架 | 按店铺维度分发差异化定价 |
| 策略市场 | 用户自研策略发布/订阅/积分收益分成 |
| 数据分析看板 | 全平台商业数据统一看板 |
| 通知中心 | 全站消息/规则公告/合规警告/系统通知 |
| 退货退款管理 | 订单模块子页面 |
| 物流管理独立页 | 运费模板/物流渠道/发货台 |
| 营销活动列表页 | 折扣/秒杀/优惠券列表管理 |
| 店铺授权/管理页 | 多店铺层级管理的完整页面 |
| 用户/子账号管理页 | 权限隔离的完整页面设计 |

### 6.4 未来预留功能

| 预留项 | 说明 |
|--------|------|
| D级策略数据源 | TR-07行业新闻、BL-05小众人群、TR-03节日营销等7条 |
| 平台官方API | 多数B级/A级策略的未来升级路径 |
| NLP算力 | CP-05差评分析、RP-02周期消耗品、LC-04衰退预警 |
| 跨平台比对算力 | BS-05多平台爆款交叉、BL-03跨站蓝海迁移 |
| 实时汇率API | PF-04汇率波动对冲 |
| HS编码/关税API | RC-04税务合规、PF-07关税规避 |

---

## 七、统一UI/UX全局交互标准

### 7.1 全局设计规范

#### 7.1.1 设计原则

| 原则 | 说明 |
|------|------|
| 只读优先 | 所有涉及资金、发布、修改的操作必须有二次确认，默认不自动执行写操作 |
| 信息密度 | 列表页以表格为主，兼顾卡片浏览；关键指标一眼可见 |
| 平台感知 | 不同平台的差异化功能通过标签、颜色、图标清晰区分 |
| 国别隔离 | 货币、类目、支付方式等按站点独立展示，不混用 |
| 批量高效 | 批量操作前置到采集/编辑阶段，减少单条修改成本 |

#### 7.1.2 色彩体系

| 用途 | 色值 | 应用场景 |
|------|------|----------|
| 主色 | #1890FF (Shopee蓝) | 按钮、链接、选中态 |
| 成功 | #52C41A | 已完成、已发布、正常状态 |
| 警告 | #FAAD14 | 待处理、审核中、流量下降 |
| 危险 | #F5222D | 违规、删除、超时 |
| 信息 | #1890FF | 提示、说明、链接 |
| 中性-标题 | #262626 | 标题文字 |
| 中性-正文 | #595959 | 正文文字 |
| 中性-辅助 | #8C8C8C | 辅助说明、占位符 |
| 背景 | #F5F5F5 | 页面背景 |
| 白 | #FFFFFF | 卡片/容器背景 |

**平台标识色**：

| 平台 | 标识色 | 应用 |
|------|--------|------|
| Shopee | #EE4D2D (Shopee橙) | 商品标签、状态徽章、导航高亮 |
| TikTok Shop | #000000 (黑) | 商品标签、状态徽章、导航高亮 |
| TEMU | #FB5C2F (Temu橙红) | 商品标签、状态徽章、导航高亮 |
| 妙手ERP | #1677FF (妙手蓝) | 商品标签、状态徽章、导航高亮 |

#### 7.1.3 字体与间距

| 元素 | 字号 | 字重 | 行高 |
|------|------|------|------|
| 页面标题 | 20px | 600 | 28px |
| 模块标题 | 16px | 600 | 24px |
| 正文 | 14px | 400 | 22px |
| 辅助文字 | 12px | 400 | 20px |
| 表格文字 | 13px | 400 | 20px |

**间距系统**：
- 页面边距：24px
- 卡片内边距：16px
- 模块间距：16px / 24px
- 表格行高：48px（紧凑）/ 56px（标准）

### 7.2 全局布局规范

```
┌─────────────────────────────────────────────────────────────┐
│  顶部导航栏：Logo | 平台切换(Shopee/TikTok/TEMU/妙手) | [店铺切换▼] [通知🔔] [头像] │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  左侧导航    │  主工作区                                    │
│  （17项）    │  • 商品列表/订单列表/资金面板...              │
│              │  • 选品器四栏动态布局                         │
│  - 首页      │  • 数据分析看板                              │
│  - 商品      │  • 通知中心                                  │
│  - 订单      │                                              │
│  - 物流      │  底部操作栏：批量操作/导出/打印               │
│  - 营销      │                                              │
│  - 财务      │                                              │
│  - 数据      │                                              │
│  - 选品      │                                              │
│  - 店铺      │                                              │
│  - 通知      │                                              │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### 7.3 多平台多店铺产品管理页面

#### 7.3.1 页面布局

```
┌─────────────────────────────────────────────────────────────────┐
│ 顶部导航栏                                                      │
│ [Logo] [Shopee] [TikTok Shop] [TEMU] [妙手ERP]   [店铺切换▼] [通知🔔] [头像] │
├─────────────────────────────────────────────────────────────────┤
│ 筛选工具栏                                                      │
│ [商品名称搜索] [类目▼] [状态: 全部/在售中/未发布/已下架] [排序▼] [批量操作▼]        │
├──────────────┬──────────────────────────────────────────────────┤
│ 左侧分类树    │ 主体内容区                                      │
│              │                                                  │
│ ▼ 时尚配饰   │ ┌────────────────────────────────────────────┐  │
│   ▼ 包袋     │ │ 商品列表（表格/卡片/树状切换）               │  │
│     手提包   │ │ · 商品图片+标题+ID                          │  │
│     斜挎包   │ │ · 价格区间 · 库存 · L30D表现                │  │
│     钱包     │ │ · Smart Diagnosis / SPS / 优化事项          │  │
│   鞋履       │ │ · 操作：编辑/推广/复制/更多                  │  │
│              │ └────────────────────────────────────────────┘  │
│ ▼ 家居用品   │                                                  │
│              │ [分页: 1/30 每页12条]                            │
├──────────────┴──────────────────────────────────────────────────┤
│ 底部状态栏                                                      │
│ 商品总数: 409 | 架上: 354 | 违规: 55 | 发品额度: 0/400           │
└─────────────────────────────────────────────────────────────────┘
```

#### 7.3.2 视图切换交互

**三种视图模式**：

1. **表格视图**（默认）: 适合批量操作和数据分析
   - 可自定义显示列
   - 支持排序、筛选
   - 支持批量选择

2. **卡片视图**: 适合快速浏览和图片展示
   - 商品图片大尺寸展示
   - 关键信息卡片化
   - 适合移动端

3. **树状视图**: 适合类目丰富的商品管理
   - 左侧类目树展开
   - 右侧显示当前类目下商品
   - 支持拖拽归类

**切换方式**: 右上角视图切换按钮组

#### 7.3.3 商品卡片设计（卡片视图）

```
┌─────────────────────────────────┐
│ [商品图片]                       │
│                                  │
│ Portable Foldable Dog Bowl...   │ ← 标题截断(2行)
│                                  │
│ 商品ID: 52660404545             │
│                                  │
│ ₱429 - ₱688                    │ ← 价格区间
│                                  │
│ SKU: Yellow,350ml / ...         │ ← 变体折叠
│                                  │
│ 📦 库存: 500                     │
│ 📊 L30D Sales: 0                │
│                                  │
│ [SSP] [Hot Listing] [新品扶持]  │ ← 平台特色标签
│ [Smart Diagnosis: 1问题]        │
│                                  │
│ [编辑] [推广] [更多▼] [复制]     │ ← 操作按钮
└─────────────────────────────────┘
```

#### 7.3.4 表格视图设计

**核心列定义**：

| 列 | 宽度 | 可排序 | 说明 |
|----|------|--------|------|
| 勾选框 | 40px | — | 批量选择 |
| 商品信息 | 280px | 否 | 图片+标题+ID |
| 类目 | 160px | 是 | 三级类目路径 |
| 价格 | 120px | 是 | 售价区间 |
| 库存 | 80px | 是 | 总库存数 |
| 表现 | 140px | 是 | L30D销量/曝光 |
| 状态 | 100px | 是 | 上架状态标签 |
| 平台特性 | 160px | 否 | SSP/SPS/优化事项 |
| 操作 | 120px | 否 | 编辑/推广/更多 |

**平台特性列内容**：

| 平台 | 显示内容 |
|------|----------|
| Shopee | SSP编号、Hot Listing状态、Smart Diagnosis问题数 |
| TikTok Shop | SPS评分、CRM解锁状态 |
| TEMU | SPU/SKC ID、申报价格、优化事项 |
| 妙手ERP | 发布状态（未发布/定时发布/已发布） |

#### 7.3.5 筛选器交互

**筛选器区域**：

```
┌─────────────────────────────────────────────────────────────┐
│ 商品名称 [___________]  类目 [▼全部▼]  状态 [▼全部▼]        │
│ 价格区间 [₱______ - ₱______]  库存 [______ - ______]        │
│ 创建时间 [📅 开始日期 - 📅 结束日期]                         │
│ [查询] [重置] [展开高级筛选 ▼]                               │
└─────────────────────────────────────────────────────────────┘
```

**高级筛选扩展项**：
- 平台特性筛选（Shopee: SSP状态、Hot Listing；TikTok: SPS评分区间；Temu: 优化事项类型）
- 分组筛选
- 来源筛选（手动创建/采集）
- 同步状态筛选

#### 7.3.6 批量操作交互

**批量操作栏**（选中商品后出现）:

```
已选择 5 个商品  [批量发布] [批量编辑] [设置类目] [设置售价] [引用模板] [分组] [创建产品] [批量删除]
```

**批量发布流程**：
1. 选择目标平台 + 店铺/站点
2. 选择发布方式（立即发布/定时发布）
3. 预览差异字段（各平台必填字段缺失提示）
4. 确认发布 → 显示发布结果

**批量编辑弹窗**：
- 可编辑字段选择（标题、价格、库存、类目等）
- 批量修改规则（统一值/递增/递减/替换）
- 预览修改结果
- 确认应用

#### 7.3.7 权限隔离设计

**跨平台权限**：
- 每个平台独立授权，未授权平台在导航中隐藏或置灰
- 子账号权限由主账号配置，CBHunter继承平台权限

**跨境 vs 本地店权限**：
- TikTok Shop跨境账号部分模块无权限时，显示友好提示而非空白
- Shopee财务页面需要额外密码验证时，引导用户完成验证

**权限提示示例**：
```
┌─────────────────────────────────────────┐
│ ⚠️ 您暂无此页面权限                      │
│ 请联系主账号管理员获取相应权限。          │
│ 当前店铺: CocoTrip Shop (Cross Border)  │
│ 可能原因: 跨境店铺营销模块需额外授权      │
└─────────────────────────────────────────┘
```

### 7.4 上架编辑页交互规范（弹窗式编辑）

#### 7.4.1 页面结构

基于四平台编辑页面深度调研，CBHunter采用**弹窗式编辑**而非独立页面编辑。弹窗在列表页内打开，保持上下文，支持批量操作和图片编辑器集成。

```
┌─────────────────────────────────────────────────────────────────┐
│ ← 返回    添加商品 / 编辑商品              [保存草稿] [创建/更新] │
├──────────────────────┬──────────────────────────────────────────┤
│                      │                                        │
│   左侧步骤导航        │            右侧内容区                     │
│   (Shopee风格)       │                                          │
│                      │  ┌────────────────────────────────────┐  │
│  ① 基本信息           │  │ 标签页: 基本信息 | 销售资料 | 图片  │  │
│  ② 销售资料           │  │              | 物流 | 其他          │  │
│  ③ 图片管理           │  └────────────────────────────────────┘  │
│  ④ 物流设置           │                                          │
│  ⑤ 其他属性           │  ┌────────────────────────────────────┐  │
│                      │  │                                    │  │
│                      │  │  [取消] [保存草稿] [创建/更新] [发布]│  │
│                      │  └────────────────────────────────────┘  │
├──────────────────────┴──────────────────────────────────────────┤
│  iframe: 图片编辑器组件（可切换自研/易可图）                       │
└─────────────────────────────────────────────────────────────────┘
```

#### 7.4.2 弹窗层级结构

```
主弹窗（产品编辑）
├── 步骤导航栏（固定左侧）
├── 内容区（动态渲染）
│   ├── 基本信息标签页
│   │   ├── 商品图片上传区（最多9张，拖拽排序）
│   │   ├── 商品视频上传区
│   │   ├── 商品名称输入框（字符计数）
│   │   ├── 类目选择器（三级联动）
│   │   └── 商品描述富文本编辑器
│   │
│   ├── 销售资料标签页
│   │   ├── SKU管理表格（动态行列）
│   │   │   ├── 规格一输入
│   │   │   ├── 规格二输入
│   │   │   ├── SKU图片上传
│   │   │   ├── 价格/库存/货号
│   │   │   └── 体积/重量（TEMU）
│   │   ├── 定价区域
│   │   │   ├── Shopee/TikTok: 售价 + 原价
│   │   │   └── TEMU: 申报价格(CNY) + 开款价格状态
│   │   └── 批量导入/导出
│   │
│   ├── 图片管理标签页
│   │   ├── 主图管理（缩略图网格 + 拖拽排序）
│   │   ├── SKU图片管理（按SKU分组显示）
│   │   ├── 批量编辑按钮 → 打开iframe编辑器
│   │   └── 图片编辑器iframe
│   │
│   ├── 物流设置标签页
│   │   ├── 物流渠道选择（按国别动态加载）
│   │   ├── 重量/尺寸
│   │   └── 发货天数/备货仓组（TEMU）
│   │
│   └── 其他属性标签页
│       ├── 品牌选择
│       ├── 类目动态属性（Schema驱动）
│       ├── 合规信息（TEMU强制：资质/实拍图/合规信息）
│       └── 自定义扩展字段
│
└── 底部操作栏
    ├── 取消
    ├── 保存草稿
    ├── 创建/更新
    └── 创建并发布/更新并发布
```

#### 7.4.3 动态表单渲染逻辑

**类目选择触发链**：

```
选择L1类目
  → 加载L2类目列表
    → 选择L2类目
      → 加载L3类目列表
        → 选择L3类目
          → 加载类目属性Schema
            → 渲染动态表单字段
              → 更新销售资料/运费/其他Tab可用状态
```

**动态字段加载状态**：

| 状态 | 显示 |
|------|------|
| 未选择类目 | "请先选择商品类目" + 类目选择器disabled |
| 加载中 | 骨架屏/Skeleton + Loading动画 |
| 加载完成 | 显示完整表单字段 |
| 加载失败 | 错误提示 + 重试按钮 |

#### 7.4.4 销售资料 Tab 字段

**SKU管理区域（两层规格模式）**：

```
┌─────────────────────────────────────────────────────────────┐
│ SKU管理                                                     │
│ [+ 添加规格] [批量导入Excel]                                 │
│                                                             │
│ ┌──────────┬──────────┬──────────┬──────────┬──────────┐    │
│ │ 规格名称  │ 价格     │ 原价     │ 库存     │ 货号     │    │
│ ├──────────┼──────────┼──────────┼──────────┼──────────┤    │
│ │ Yellow   │ ₱429     │ ₱612     │ 500      │ [____]   │    │
│ │ Green    │ ₱429     │ ₱612     │ 500      │ [____]   │    │
│ │ Blue     │ ₱482     │ ₱688     │ 500      │ [____]   │    │
│ └──────────┴──────────┴──────────┴──────────┴──────────┘    │
│                                                             │
│ [添加新规格]                                                  │
└─────────────────────────────────────────────────────────────┘
```

**Temu SKU管理增强（三层结构）**：

```
┌─────────────────────────────────────────────────────────────┐
│ SKU管理 (Temu SPU→SKC→SKU三层结构)                          │
│                                                             │
│ SPU: [自动生成/手动输入]                                     │
│ SKC: [自动生成/手动输入]                                     │
│                                                             │
│ ┌──────────┬──────────┬──────────┬──────────┬──────────┐    │
│ │ 颜色/规格 │ 体积(cm) │ 重量(g) │ 申报价格 │ 库存     │    │
│ ├──────────┼──────────┼──────────┼──────────┼──────────┤    │
│ │ 黑色     │ 12×8×4   │ 80       │ ¥14.8    │ 500      │    │
│ │ 浅棕色   │ 12×8×4   │ 80       │ ¥14.8    │ 500      │    │
│ └──────────┴──────────┴──────────┴──────────┴──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

#### 7.4.5 图片管理 Tab 字段

参考妙手ERP的双层弹窗架构，图片管理作为独立标签页：

```
┌─────────────────────────────────────────────────────────────┐
│ 图片管理                                                    │
│                                                             │
│ 主图管理                                                    │
│ [图1] [图2] [图3] [图4] [图5] [图6] [图7] [图8] [图9]      │
│ ↑ 拖拽排序                                                  │
│                                                             │
│ SKU图片管理                                                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ SKU: 红色/小号                                          │ │
│ │ [SKU图1] [SKU图2] [SKU图3] [+添加]                      │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ SKU: 蓝色/中号                                          │ │
│ │ [SKU图1] [SKU图2] [+添加]                               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ [批量编辑图片 → 打开iframe编辑器]                             │
│                                                             │
│ iframe: 易可图图片编辑器                                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 调整 | 裁剪旋转 | 文字 | 标记 | 主图模板 | AI设计 | ...  │ │
│ │                                                         │ │
│ │ [图片画布区域]                                           │ │
│ │                                                         │ │
│ │ [保存] [取消]                                            │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 7.4.6 批量编辑弹窗

参考妙手ERP的批量编辑弹窗，支持以下批量操作：

```
┌─────────────────────────────────────────────────────────────┐
│ 批量编辑                                                    │
│                                                             │
│ 编辑模式: ○ 统一值  ○ 递增  ○ 递减  ○ 替换                   │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 商品标题    [批量标题优化 ▼]                             │ │
│ │ 商品图片    [批量编辑图片 → iframe编辑器]                │ │
│ │ SKU规格     [表格内直接编辑]                             │ │
│ │ 售价        [+10% / ×1.1 / 统一值___]                    │ │
│ │ 类目        [类目选择器 ▼]                               │ │
│ │ 描述        [富文本编辑器]                               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ [预览修改结果] [确认应用] [取消]                              │
└─────────────────────────────────────────────────────────────┘
```

#### 7.4.7 运费 Tab 字段

```
┌─────────────────────────────────────────────────────────────┐
│ 运费设置                                                    │
│                                                             │
│ 物流渠道 *                                                   │
│ [Express International ▼]                                   │
│                                                             │
│ 运费模板 *                                                   │
│ [标准运费模板 ▼]                                              │
│                                                             │
│ 商品重量 (g) *                                               │
│ [____]                                                        │
│                                                             │
│ 商品尺寸 (cm) *                                              │
│ 长 [____] × 宽 [____] × 高 [____]                            │
│                                                             │
│ 跨境物流选项                                                  │
│ □ 支持COD  □ 支持货到付款                                    │
│                                                             │
│ 预计运费: ₱15.00 - ₱25.00                                   │
└─────────────────────────────────────────────────────────────┘
```

#### 7.4.8 其他 Tab 字段

```
┌─────────────────────────────────────────────────────────────┐
│ 其他信息                                                    │
│                                                             │
│ 商品属性 (根据类目动态加载)                                    │
│ 风格: [休闲 ▼]                                               │
│ 护理说明: [干布清洁 ▼]                                       │
│ 材料: [帆布 ▼]                                               │
│ 闭合类型: [拉链 ▼]                                           │
│                                                             │
│ 合规信息 (Temu强制)                                           │
│ □ 商品资质已上传  □ 实拍图已上传  □ 合规信息已补充             │
│                                                             │
│ 认证要求 (按国别/类目动态加载)                                  │
│ NCC认证: [Model Name ___] [Registration ID ___]              │
│ Anatel认证: [生产商 ___]                                     │
│                                                             │
│ 自定义字段                                                    │
│ [字段名] [字段值]                                             │
│ [+ 添加自定义字段]                                            │
└─────────────────────────────────────────────────────────────┘
```

#### 7.4.9 表单校验规则

| 字段 | 校验规则 | 错误提示 |
|------|----------|----------|
| 商品名称 | 必填，1-180字符 | 请输入商品名称（1-180字符） |
| 类目 | 必填，必须选择三级类目 | 请选择商品类目 |
| 商品描述 | 必填，1-5000字符 | 请输入商品描述（最多5000字符） |
| 商品图片 | 必填，至少1张 | 请上传至少1张商品图片 |
| SKU价格 | 必填，正数 | 请输入有效的销售价格 |
| SKU库存 | 必填，非负整数 | 请输入有效的库存数量 |
| 商品重量 | 必填，正数 | 请输入有效的商品重量 |
| 商品尺寸 | 必填，长宽高>0 | 请输入有效的商品尺寸 |
| Temu供货价 | 必填，正数 | 请输入有效的申报价格 |
| Temu资质 | 必填（全托管） | 请上传商品资质文件 |
| Temu实拍图 | 必填（全托管） | 请上传商品实拍图 |

#### 7.4.10 发布确认弹窗

```
┌─────────────────────────────────────────────────────────────┐
│ 确认发布商品                                                  │
│                                                               │
│ 商品: Portable Foldable Dog Bowl...                          │
│ 目标平台: Shopee Philippines                                 │
│ 目标店铺: cocotrip.ph                                        │
│ 发布方式: 立即发布                                            │
│                                                               │
│ 以下字段将在发布时覆盖:                                        │
│ • 类目: 包袋 > 手提包 > 通勤手提包                            │
│ • 价格: ₱429 - ₱688                                         │
│ • 库存: 500 (每SKU)                                           │
│                                                               │
│ □ 我已确认以上信息无误                                        │
│                                                               │
│ [取消] [确认发布]                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.5 活动配置页交互规范

#### 7.5.1 Shopee 折扣活动配置

```
┌─────────────────────────────────────────────────────────────┐
│ 创建折扣活动                                                  │
│                                                               │
│ 活动名称 *                                                    │
│ [☀️新产品测品折扣____________________________]                 │
│                                                               │
│ 促销活动类型 *                                                │
│ ○ 套装优惠 (Buy X Get Y / Any N enjoy X% off)                │
│ ○ 我的折扣活动 (自定义折扣)                                    │
│ ○ 分类折扣 (按商品分类设置)                                    │
│                                                               │
│ 商品范围 *                                                    │
│ ○ 全部商品                                                    │
│ ○ 指定商品 [+ 添加商品]                                       │
│ ○ 指定分类 [+ 添加分类]                                       │
│                                                               │
│ 折扣规则 *                                                    │
│ 买 [3] 件 享 [2]% 折扣                                        │
│                                                               │
│ 活动期间 *                                                    │
│ [📅 2026-07-20] 至 [📅 2026-12-31]                           │
│                                                               │
│ 关联商品数: +13                                                │
│                                                               │
│ [取消] [保存草稿] [创建活动]                                   │
└─────────────────────────────────────────────────────────────┘
```

#### 7.5.2 Shopee 优惠券配置

```
┌─────────────────────────────────────────────────────────────┐
│ 创建优惠券                                                    │
│                                                               │
│ 优惠券活动名称 *                                              │
│ [新买家优惠卷____________________]                             │
│ 优惠券码: COCOA4MOM (自动生成/自定义)                          │
│                                                               │
│ 优惠券类型 *                                                  │
│ ○ 店铺优惠券  ○ 商品优惠券  ○ 非公开优惠券                    │
│ ○ 直播优惠券  ○ 短视频优惠券  ○ 新买家优惠券                  │
│ ○ 回购买家优惠券  ○ 关注礼优惠券                              │
│                                                               │
│ 适用商品范围 *                                                │
│ ○ 全部商品                                                    │
│ ○ 指定商品 [+ 添加商品]                                       │
│                                                               │
│ 目标买家 *                                                    │
│ ○ 所有买家  ○ 店铺粉丝  ○ 新买家  ○ 近期消费买家              │
│                                                               │
│ 折扣金额 *                                                    │
│ [80] ₱                                                        │
│                                                               │
│ 可使用总数 *                                                  │
│ [100000]                                                      │
│                                                               │
│ 优惠券领取期间 *                                              │
│ [📅 2026-07-07 04:50] 至 [📅 2026-09-18 05:50]               │
│                                                               │
│ 已使用: 0 / 100000                                            │
│                                                               │
│ [取消] [保存草稿] [创建优惠券]                                 │
└─────────────────────────────────────────────────────────────┘
```

#### 7.5.3 TikTok Shop CRM聊天计划配置

```
┌─────────────────────────────────────────────────────────────┐
│ 创建聊天计划                                                  │
│                                                               │
│ 访问条件检查:                                                 │
│ ✅ SPS评分: 3.8 (≥3.5 满足)                                  │
│ ✅ GMV: ₱12,500 (>0 满足)                                   │
│                                                               │
│ 计划类型 *                                                    │
│ ○ 一次性计划  ○ 自动计划                                      │
│                                                               │
│ 模板选择 *                                                    │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ 分享热销商品 (3928位商家已采用)                           │   │
│ │ 发布新品上市公告 (1742位商家已采用)                       │   │
│ │ 推广直播、促销及活动                                      │   │
│ │ 将粉丝转化为客户                                          │   │
│ │ 推动客户复购                                              │   │
│ │ 赢回不活跃客户                                            │   │
│ │ 邀请客户提交评价和反馈                                    │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│ 自动计划模板:                                                  │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ 推广直播活动 (转化率高)                                   │   │
│ │ 开始直播提醒                                              │   │
│ │ 降价提醒 (转化率高)                                       │   │
│ │ 挽回已加购未下单商品 (转化率高)                            │   │
│ │ 挽回未完成结账订单 (转化率高)                              │   │
│ │ 售后感谢 (转化率高)                                       │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│ 消息内容 *                                                    │
│ [自定义消息内容...]                                             │
│                                                               │
│ 配额: 本周总配额: 1000 / 剩余: 856                             │
│                                                               │
│ [取消] [保存草稿] [创建计划]                                   │
└─────────────────────────────────────────────────────────────┘
```

#### 7.5.4 Temu 商品优化事项处理

```
┌─────────────────────────────────────────────────────────────┐
│ 商品优化事项                                                  │
│                                                               │
│ 🔴 高价商品流量下降中                                          │
│    商品: 女款千鸟格爱心零钱包                                  │
│    建议: 调整申报价格以提升竞争力                                │
│    [去处理] [忽略]                                             │
│                                                               │
│ 🟡 建议零售价待填写 (2个待处理)                                 │
│    商品: 免抽气压缩袋                                          │
│    商品: 波西米亚复古指环套装                                   │
│    [批量去处理]                                                │
│                                                               │
│ 🟡 商品分类错误待修正 (1个待修正)                               │
│    商品: XXX                                                   │
│    [去修正]                                                    │
│                                                               │
│ 🟢 流量扶持待领取 (0个)                                        │
│ 🆕 传视频得免费流量加权 (新功能)                                │
│ 🟡 商品流量待关注 (5个)                                        │
│ 🟡 申报价格待关注 (0个)                                        │
│ 🟢 享备货权益待领取 (0个)                                      │
│                                                               │
│ [刷新] [标记全部已读]                                           │
└─────────────────────────────────────────────────────────────┘
```

### 7.6 订单资金页交互规范

#### 7.6.1 订单列表页

```
┌─────────────────────────────────────────────────────────────┐
│ 我的订单                                                     │
│                                                               │
│ [全部(302)] [待付款] [待出货] [运送中] [已完成] [退货退款取消(2)] │
│                                                               │
│ 订单编号 [________] 物流渠道 [所有渠道▼] [📅 2026/06/20 - 2026/07/20] │
│ [搜索] [重置] [导出]                                          │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ ☑ 订单编号    买家      商品          金额      状态     │   │
│ │ 260701GAP3... bj__ji1j91 [3-Way...] x1  ₱353  已完成   │   │
│ │               MariBank Savings   Express Int'l          │   │
│ │               运单: PH263130150995O                     │   │
│ │                                                         │   │
│ │ ☐ 2606058J2...  [Couple...] x3 ₱2,349  已取消          │   │
│ │               货到付款   Express Int'l                  │   │
│ │               取消原因: 已被买家取消                     │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│ [批量出货] [导出] [打印面单]                                   │
│ 1/30 页                                                       │
└─────────────────────────────────────────────────────────────┘
```

#### 7.6.2 订单详情页（抽屉式）

```
┌─────────────────────────────────────────────────────────────┐
│ ← 返回    订单详情                              [打印] [关闭] │
├─────────────────────────────────────────────────────────────┤
│ 订单信息                                                      │
│ 订单编号: 260701GAP3P1J9                                     │
│ 下单日期: 2026-07-01 14:30                                   │
│ 状态: ✅ 已完成                                              │
│ 支付方式: MariBank Savings                                   │
│ 物流渠道: Express International (快速渠道 - 内地)             │
│ 运单号: PH263130150995O [复制]                               │
│ 发货时限: 2026-07-05 23:59                                   │
│                                                               │
│ 商品明细                                                      │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ [图片] [3-Way Wear] 2026 Soft PU Leather Tote Bag...   │  │
│ │ 规格: Coffee  数量: x1  单价: ₱353                     │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                               │
│ 金额明细                                                      │
│ 商品金额: ₱353                                                │
│ 运费: ₱0.00                                                   │
│ 平台佣金: ₱15.00                                              │
│ 支付手续费: ₱3.53                                             │
│ 实收金额: ₱334.47                                             │
│                                                               │
│ 操作                                                          │
│ [查看详情] [评价] [联系买家] [申请退款]                        │
└─────────────────────────────────────────────────────────────┘
```

#### 7.6.3 资金概览页

```
┌─────────────────────────────────────────────────────────────┐
│ 我的收入                                                     │
│                                                               │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│ │ 待结算金额   │ 本月收入    │ 累计收入    │ 钱包余额    │   │
│ │ ₱12,500.00  │ ₱45,200.00 │ ₱128,000.00 │ ₱8,300.00  │   │
│ └─────────────┴─────────────┴─────────────┴─────────────┘   │
│                                                               │
│ 结算周期: 每月15日 / 28日                                      │
│ 收款账户: ***1234 (MariBank)                                  │
│                                                               │
│ 收入明细                                                      │
│ ┌─────────────────────────────────────────────────────────┐   │
│ │ 日期        订单号      金额        佣金    实收        │   │
│ │ 07-20       260701...   ₱353.00    ₱15.00  ₱334.47    │   │
│ │ 07-19       260701...   ₱2,349.00  ₱99.00  ₱2,184.00  │   │
│ │ ...                                                     │   │
│ └─────────────────────────────────────────────────────────┘   │
│                                                               │
│ [提现] [查看对账单] [设置收款账户]                              │
└─────────────────────────────────────────────────────────────┘
```

#### 7.6.4 Temu 库存管理页

```
┌─────────────────────────────────────────────────────────────┐
│ 库存管理                                                     │
│                                                               │
│ 商品: 女款千鸟格爱心零钱包                                    │
│ SPU: 4641171973  SKC: 75910152523  备货仓组: 广东仓组1        │
│ 申报价格: ¥14.8  开款价格状态: 已生效                          │
│                                                               │
│ 仓内库存                                                      │
│ 可用: 500  预占用: 50  暂不可用: 0  实物: 550                 │
│                                                               │
│ 卖家仓库存                                                    │
│ 建议目标库存天数: 15天  建议备货量: 200  可售天数: 30天        │
│                                                               │
│ 销售趋势                                                      │
│ [今日] [近7天] [近30天]                                       │
│ 今日销量: 5  7天销量: 32  30天销量: 128                        │
│                                                               │
│ [申请备货] [备货详情] [发起调价] [修改卖家仓库存]              │
│ [销售趋势图表] [Excel修改卖家仓库存]                           │
└─────────────────────────────────────────────────────────────┘
```

### 7.7 选品器现代化交互范式（股票选股器范式）

#### 7.7.1 四栏动态布局（v2）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  左侧策略库(20%) │ 中央可视化策略流程图(45%) │ 右侧智能面板(20%) │ 底部结果栏(15%) │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────────────────┐  ┌──────────────┐  │
│  │ 策略库搜索        │  │                              │  │ AI推荐       │  │
│  │ [🔍 搜索策略...]   │  │    可视化策略流程图画布       │  │              │  │
│  │                  │  │                              │  │ 相似策略     │  │
│  │ ▼ 爆款驱动 BS     │  │  ┌──────┐  ∩  ┌──────┐     │  │ ·BS-01+BL-01 │  │
│  │ ├ BS-01 [A]      │  │  │BS-01 │──→│BL-01 │     │  │ 历史命中率高 │  │
│  │ ├ BS-02 [A]      │  │  └──────┘     └──────┘     │  │              │  │
│  │ ├ BS-03 [A]      │  │       ∩                    │  │ 互补策略     │  │
│  │ └ ...             │  │  ┌──────┐                 │  │ ·PF-01       │  │
│  │                  │  │  │PF-01 │                 │  │ ·CP-02       │  │
│  │ ▼ 蓝海挖掘 BL     │  │  └──────┘                 │  │ ·RP-05       │  │
│  │ ├ BL-01 [A]      │  │                              │  │              │  │
│  │ ├ BL-02 [A]      │  │  节点卡片：策略ID+名称+数据级别颜色编码 │  │ 风险预警     │  │
│  │ └ ...             │  │  A级=绿色 B级=蓝色 C级=黄色 D级=灰色    │  │ ·RC-01       │  │
│  │                  │  │  连线带运算符号(∩/∪/\)             │  │ ·LC-04       │  │
│  │ ▼ 利润导向 PF     │  │  点击节点→右侧显示参数配置          │  │              │  │
│  │ ├ PF-01 [C]      │  │  拖拽节点→画布自动建连线            │  │ 权重调节     │  │
│  │ └ ...             │  │  右键菜单→删除/嵌套/设置权重         │  │ w_sales:██░░ │  │
│  │                  │  │                              │  │ w_profit:████ │  │
│  │ ▼ 竞争分析 CP     │  │                              │  │ w_comp:█░░░░ │  │
│  │ ├ CP-01 [A]      │  │                              │  │ ...          │  │
│  │ └ ...             │  │                              │  │              │  │
│  │                  │  │                              │  │ 实时预览     │  │
│  │ ▼ 趋势洞察 TR     │  │                              │  │ 预估命中: 15 │  │
│  │ ├ TR-01 [A]      │  │                              │  │ 数据缺失: 1  │  │
│  │ └ ...             │  │                              │  │              │  │
│  │                  │  │                              │  │ 智能合并推荐 │  │
│  │ ▼ 合规风控 RC     │  │                              │  │ 建议叠加...  │  │
│  │ ├ RC-01 [A]      │  │                              │  │              │  │
│  │ └ ...             │  │                              │  │              │  │
│  │                  │  │                              │  │              │  │
│  │ ▼ 复购类 RP(v2)   │  │                              │  │              │  │
│  │ ├ RP-01~RP-08    │  │                              │  │              │  │
│  │                  │  │                              │  │              │  │
│  │ ▼ 生命周期LC(v2)  │  │                              │  │              │  │
│  │ ├ LC-01~LC-08    │  │                              │  │              │  │
│  │                  │  │                              │  │              │  │
│  │ ──────────────── │  │                              │  │              │  │
│  │ 我的策略          │  │                              │  │              │  │
│  │ 公共模板          │  │                              │  │              │  │
│  │ 自定义分组        │  │                              │  │              │  │
│  │ [+ 新建分组]      │  │                              │  │              │  │
│  └──────────────────┘  └──────────────────────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│  底部结果栏                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ 候选商品池(Tab: 列表/表格/图表) | 标杆样例 | 趋势图表 | 联动操作      │    │
│  │                                                                     │    │
│  │ [商品图片] Portable Foldable Dog Bowl...                            │    │
│  │ 平台: TikTok PH | 类目: 宠物用品 | 销量L7: 1,234 | 评分: 4.8       │    │
│  │ 策略得分: BS-01=95, BL-01=88, PF-01=72                             │    │
│  │ [雷达图: 六维权重得分] [生命周期阶段: 成长期] [风险评估: 低]          │    │
│  │ [收藏到素材库] [转为草稿] [上架到店铺] [加入白名单]                   │    │
│  │                                                                     │    │
│  │ ─────────────────────────────────────────────────────────────         │    │
│  │ [分页: 1/30 每页12条]                                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 7.7.2 左侧策略库面板详细设计

**策略卡片样式**：
```
┌─────────────────────────────────┐
│ ● BS-01  平台榜单Top N           │ ← 策略ID + 名称
│   数据级别: [A级] 绿色标签       │ ← ABCD颜色编码
│   适配: TikTok/Shopee/Temu       │
│   [★ 收藏] [▶ 添加到画布]        │
└─────────────────────────────────┘
```

**策略库分类导航**：
| 分类 | 前缀 | 数量 | 默认颜色 |
|------|------|------|----------|
| 爆款驱动 | BS | 8 | #EE4D2D (Shopee橙) |
| 蓝海挖掘 | BL | 8 | #1890FF (主色蓝) |
| 利润导向 | PF | 8 | #52C41A (成功绿) |
| 竞争分析 | CP | 8 | #FAAD14 (警告黄) |
| 趋势洞察 | TR | 8 | #722ED1 (紫色) |
| 合规与风控 | RC | 8 | #F5222D (危险红) |
| 复购类 | RP | 8 | #13C2C2 (青色) |
| 生命周期类 | LC | 8 | #2F54EB (蓝色) |

**策略库操作**：
- 分类折叠/展开
- 关键词搜索（策略ID/名称/描述）
- 收藏策略置顶
- 我的策略 / 公共模板 / 自定义分组 三个Tab切换
- 长按拖拽策略卡片到画布

#### 7.7.3 中央可视化策略流程图详细设计

**节点卡片结构**：
```
┌─────────────────────────────────┐
│ BS-01  平台榜单Top N             │
│ ─────────────────────────────   │
│ 数据级别: A级 [绿色圆点]         │
│ 适配平台: TikTok/Shopee/Temu     │
│ 参数: TopN=50, 时间=7d          │
│ 状态: ✅ 已配置                   │
│ ─────────────────────────────   │
│ [⚙ 参数] [📊 胜率] [✕ 删除]     │
└─────────────────────────────────┘
```

**连线与运算符号**：
```
[BS-01] ──∩──→ [BL-01] ──∩──→ [PF-01]
               ↑
            [TR-02] ──∪──→

连线类型：
├── 实线 → 交集（∩）
├── 虚线 → 并集（∪）
├── 点划线 → 差集（\）
└── 双线 → 加权评分（Σ）

连线可点击切换运算类型
```

**画布操作**：
| 操作 | 方式 | 说明 |
|------|------|------|
| 添加节点 | 从策略库拖拽到画布 | 自动创建叶子节点 |
| 建连线 | 拖拽节点边缘连接点 | 自动生成运算连线 |
| 移动节点 | 拖拽节点主体 | 实时更新连线位置 |
| 删除节点 | 右键→删除 / Delete键 | 同时删除关联连线 |
| 插入嵌套 | 右键→嵌入为新复合策略 | 将多个节点包裹为子复合策略 |
| 添加负向规则 | 拖拽NF规则到画布 | 负向筛选一等公民 |
| 设置权重 | 点击节点→权重滑块 | 0-1可调 |
| 画布缩放 | Ctrl+滚轮 / 右下角滑块 | 支持全局缩放到25%-400% |
| 展开/折叠嵌套 | 点击复合策略节点标题 | 查看/隐藏内部结构 |

**运算符切换交互**：
```
点击连线 → 弹出运算类型选择器
┌─────────────────────┐
│ 选择运算类型          │
│ ○ 交集 ∩             │
│ ○ 并集 ∪             │
│ ○ 差集 \             │
│ ○ 加权评分 Σ         │
│                       │
│ 加权权重: [0.5]       │
│ [确认] [取消]          │
└─────────────────────┘
```

#### 7.7.4 右侧智能面板详细设计

**AI推荐区域**：
```
┌─────────────────────────────────┐
│ 🤖 AI策略推荐                    │
│                                 │
│ 相似策略：                       │
│ ┌─────────────────────────────┐ │
│ │ "TikTok菲律宾包袋爆款"        │ │
│ │ 命中率: 72% | 首月出单率: 67% │ │
│ │ [添加到画布]                  │ │
│ ├─────────────────────────────┤ │
│ │ "Shopee马来站3C配件蓝海"      │ │
│ │ 命中率: 65% | 首月出单率: 58% │ │
│ │ [添加到画布]                  │ │
│ └─────────────────────────────┘ │
│                                 │
│ 互补策略：                       │
│ · PF-01(毛利率筛选) — 补充利润   │
│ · CP-02(价格战规避) — 补充竞争   │
│ · RP-05(稳定日销款) — 补充复购   │
│                                 │
│ 风险预警：                       │
│ ⚠ RC-01(禁限售规避) — 该类目存在合规风险 │
│ ⚠ LC-04(衰退期预警) — 部分商品已进入衰退期 │
│                                 │
│ 智能合并推荐：                    │
│ 💡 建议叠加 LC-02(成长期加速) 观察趋势 │
└─────────────────────────────────┘
```

**权重调节区域**：
```
┌─────────────────────────────────┐
│ ⚖️ 权重调节                      │
│                                 │
│ 预设模板: [爆款优先▼] [保存为模板]│
│                                 │
│ 销量权重: ████████░░ 0.30       │
│ 利润权重: ██████████ 0.35       │
│ 竞争度:   ████░░░░░░ 0.15       │
│ 趋势:     ██████░░░░ 0.10       │
│ 复购:     ███░░░░░░░ 0.07       │
│ 合规:     ██░░░░░░░░ 0.03       │
│ ─────────────────────────────   │
│ 综合得分 = Σ(w_i × score_i)     │
│                                 │
│ [重置为默认] [应用并重新计算]     │
└─────────────────────────────────┘
```

**实时预览区域**：
```
┌─────────────────────────────────┐
│ 👁 实时预览                      │
│                                 │
│ 预估命中商品数: 15               │
│ 数据完整性: 85%                  │
│ 数据缺失策略: TR-03(节日营销)    │
│                                 │
│ 各策略贡献度:                    │
│ BS-01: ██████████ 35%           │
│ BL-01: ███████░░░ 28%           │
│ PF-01: █████░░░░░ 18%           │
│ TR-02: ████░░░░░░ 12%           │
│ 其他:  7%                       │
│                                 │
│ [运行选品]                       │
└─────────────────────────────────┘
```

#### 7.7.5 负向筛选面板详细设计

```
┌─────────────────────────────────┐
│ 🚫 负向筛选规则                  │
│                                 │
│ 已启用规则:                      │
│ ☑ NF-01 排除高退货率 [阈值: 5%] │
│ ☑ NF-02 排除低利润 [阈值: 10%]  │
│ ☐ NF-03 排除高竞争 [阈值: 60%]  │
│ ☑ NF-04 排除违规风险             │
│ ☐ NF-05 排除价格战               │
│ ☐ NF-06 排除衰退品               │
│ ☐ NF-07 排除低评分 [阈值: 3.5]  │
│ ☐ NF-08 排除同质化 [阈值: 80%]  │
│                                 │
│ AI推荐排除规则：                  │
│ 💡 基于当前策略，建议启用：        │
│ · NF-05(排除价格战) — 该类目     │
│   最低价已无利润空间              │
│ · NF-07(排除低评分) — 竞品评分   │
│   普遍偏低                       │
│                                 │
│ 实时影响预览：                    │
│ 排除前: 50个商品                 │
│ 排除后: 15个商品（排除率70%）     │
│ 被排除商品明细: [查看列表]        │
│                                 │
│ [+ 添加自定义负向规则]            │
└─────────────────────────────────┘
```

#### 7.7.6 底部结果栏详细设计

**候选商品列表视图**：
```
┌─────────────────────────────────────────────────────────────────────┐
│ 候选商品池                          Tab: [列表] [表格] [图表]       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ [商品图片] Portable Foldable Dog Bowl...                       │ │
│ │ 平台: TikTok PH | 类目: 宠物用品 | L7销量: 1,234 | 评分: 4.8  │ │
│ │                                                                     │ │
│ │ 策略得分雷达图:                                                       │ │
│ │   销量:██████████ 95   利润:██████░░░ 72   竞争:████████░░ 88       │ │
│ │   趋势:█████░░░░ 55   复购:████░░░░░ 40   合规:██████████ 95       │ │
│ │                                                                     │ │
│ │ 生命周期阶段: 🟢 成长期    风险评估: 🟢 低    置信度: 🟢 高          │ │
│ │                                                                     │ │
│ │ [收藏到素材库] [转为草稿] [上架到店铺] [加入白名单] [查看详情]        │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ [商品图片] ...                                                  │ │
│ │ ...                                                             │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│ 分页: 1/30 每页12条                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

**表格视图列定义**：

| 列 | 宽度 | 可排序 | 说明 |
|----|------|--------|------|
| 勾选框 | 40px | — | 批量选择 |
| 商品信息 | 280px | 否 | 图片+标题+ID |
| 平台/国别 | 120px | 是 | 来源平台+站点 |
| 类目 | 160px | 是 | 三级类目路径 |
| 价格 | 120px | 是 | 售价区间 |
| 销量 | 100px | 是 | L7/L30D销量 |
| 策略得分 | 160px | 是 | 综合得分+各策略得分 |
| 生命周期 | 100px | 是 | 新品期/成长期/成熟期/衰退期 |
| 风险等级 | 80px | 是 | 低/中/高 |
| 操作 | 200px | 否 | 收藏/草稿/上架/白名单/详情 |

**标杆样例区域**：
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🏆 标杆样例商品                                                     │
│                                                                     │
│ 本策略组合在以下商品上表现最佳：                                     │
│                                                                     │
│ [图1] 商品A  命中率92%  首月销量1,200  毛利率38%                     │
│ [图2] 商品B  命中率88%  首月销量980   毛利率32%                     │
│ [图3] 商品C  命中率85%  首月销量750   毛利率41%                     │
│                                                                     │
│ [一键收藏全部到素材图库] [导出标杆分析]                               │
└─────────────────────────────────────────────────────────────────────┘
```

**趋势图表区域**：
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📈 趋势图表                                                         │
│                                                                     │
│ [近7天] [近30天] [近90天]                                           │
│                                                                     │
│ 候选商品销量趋势: [折线图]                                          │
│ 类目热度趋势: [面积图]                                              │
│ 价格分布: [直方图]                                                  │
│ 竞争度变化: [柱状图]                                                │
│                                                                     │
│ [导出数据] [分享图表]                                               │
└─────────────────────────────────────────────────────────────────────┘
```

**联动操作入口**：
| 操作 | 说明 | 目标模块 |
|------|------|----------|
| 收藏到素材库 | 标杆商品图片/视频收藏 | 素材图库模块 |
| 转为草稿 | 选品结果转化为待发布商品草稿 | 商品编辑模块 |
| 上架到店铺 | 直接发布到授权店铺 | 多店铺同步模块 |
| 加入白名单 | 加入负向筛选白名单必保商品 | 选品引擎 |
| 查看胜率回溯 | 查看该策略历史表现 | 策略胜率看板 |
| 衍生策略 | 基于当前组合生成变体策略 | 策略衍生引擎 |

#### 7.7.7 策略效果回溯看板UI

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 策略胜率看板                                                     │
│                                                                     │
│ 策略 CS-001 历史表现（近90天）                                      │
│                                                                     │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┐           │
│ │ 执行次数    │ 平均命中    │ 平均首月出单│ 平均毛利率  │           │
│ │ 12次        │ 23个        │ 67%         │ 34.2%       │           │
│ └─────────────┴─────────────┴─────────────┴─────────────┘           │
│                                                                     │
│ 最佳一次: 45个候选，32个出单                                        │
│ 最差一次: 8个候选，2个出单                                          │
│                                                                     │
│ 胜率趋势图: [📈 近30天上升]                                         │
│                                                                     │
│ 归因分析:                                                            │
│ ├── 有利因素: 权重配置合理、数据源稳定                                │
│ ├── 不利因素: TR-07数据缺失导致偏差、PF-01成本数据过期                │
│ └── 优化建议: 提高PF-01权重至0.35，补充RP-05策略                     │
│                                                                     │
│ 波动分析: [波动曲线图]                                              │
│ 结果波动监控: [异常检测告警]                                         │
│                                                                     │
│ [回测验证] [导出胜率报告]                                            │
└─────────────────────────────────────────────────────────────────────┘
```

#### 7.7.8 AI自然语言生成交互

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🤖 AI策略生成器                                                     │
│                                                                     │
│ 输入框:                                                            │
│ "我想在TikTok菲律宾站找包袋类目的蓝海爆款，要求毛利率30%以上"        │
│                                                                     │
│ AI解析结果:                                                        │
│ ├── 平台: TikTok                                                   │
│ ├── 国别: 菲律宾(PH)                                                │
│ ├── 类目: 包袋                                                      │
│ ├── 时间窗口: 7天                                                   │
│ ├── 利润要求: 毛利率≥30%                                            │
│ ├── 排除条件: 无                                                    │
│ └── 推荐策略组合:                                                   │
│     · BS-01(榜单Top50) — 爆款基础                                   │
│     · BL-01(低竞争高需求) — 蓝海筛选                                │
│     · PF-01(毛利率≥30%) — 利润保障                                │
│     · RP-05(稳定日销款) — 现金流补充                              │
│     · 负向: NF-01(高退货率), NF-04(违规风险)                     │
│                                                                     │
│ [✅ 策略已生成，可直接运行]                                          │
│ [💡 建议叠加 LC-02(成长期加速) 观察趋势]                             │
│ [⚠️ 注意：PF-01需要导入成本数据才能生效]                              │
│                                                                     │
│ [应用到画布] [保存为新策略] [导出JSON]                               │
└─────────────────────────────────────────────────────────────────────┘
```

#### 7.7.9 核心交互特性汇总

| 特性 | 说明 |
|------|------|
| 可视化策略流程图 | 节点卡片 + 带运算符号的连线，支持拖拽建连线、点击切换运算、画布缩放 |
| 策略库颜色编码 | A级=绿色、B级=蓝色、C级=黄色、D级=灰色，一目了然 |
| 实时参数预览 | 边改参数边看预估命中数，参数联动影响传播分析 |
| 智能推荐面板 | AI推荐相似策略/互补策略/风险预警；智能合并推荐 |
| 拖拽式搭建 | 7种拖拽操作（添加节点/建连线/移动/删除/插入嵌套/添加负向规则/设置权重） |
| 多层嵌套可视化 | 复合策略节点可展开/折叠查看内部结构 |
| 负向筛选一等公民 | 负向规则面板 + AI推荐排除规则 + 实时影响预览 |
| 策略效果回溯 | 胜率看板 + 波动分析 + 归因分析 + 结果波动监控 |
| AI自然语言生成 | 输入描述 → AI提取平台/国别/类目/时间窗口/利润要求/排除条件 → 匹配64条策略生成策略树 |
| 商品详情增强 | 各策略得分雷达图 + 生命周期阶段判断 + 风险评估 |

### 7.8 响应式设计规范

#### 7.8.1 断点定义

| 断点 | 宽度 | 适配策略 |
|------|------|----------|
| Desktop | ≥1440px | 完整表格视图，三列布局 |
| Laptop | 1024px - 1439px | 标准表格视图，两列布局 |
| Tablet | 768px - 1023px | 卡片视图优先，侧边栏可折叠 |
| Mobile | <768px | 简化列表，底部导航，单列布局 |

#### 7.8.2 移动端适配要点

- 商品列表切换为卡片视图
- 表格列可横向滚动
- 筛选器折叠为抽屉式
- 批量操作简化为单选模式
- 订单详情改为全屏页面

### 7.9 无障碍与国际化

#### 7.9.1 国际化支持

| 维度 | 实现方式 |
|------|----------|
| 界面语言 | 中文默认，支持英文/泰语/越南语/马来语/印尼语 |
| 货币格式化 | 按站点自动格式化（₱1,234.56 / S$1,234.56 / ¥14.80） |
| 日期格式 | 按站点本地化（MM/DD/YYYY vs DD/MM/YYYY） |
| 时区 | 自动转换为用户本地时区 |
| 数字分隔符 | 按地区习惯（1,000 vs 1.000） |

#### 7.9.2 无障碍要求

- 所有交互元素支持键盘操作
- 颜色对比度符合 WCAG 2.1 AA标准
- 表单错误提示同时使用颜色和文本
- 图片商品提供alt文本
- 屏幕阅读器兼容

---

## 八、数据库整体优化、新增表、字段规整方案

### 8.1 现有表结构优化

| 表名 | 优化内容 |
|------|----------|
| products | 增加platform_extension JSONB、country_config外键 |
| sku_table | 增加dimensions、weight_g、seller_sku_code字段 |
| orders | 增加order_status统一枚举、payment_method映射 |
| finance_records | 增加amount_cny、currency_code、settlement_date |
| logistics | 增加shipping_channel、tracking_number、dispatch_deadline |
| marketing_activities | 增加platform_code、country_code、shop_id |
| media_library | 增加product_id关联、image_type(主图/SKU图片) |
| shops | 增加shop_region(本地店/跨境店/全托管/半托管) |

### 8.2 完整SQL DDL（16张选品模块表）

#### 8.2.1 base_strategies — 原生策略定义表

```sql
CREATE TABLE base_strategies (
    strategy_id VARCHAR(10) PRIMARY KEY,          -- 如 BS-01
    strategy_name VARCHAR(100) NOT NULL,           -- 策略名称
    category VARCHAR(20) NOT NULL,                 -- 大类：爆款驱动/蓝海挖掘/利润导向/竞争分析/趋势洞察/合规风控/复购类/生命周期类
    prefix VARCHAR(5) NOT NULL,                    -- 前缀：BS/BL/PF/CP/TR/RC/RP/LC
    description TEXT NOT NULL,                     -- 策略描述
    data_feasibility CHAR(1) NOT NULL CHECK (data_feasibility IN ('A','B','C','D')),  -- 数据可行性等级
    platforms TEXT[] NOT NULL,                     -- 适配平台数组
    parameters_schema JSONB DEFAULT '{}',          -- 可参数化配置项(JSON Schema)
    thresholds_schema JSONB DEFAULT '{}',          -- 阈值调节项(JSON Schema)
    default_parameters JSONB DEFAULT '{}',         -- 默认参数值
    data_source_ref VARCHAR(50),                   -- 关联数据源ID（D级为空）
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','paused','deprecated')),
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_base_strategies_category ON base_strategies(category);
CREATE INDEX idx_base_strategies_feasibility ON base_strategies(data_feasibility);
CREATE INDEX idx_base_strategies_platforms ON base_strategies USING GIN(platforms);
CREATE UNIQUE INDEX idx_base_strategies_prefix_id ON base_strategies(prefix, strategy_id);

-- 64条种子数据
INSERT INTO base_strategies (strategy_id, strategy_name, category, prefix, description, data_feasibility, platforms, status) VALUES
('BS-01','平台榜单Top N','爆款驱动','BS','筛选各平台公域榜单前N名商品','A',ARRAY['tiktok','shopee','temu','amazon','lazada','aliexpress'],'active'),
('BS-02','飙升榜入选','爆款驱动','BS','近7天/30天销量增速前N的商品','A',ARRAY['tiktok','shopee','amazon'],'active'),
('BS-03','新品爆款','爆款驱动','BS','上架30天内销量突破阈值的商品','A',ARRAY['tiktok','shopee','amazon'],'active'),
('BS-04','类目冠军','爆款驱动','BS','某类目下销量/销售额第一的商品','A',ARRAY['tiktok','shopee','temu','amazon'],'active'),
('BS-05','多平台爆款交叉','爆款驱动','BS','同时在≥2个平台热销的同类商品','A',ARRAY['tiktok','shopee','temu','amazon'],'active'),
('BS-06','季节性爆款预判','爆款驱动','BS','基于历史季节性规律预测下一周期爆款','C',ARRAY['all'],'active'),
('BS-07','直播爆款','爆款驱动','BS','直播期间销量激增的商品','A',ARRAY['tiktok'],'active'),
('BS-08','短视频爆款','爆款驱动','BS','短视频带货销量突出的商品','A',ARRAY['tiktok'],'active'),
('BL-01','低竞争高需求','蓝海挖掘','BL','搜索量大但商品数少的类目/关键词','A',ARRAY['tiktok','shopee','amazon'],'active'),
('BL-02','空白类目发现','蓝海挖掘','BL','平台类目树中存在但未充分开发的节点','A',ARRAY['shopee','temu','amazon'],'active'),
('BL-03','跨站蓝海迁移','蓝海挖掘','BL','A平台热销但B平台尚未大量出现的商品','A',ARRAY['tiktok','shopee','temu','amazon'],'active'),
('BL-04','长尾关键词选品','蓝海挖掘','BL','针对长尾搜索词找对应商品','A',ARRAY['tiktok','shopee','amazon'],'active'),
('BL-05','小众人群定制','蓝海挖掘','BL','面向特定人群/场景的细分商品','D',ARRAY['all'],'active'),
('BL-06','地域差异化','蓝海挖掘','BL','某国别热销但其他国别未覆盖','A',ARRAY['shopee','tiktok'],'active'),
('BL-07','价格带空白','蓝海挖掘','BL','某价格区间商品少但需求存在','A',ARRAY['tiktok','shopee','amazon'],'active'),
('BL-08','评论空白机会','蓝海挖掘','BL','高需求但现有商品评论数低的品类','A',ARRAY['amazon','shopee','tiktok'],'active'),
('PF-01','毛利率筛选','利润导向','PF','售价-成本≥目标毛利率','C',ARRAY['all'],'active'),
('PF-02','运费占比控制','利润导向','PF','运费占售价比例≤阈值','B',ARRAY['shopee','tiktok','temu'],'active'),
('PF-03','平台佣金优化','利润导向','PF','选择佣金率低的类目/站点','B',ARRAY['shopee','tiktok','temu'],'active'),
('PF-04','汇率波动对冲','利润导向','PF','优先结算货币稳定的站点','C',ARRAY['all'],'active'),
('PF-05','退货率控制','利润导向','PF','筛选退货率低的类目','A',ARRAY['amazon','shopee'],'active'),
('PF-06','体积重优化','利润导向','PF','轻小件优先，降低物流成本','A',ARRAY['all'],'active'),
('PF-07','关税规避选品','利润导向','PF','避开高关税品类/材质','C',ARRAY['all'],'active'),
('PF-08','批量采购折扣','利润导向','PF','1688/供应链批量价利润测算','C',ARRAY['all'],'active'),
('CP-01','卖家集中度','竞争分析','CP','头部卖家占比过高的类目回避','A',ARRAY['tiktok','shopee','amazon'],'active'),
('CP-02','价格战规避','竞争分析','CP','同商品最低价过低、利润空间不足','A',ARRAY['all'],'active'),
('CP-03','品牌壁垒检测','竞争分析','CP','识别品牌垄断类目','A',ARRAY['amazon','shopee'],'active'),
('CP-04','新进入者友好度','竞争分析','CP','近期新店上架速度快的类目','A',ARRAY['tiktok','shopee'],'active'),
('CP-05','差评机会分析','竞争分析','CP','竞品差评中暴露的改进点','A',ARRAY['amazon','shopee','tiktok'],'active'),
('CP-06','listing质量差距','竞争分析','CP','现有商品主图/标题/描述质量低','A',ARRAY['all'],'active'),
('CP-07','广告竞争度','竞争分析','CP','竞价广告少的类目竞争较低','B',ARRAY['amazon','shopee','tiktok'],'active'),
('CP-08','跟卖风险预警','竞争分析','CP','识别易被跟卖的标准化商品','A',ARRAY['amazon','temu'],'active'),
('TR-01','社交媒体热点','趋势洞察','TR','TikTok/Instagram热点话题关联商品','A',ARRAY['tiktok','instagram'],'active'),
('TR-02','搜索趋势上升','趋势洞察','TR','平台内搜索量持续上升的关键词','A',ARRAY['tiktok','shopee','amazon'],'active'),
('TR-03','节日/事件营销','趋势洞察','TR','基于节假日、大型活动提前选品','D',ARRAY['all'],'active'),
('TR-04','KOL带货风向','趋势洞察','TR','头部KOL近期推荐的商品类型','A',ARRAY['tiktok'],'active'),
('TR-05','众筹/预售热度','趋势洞察','TR','Kickstarter/Indiegogo等众筹平台热门品类','C',ARRAY['all'],'active'),
('TR-06','谷歌趋势验证','趋势洞察','TR','Google Trends验证商品需求趋势','A',ARRAY['all'],'active'),
('TR-07','行业新闻追踪','趋势洞察','TR','电商行业新闻/政策变化带来的机会','D',ARRAY['all'],'active'),
('TR-08','竞品上新监控','趋势洞察','TR','监控竞品店铺新品上架动态','A',ARRAY['tiktok','shopee','amazon'],'active'),
('RC-01','禁限售规避','合规与风控','RC','避开各平台禁限售类目/商品','A',ARRAY['all'],'active'),
('RC-02','知识产权风险','合规与风控','RC','检测商标、专利、版权风险','C',ARRAY['amazon','shopee'],'active'),
('RC-03','认证要求检查','合规与风控','RC','目标国别强制认证要求','B',ARRAY['all'],'active'),
('RC-04','税务合规','合规与风控','RC','VAT/GST/销售税影响定价','C',ARRAY['all'],'active'),
('RC-05','物流限制规避','合规与风控','RC','避开液体、粉末、电池等敏感物流商品','A',ARRAY['all'],'active'),
('RC-06','平台政策变动监控','合规与风控','RC','监控平台规则变化对现有商品的影响','B',ARRAY['all'],'active'),
('RC-07','退货政策匹配','合规与风控','RC','不同国家别退货政策差异','B',ARRAY['all'],'active'),
('RC-08','环保合规','合规与风控','RC','EU/美国环保法规（包装法、EPR等）','C',ARRAY['eu'],'active'),
('RP-01','复购率选品','复购类','RP','筛选历史复购率高的商品/类目','B',ARRAY['shopee','tiktok'],'active'),
('RP-02','周期消耗品选品','复购类','RP','识别周期性补货商品','A',ARRAY['all'],'active'),
('RP-03','老客回购潜力款','复购类','RP','面向已有粉丝/老客的二次转化商品','B',ARRAY['tiktok','shopee'],'active'),
('RP-04','低流失商品筛选','复购类','RP','筛选退货率低、差评少、复购稳定的商品','A',ARRAY['amazon','shopee','tiktok'],'active'),
('RP-05','稳定日销款','复购类','RP','非爆款但长期稳定出单的商品','A',ARRAY['tiktok','shopee','amazon'],'active'),
('RP-06','季节循环爆款','复购类','RP','每年固定周期反复爆发的商品','C',ARRAY['all'],'active'),
('RP-07','订阅制/定期购商品','复购类','RP','适合设置自动补货提醒的消耗品类目','D',ARRAY['all'],'active'),
('RP-08','高LTV商品识别','复购类','RP','客户终身价值高的商品','B',ARRAY['all'],'active'),
('LC-01','新品期机会','生命周期类','LC','上架30天内快速起量的商品','A',ARRAY['tiktok','shopee'],'active'),
('LC-02','成长期加速','生命周期类','LC','搜索量/销量持续上升但未饱和的类目','A',ARRAY['tiktok','shopee','amazon'],'active'),
('LC-03','成熟期利润优化','生命周期类','LC','市场已成熟但仍有利润空间的细分差异化商品','A',ARRAY['all'],'active'),
('LC-04','衰退期预警','生命周期类','LC','识别销量下滑、评论负向增加、竞品减少的品类','A',ARRAY['all'],'active'),
('LC-05','品类生命周期研判','生命周期类','LC','判断某类目整体处于导入/成长/成熟/衰退哪一阶段','A',ARRAY['all'],'active'),
('LC-06','爆款生命周期管理','生命周期类','LC','监控已选爆款的生命周期阶段','A',ARRAY['all'],'active'),
('LC-07','跨生命周期迁移','生命周期类','LC','在某平台已进入成熟期的商品，迁移到另一平台仍处于新品/成长期','A',ARRAY['tiktok','shopee','temu','amazon'],'active'),
('LC-08','反周期选品','生命周期类','LC','在品类衰退期反向进入','A',ARRAY['all'],'active');
```

#### 8.2.2 strategy_parameters — 用户自定义参数实例表

```sql
CREATE TABLE strategy_parameters (
    id BIGSERIAL PRIMARY KEY,
    strategy_id VARCHAR(10) NOT NULL REFERENCES base_strategies(strategy_id),
    job_id UUID,                                  -- 选品任务ID，NULL表示全局默认参数
    param_key VARCHAR(100) NOT NULL,              -- 参数键名
    param_value JSONB NOT NULL,                   -- 参数值（支持任意JSON）
    is_default BOOLEAN DEFAULT false,             -- 是否为默认参数
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (strategy_id, job_id, param_key)
);

CREATE INDEX idx_strategy_params_job ON strategy_parameters(job_id);
```

#### 8.2.3 composite_strategies — 复合策略表（自引用嵌套）

```sql
CREATE TABLE composite_strategies (
    composite_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    parent_composite_id UUID REFERENCES composite_strategies(composite_id),  -- 自引用，支持无限嵌套
    operator VARCHAR(20) NOT NULL CHECK (operator IN ('intersection','union','difference','weighted')),
    strategy_tree JSONB NOT NULL,                  -- 完整策略树JSON
    weight_config JSONB DEFAULT '{}',              -- 六维权重配置
    negative_filter_snapshot JSONB DEFAULT '[]',   -- 负向筛选快照
    version INTEGER DEFAULT 1,
    is_current_version BOOLEAN DEFAULT true,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','archived','deprecated')),
    saved_as_new BOOLEAN DEFAULT false,            -- 是否由运算结果另存为新策略
    trigger_type VARCHAR(20) DEFAULT 'manual',     -- manual/auto/scheduled/ai_generated
    created_by UUID,                              -- 创建用户ID
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_composite_parent ON composite_strategies(parent_composite_id);
CREATE INDEX idx_composite_operator ON composite_strategies(operator);
CREATE INDEX idx_composite_status ON composite_strategies(status);
CREATE INDEX idx_composite_tree ON composite_strategies USING GIN(strategy_tree);
```

#### 8.2.4 composite_links — 复合策略子节点关联表

```sql
CREATE TABLE composite_links (
    id BIGSERIAL PRIMARY KEY,
    composite_id UUID NOT NULL REFERENCES composite_strategies(composite_id) ON DELETE CASCADE,
    child_type VARCHAR(10) NOT NULL CHECK (child_type IN ('base','composite')),
    ref_id VARCHAR(10) NOT NULL,                   -- base策略ID或子复合策略ID
    link_operator VARCHAR(20) DEFAULT 'intersection',
    weight DECIMAL(3,2) DEFAULT 1.0 CHECK (weight >= 0 AND weight <= 1),
    sort_order INTEGER DEFAULT 0,
    extra_config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (composite_id, ref_id, sort_order)
);

CREATE INDEX idx_composite_links_composite ON composite_links(composite_id);
```

#### 8.2.5 data_sources — 数据源注册表

```sql
CREATE TABLE data_sources (
    source_id VARCHAR(50) PRIMARY KEY,
    source_name VARCHAR(200) NOT NULL,
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('crawler','api','import','manual','none')),
    platforms TEXT[],                              -- 适配平台
    url_pattern TEXT,                              -- 爬虫URL模板
    api_endpoint TEXT,                             -- API端点
    auth_config JSONB,                             -- 认证配置（加密存储）
    refresh_frequency VARCHAR(20) DEFAULT 'daily', -- 刷新频率
    field_mapping JSONB DEFAULT '{}',              -- 原始字段→标准字段映射
    health_status VARCHAR(20) DEFAULT 'healthy' CHECK (health_status IN ('healthy','degraded','down','unknown')),
    rate_limit INTEGER,                            -- 调用限额
    last_success_at TIMESTAMPTZ,
    last_error_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_data_sources_type ON data_sources(source_type);
CREATE INDEX idx_data_sources_health ON data_sources(health_status);
CREATE INDEX idx_data_sources_platforms ON data_sources USING GIN(platforms);
```

#### 8.2.6 strategy_data_source_mapping — 策略-数据源映射表

```sql
CREATE TABLE strategy_data_source_mapping (
    id BIGSERIAL PRIMARY KEY,
    strategy_id VARCHAR(10) NOT NULL REFERENCES base_strategies(strategy_id),
    data_source_id VARCHAR(50) REFERENCES data_sources(source_id),  -- D级策略可为NULL
    priority INTEGER DEFAULT 0,
    field_mappings JSONB DEFAULT '{}',             -- 策略参数→数据源字段映射
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','paused','deprecated')),
    valid_from DATE,
    valid_to DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (strategy_id, data_source_id, status)
);

CREATE INDEX idx_mapping_strategy ON strategy_data_source_mapping(strategy_id);
CREATE INDEX idx_mapping_datasource ON strategy_data_source_mapping(data_source_id);
```

#### 8.2.7 selection_jobs — 选品任务表

```sql
CREATE TABLE selection_jobs (
    job_uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    composite_strategy_id UUID NOT NULL REFERENCES composite_strategies(composite_id),
    strategy_snapshot JSONB NOT NULL,              -- 执行时的策略快照（防历史修改影响）
    user_config JSONB DEFAULT '{}',                -- 用户参数配置覆盖
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','running','completed','failed','cancelled')),
    duration_ms INTEGER,
    total_matched INTEGER DEFAULT 0,
    data_missing_count INTEGER DEFAULT 0,
    trigger_type VARCHAR(20) DEFAULT 'manual' CHECK (trigger_type IN ('manual','auto','scheduled','ai_generated')),
    execution_trace JSONB DEFAULT '[]',            -- 每层运算追踪
    result_summary JSONB DEFAULT '{}',             -- 结果摘要（预估命中数等）
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_selection_jobs_status ON selection_jobs(status);
CREATE INDEX idx_selection_jobs_strategy ON selection_jobs(composite_strategy_id);
CREATE INDEX idx_selection_jobs_created ON selection_jobs(created_at DESC);
CREATE INDEX idx_selection_jobs_trigger ON selection_jobs(trigger_type);
```

#### 8.2.8 candidate_products — 候选商品快照表

```sql
CREATE TABLE candidate_products (
    id BIGSERIAL PRIMARY KEY,
    job_uuid UUID NOT NULL REFERENCES selection_jobs(job_uuid) ON DELETE CASCADE,
    platform VARCHAR(20) NOT NULL,
    country_code VARCHAR(5),
    product_id VARCHAR(50),
    title TEXT,
    image_url TEXT,
    category_l1 VARCHAR(100),
    category_l2 VARCHAR(100),
    category_l3 VARCHAR(100),
    price_min DECIMAL(12,2),
    price_max DECIMAL(12,2),
    sales_l7 INTEGER DEFAULT 0,
    sales_l30d INTEGER DEFAULT 0,
    rating DECIMAL(3,2),
    review_count INTEGER DEFAULT 0,
    search_volume INTEGER DEFAULT 0,
    competitor_count INTEGER DEFAULT 0,
    strategy_scores JSONB DEFAULT '{}',            -- 各策略得分
    composite_score DECIMAL(5,2),                  -- 综合得分
    lifecycle_stage VARCHAR(20),                   -- 新品期/成长期/成熟期/衰退期
    risk_level VARCHAR(10) DEFAULT 'low',          -- low/medium/high
    confidence VARCHAR(10) DEFAULT 'medium',       -- low/medium/high
    excluded_by_negative_filter BOOLEAN DEFAULT false,
    excluded_reason VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_candidate_job ON candidate_products(job_uuid);
CREATE INDEX idx_candidate_platform ON candidate_products(platform);
CREATE INDEX idx_candidate_score ON candidate_products(composite_score DESC);
CREATE INDEX idx_candidate_lifecycle ON candidate_products(lifecycle_stage);
-- 分区表预留：按月份分区
-- PARTITION BY RANGE (created_at)

-- v2增强字段（ALTER TABLE）
-- ALTER TABLE candidate_products ADD COLUMN benchmark_type VARCHAR(20);
-- ALTER TABLE candidate_products ADD COLUMN benchmark_score DECIMAL(5,2);
-- ALTER TABLE candidate_products ADD COLUMN recommendation_note TEXT;
-- ALTER TABLE candidate_products ADD COLUMN suggested_price_range JSONB;
```

#### 8.2.9 benchmark_products — 标杆商品样例表

```sql
CREATE TABLE benchmark_products (
    id BIGSERIAL PRIMARY KEY,
    job_uuid UUID REFERENCES selection_jobs(job_uuid),
    platform VARCHAR(20),
    product_id VARCHAR(50),
    title TEXT,
    image_url TEXT,
    category_path TEXT,
    benchmark_type VARCHAR(20),                    -- best_sales/best_margin/best_trend/best_blue_ocean
    benchmark_score DECIMAL(5,2),
    recommendation_note TEXT,
    suggested_price_range JSONB,
    linked_media_library_id BIGINT,                -- 关联素材图库
    linked_draft_product_id BIGINT,                -- 关联商品草稿
    linked_listing_task_id BIGINT,                 -- 关联上架任务
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_benchmark_job ON benchmark_products(job_uuid);
CREATE INDEX idx_benchmark_type ON benchmark_products(benchmark_type);
```

#### 8.2.10 data_collection_logs — 数据采集日志表

```sql
CREATE TABLE data_collection_logs (
    id BIGSERIAL PRIMARY KEY,
    data_source_id VARCHAR(50) REFERENCES data_sources(source_id),
    strategy_id VARCHAR(10) REFERENCES base_strategies(strategy_id),
    job_uuid UUID REFERENCES selection_jobs(job_uuid),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','running','success','partial','failed')),
    items_found INTEGER DEFAULT 0,
    items_parsed INTEGER DEFAULT 0,
    items_validated INTEGER DEFAULT 0,
    duration_ms INTEGER,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    raw_response JSONB,
    collected_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_log_source ON data_collection_logs(data_source_id);
CREATE INDEX idx_log_job ON data_collection_logs(job_uuid);
CREATE INDEX idx_log_status ON data_collection_logs(status);
CREATE INDEX idx_log_collected ON data_collection_logs(collected_at DESC);
```

#### 8.2.11 strategy_weights — 策略权重配置表（v2新增）

```sql
CREATE TABLE strategy_weights (
    id BIGSERIAL PRIMARY KEY,
    composite_strategy_id UUID REFERENCES composite_strategies(composite_id),
    user_id UUID,
    weight_type VARCHAR(20) DEFAULT 'preset' CHECK (weight_type IN ('preset','custom','ai_generated')),
    template_name VARCHAR(50),                     -- 爆款优先/利润优先/蓝海优先/稳健经营/合规优先/自定义
    w_sales DECIMAL(3,2) DEFAULT 0.25,
    w_profit DECIMAL(3,2) DEFAULT 0.25,
    w_competition DECIMAL(3,2) DEFAULT 0.20,
    w_trend DECIMAL(3,2) DEFAULT 0.15,
    w_repurchase DECIMAL(3,2) DEFAULT 0.10,
    w_compliance DECIMAL(3,2) DEFAULT 0.05,
    weight_config JSONB DEFAULT '{}',              -- 扩展权重配置
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 预设种子数据
INSERT INTO strategy_weights (template_name, w_sales, w_profit, w_competition, w_trend, w_repurchase, w_compliance, weight_type) VALUES
('爆款优先', 0.40, 0.10, 0.15, 0.20, 0.10, 0.05, 'preset'),
('利润优先', 0.15, 0.40, 0.10, 0.10, 0.15, 0.10, 'preset'),
('蓝海优先', 0.15, 0.15, 0.40, 0.15, 0.10, 0.05, 'preset'),
('稳健经营', 0.20, 0.20, 0.15, 0.10, 0.25, 0.10, 'preset'),
('合规优先', 0.15, 0.15, 0.10, 0.10, 0.10, 0.40, 'preset');

CREATE INDEX idx_weights_user ON strategy_weights(user_id);
CREATE INDEX idx_weights_strategy ON strategy_weights(composite_strategy_id);
```

#### 8.2.12 negative_filters — 负向筛选规则定义表（v2新增）

```sql
CREATE TABLE negative_filters (
    filter_id VARCHAR(10) PRIMARY KEY,             -- NF-01 ~ NF-08
    filter_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    data_source_ref VARCHAR(50),                   -- 关联数据源
    data_feasibility CHAR(1) CHECK (data_feasibility IN ('A','B','C','D')),
    precise_channel_source VARCHAR(50),            -- 精准渠道来源
    access_difficulty VARCHAR(20),                 -- 获取难易度
    update_frequency VARCHAR(20),                  -- 更新频率
    data_cost VARCHAR(20),                         -- 数据成本
    implementation_feasibility VARCHAR(30),        -- 落地可行性
    config_schema JSONB DEFAULT '{}',              -- 规则配置Schema
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8条预置负向规则
INSERT INTO negative_filters (filter_id, filter_name, description, data_feasibility, precise_channel_source, access_difficulty, update_frequency, data_cost, implementation_feasibility) VALUES
('NF-01','排除高退货率','自动排除退货率超过阈值的类目/商品','A','公域评论+卖家后台退货率','中等','月更','免费','短期可落地'),
('NF-02','排除低利润','排除扣除所有成本后利润率低于阈值的商品','C','成本表+售价+运费+佣金','中等','静态人工','免费','短期可落地'),
('NF-03','排除高竞争','排除头部卖家集中度超过阈值的类目','A','公域商品列表+卖家分析','中等','周更','免费','短期可落地'),
('NF-04','排除违规风险','排除触碰禁限售/知识产权红线的商品','A','平台规则+品牌数据库','简单','月更','免费','短期可落地'),
('NF-05','排除价格战','排除最低价已无利润空间的标准化商品','A','公域比价','中等','日更','免费','短期可落地'),
('NF-06','排除衰退品','排除处于生命周期衰退期的商品','A','销量趋势+NLP评论分析','困难','周更','免费(需NLP)','中期可落地'),
('NF-07','排除低评分','排除评分低于阈值的商品','A','公域评论星级','简单','日更','免费','短期可落地'),
('NF-08','排除同质化','排除搜索结果高度雷同的商品','A','标题相似度+图片相似度','困难','周更','免费(需算力)','中期可落地');
```

#### 8.2.13 negative_filter_applications — 负向规则应用记录表（v2新增）

```sql
CREATE TABLE negative_filter_applications (
    id BIGSERIAL PRIMARY KEY,
    job_uuid UUID NOT NULL REFERENCES selection_jobs(job_uuid),
    filter_id VARCHAR(10) NOT NULL REFERENCES negative_filters(filter_id),
    products_before INTEGER DEFAULT 0,
    products_after INTEGER DEFAULT 0,
    excluded INTEGER DEFAULT 0,
    exclusion_rate DECIMAL(5,2),                   -- 排除率%
    excluded_products JSONB,                       -- 被排除商品明细
    applied_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_nf_app_job ON negative_filter_applications(job_uuid);
CREATE INDEX idx_nf_app_filter ON negative_filter_applications(filter_id);
```

#### 8.2.14 strategy_win_rates — 策略胜率统计表（v2新增）

```sql
CREATE TABLE strategy_win_rates (
    id BIGSERIAL PRIMARY KEY,
    composite_strategy_id UUID REFERENCES composite_strategies(composite_id),
    base_strategy_ids TEXT[],                      -- 涉及的原生策略ID列表
    period_start DATE,
    period_end DATE,
    execution_count INTEGER DEFAULT 0,
    hit_rate DECIMAL(5,2),                         -- 命中率%
    avg_first_month_sales DECIMAL(10,2),
    avg_gross_margin DECIMAL(5,2),
    strategy_roi DECIMAL(10,2),
    repurchase_30d DECIMAL(5,2),
    repurchase_60d DECIMAL(5,2),
    repurchase_90d DECIMAL(5,2),
    lifecycle_score DECIMAL(5,2),
    volatility DECIMAL(5,2),                       -- 波动率
    best_case JSONB,                               -- {"candidates":45,"sold":32}
    worst_case JSONB,
    trend VARCHAR(10),                             -- up/down/stable
    positive_factors TEXT[],
    negative_factors TEXT[],
    optimization_suggestions TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_wins_strategy ON strategy_win_rates(composite_strategy_id);
CREATE INDEX idx_wins_period ON strategy_win_rates(period_start, period_end);
```

#### 8.2.15 strategy_derivations — 策略衍生记录表（v2新增）

```sql
CREATE TABLE strategy_derivations (
    id BIGSERIAL PRIMARY KEY,
    source_strategy_id UUID REFERENCES composite_strategies(composite_id),
    derived_strategy_id UUID REFERENCES composite_strategies(composite_id),
    derivation_type VARCHAR(30) NOT NULL CHECK (derivation_type IN (
        'parameter_tweak','platform_migration','category_limit','country_limit',
        'period_scale','combination_stack','negative_enhance','ai_generated'
    )),
    derivation_config JSONB,
    notes TEXT,
    created_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_derivation_source ON strategy_derivations(source_strategy_id);
CREATE INDEX idx_derivation_type ON strategy_derivations(derivation_type);
```

#### 8.2.16 data_source_attributes — 数据源五维属性表（v2新增）

```sql
CREATE TABLE data_source_attributes (
    source_id VARCHAR(50) PRIMARY KEY REFERENCES data_sources(source_id),
    precise_channel_source VARCHAR(50) NOT NULL,   -- 精准渠道来源
    access_difficulty VARCHAR(20) NOT NULL,        -- 获取难易度
    update_frequency VARCHAR(20) NOT NULL,         -- 更新频率
    data_cost VARCHAR(20) NOT NULL,                -- 数据成本
    implementation_feasibility VARCHAR(30) NOT NULL, -- 落地可行性
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 8.3 v2 ALTER TABLE增强（在v1基础表上追加）

```sql
-- 选品引擎相关表增强
ALTER TABLE products ADD COLUMN IF NOT EXISTS platform_extension JSONB;
ALTER TABLE products ADD COLUMN IF NOT EXISTS country_config_id UUID;
ALTER TABLE sku_table ADD COLUMN IF NOT EXISTS dimensions JSONB;
ALTER TABLE sku_table ADD COLUMN IF NOT EXISTS weight_g INTEGER;
ALTER TABLE sku_table ADD COLUMN IF NOT EXISTS seller_sku_code VARCHAR(100);
ALTER TABLE sku_table ADD COLUMN IF NOT EXISTS sku_images JSONB;

-- 候选商品v2增强
ALTER TABLE candidate_products ADD COLUMN IF NOT EXISTS benchmark_type VARCHAR(20);
ALTER TABLE candidate_products ADD COLUMN IF NOT EXISTS benchmark_score DECIMAL(5,2);
ALTER TABLE candidate_products ADD COLUMN IF NOT EXISTS recommendation_note TEXT;
ALTER TABLE candidate_products ADD COLUMN IF NOT EXISTS suggested_price_range JSONB;

-- 选品任务v2增强
ALTER TABLE selection_jobs ADD COLUMN IF NOT EXISTS user_config JSONB DEFAULT '{}';
ALTER TABLE selection_jobs ADD COLUMN IF NOT EXISTS execution_trace JSONB DEFAULT '[]';
ALTER TABLE selection_jobs ADD COLUMN IF NOT EXISTS result_summary JSONB DEFAULT '{}';
```

### 8.4 PostgreSQL触发器与自动维护

#### 8.4.1 选品任务完成后自动更新胜率统计

```sql
CREATE OR REPLACE FUNCTION update_strategy_win_rate_after_job()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' THEN
        UPDATE strategy_win_rates
        SET
            execution_count = execution_count + 1,
            hit_rate = COALESCE(
                (SELECT AVG(CASE WHEN cp.sales_l7 > 0 THEN 100.0 ELSE 0 END) FROM candidate_products cp WHERE cp.job_uuid = NEW.job_uuid),
                0
            ),
            avg_first_month_sales = COALESCE(
                (SELECT AVG(cp.sales_l30d) FROM candidate_products cp WHERE cp.job_uuid = NEW.job_uuid),
                0
            ),
            updated_at = NOW()
        WHERE composite_strategy_id = NEW.composite_strategy_id
        AND period_end = CURRENT_DATE;

        -- 若无当日记录则插入
        IF NOT FOUND THEN
            INSERT INTO strategy_win_rates (composite_strategy_id, period_start, period_end, execution_count, hit_rate, avg_first_month_sales)
            VALUES (NEW.composite_strategy_id, CURRENT_DATE, CURRENT_DATE, 1,
                    COALESCE((SELECT AVG(CASE WHEN cp.sales_l7 > 0 THEN 100.0 ELSE 0 END) FROM candidate_products cp WHERE cp.job_uuid = NEW.job_uuid), 0),
                    COALESCE((SELECT AVG(cp.sales_l30d) FROM candidate_products cp WHERE cp.job_uuid = NEW.job_uuid), 0));
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_win_rate
AFTER UPDATE OF status ON selection_jobs
FOR EACH ROW
WHEN (NEW.status = 'completed')
EXECUTE FUNCTION update_strategy_win_rate_after_job();
```

#### 8.4.2 维护脚本：定期清理过期数据

```sql
-- 清理90天前的选品任务
DELETE FROM selection_jobs WHERE created_at < NOW() - INTERVAL '90 days' AND deleted_at IS NULL;

-- 清理180天前的胜率统计（保留月度聚合）
DELETE FROM strategy_win_rates WHERE period_end < CURRENT_DATE - INTERVAL '180 days';

-- 清理365天前的衍生记录
DELETE FROM strategy_derivations WHERE created_at < NOW() - INTERVAL '365 days';

-- 清理30天前的采集日志
DELETE FROM data_collection_logs WHERE collected_at < NOW() - INTERVAL '30 days';

-- 清理已过期且未激活的数据源映射
UPDATE strategy_data_source_mapping SET status = 'deprecated'
WHERE valid_to < CURRENT_DATE AND status = 'active';

-- 清理已标记删除的软删除记录（每周执行一次）
DELETE FROM selection_jobs WHERE deleted_at < NOW() - INTERVAL '7 days';
DELETE FROM candidate_products WHERE job_uuid IN (SELECT job_uuid FROM selection_jobs WHERE deleted_at < NOW() - INTERVAL '7 days');
```

### 8.5 ER关系图

```
base_strategies (1) -- (N) strategy_parameters
       |
       | data_source_ref
       v
data_sources (1) -- (N) strategy_data_source_mapping -- (N) base_strategies
       |
       v
data_collection_logs

composite_strategies (1) -- (N) composite_links
       |
       | composite_strategy_id
       v
selection_jobs (1) -- (N) candidate_products -- (1) benchmark_products
       |
       | weight_config / negative_filter_snapshot
       v
strategy_weights / negative_filter_applications

strategy_win_rates -- composite_strategies / base_strategies
strategy_derivations -- composite_strategies / base_strategies
data_source_attributes -- data_sources
negative_filters (1) -- (N) negative_filter_applications
```

### 8.6 关键设计特点

- **JSONB灵活存储**：strategy_tree、strategy_scores、weight_config、preview_result等全部使用JSONB，适配动态策略结构
- **软删除**：base_strategies/composite_strategies/data_sources均含deleted_at
- **版本管理**：composite_strategies支持version + is_current_version，selection_jobs保存strategy_snapshot防止历史修改影响
- **唯一性约束**：strategy_data_source_mapping(strategy_id, data_source_id, status)、strategy_parameters(strategy_id, job_id, param_key)
- **分区表预留**：candidate_products可按月份分区
- **PostgreSQL触发器**：selection_jobs完成后自动更新strategy_win_rates
- **维护脚本**：清理90天任务/180天胜率/365天衍生记录/过期preview_result

### 8.7 统一字段标准字典（完整版，110+字段）

#### 8.7.1 标准字段（核心通用字段）

| 字段英文名 | 中文名 | 类型 | Shopee | TikTok Shop | TEMU | 妙手ERP | 说明 |
|-----------|--------|------|--------|-------------|------|---------|------|
| product_id | 商品ID | string | product_id | item_id | spu_id | product_id | 商品唯一标识 |
| product_title | 商品标题 | string | item_name | item_name | product_name | title | 最多180字符 |
| product_description | 商品描述 | text | item_desc | item_desc | description | description | 最多5000字符 |
| product_images | 商品图片 | array | images | images | images | main_images | 最多9张主图 |
| product_video | 商品视频 | string | video_url | video_url | video_url | video_url | Max 30MB 10-60s MP4 |
| category_l1 | 一级类目 | string | l1_cat | l1_cat | l1_cat | category_l1 | 时尚配饰/包袋/鞋履等 |
| category_l2 | 二级类目 | string | l2_cat | l2_cat | l2_cat | category_l2 | 手提包/双肩包/斜挎包等 |
| category_l3 | 三级类目 | string | l3_cat | l3_cat | l3_cat | category_l3 | 通勤手提包/购物袋/水桶包等 |
| brand | 品牌 | string | brand | brand | brand | brand | 品牌名 |
| listing_status | 上架状态 | enum | status | status | listing_status | publish_status | 架上商品/违规删除/审查中/未上架等 |
| shop_id | 店铺ID | string | shop_id | shop_id | shop_id | shop_id | 授权店铺ID |
| platform_code | 平台代码 | string | shopee | tiktok | temu | miaoshou | 平台标识 |
| country_code | 国家代码 | string | country | country | country | country | PH/SG/MY/TH/VN/ID/TW等 |
| currency_code | 货币代码 | string | currency | currency | currency | currency | PHP/SGD/MYR/THB/VND/IDR/TWD等 |
| currency_symbol | 货币符号 | string | symbol | symbol | symbol | symbol | ₱/S$/RM/฿/₫/Rp/NT$等 |
| price_min | 最低价格 | decimal | min_price | min_price | supply_price | price_min | 站点本地币 |
| price_max | 最高价格 | decimal | max_price | max_price | retail_price | price_max | 站点本地币 |
| stock_qty | 库存数量 | integer | stock | stock | warehouse_stock | stock_qty | 总库存数 |
| l30d_sales | 近30天销量 | integer | l30d_sales | l30d_sales | l30d_sales | l30d_sales | L30D Sales |
| l30d_impression | 近30天曝光量 | integer | l30d_impression | l30d_impression | l30d_impression | l30d_impression | L30D Impression |
| click_through_rate | 点击率 | decimal | ctr | ctr | ctr | ctr | CTR |
| conversion_rate | 转化率 | decimal | cvr | cvr | cvr | cvr | 转化率 |
| rating | 评分 | decimal | rating | rating | rating | rating | 1-5分 |
| review_count | 评论数 | integer | review_count | review_count | review_count | review_count | 评论总数 |
| created_at | 创建时间 | datetime | created_at | created_at | created_at | created_at | 商品创建日期 |
| updated_at | 更新时间 | datetime | updated_at | updated_at | updated_at | updated_at | 最近更新 |
| deleted_at | 软删除时间 | datetime | deleted_at | deleted_at | deleted_at | deleted_at | NULL表示未删除 |

#### 8.7.2 SKU相关字段

| 字段英文名 | 中文名 | 类型 | Shopee | TikTok Shop | TEMU | 妙手ERP | 说明 |
|-----------|--------|------|--------|-------------|------|---------|------|
| sku_id | SKU ID | string | model_id | sku_id | sku_id | sku_id | 平台分配SKU ID |
| seller_sku_code | 商家货号 | string | seller_sku | seller_sku | seller_sku | seller_sku_code | 自定义货号 |
| sku_name | SKU名称 | string | variant | variant | variant | sku_name | Yellow/350ml |
| sku_price | SKU价格 | decimal | sku_price | sku_price | supply_price | sku_price | 站点本地币/CNY |
| sku_original_price | SKU原价 | decimal | original_price | original_price | retail_price | original_price | 划线价 |
| sku_stock | SKU库存 | integer | sku_stock | sku_stock | warehouse_stock | sku_stock | 库存数量 |
| sku_dimensions | SKU尺寸 | object | — | — | dimensions | — | Temu必填：长宽高cm |
| sku_weight | SKU重量 | decimal | — | — | weight_g | — | Temu必填：克 |
| sku_images | SKU级别图片 | array | sku_images | sku_images | sku_images | sku_images | 编辑弹窗新增字段 |
| variant_attr_1 | 规格一 | string | attr1 | attr1 | skc_color | attr1 | 颜色/尺寸等 |
| variant_attr_2 | 规格二 | string | attr2 | attr2 | skc_spec | attr2 | 第二规格 |

#### 8.7.3 订单相关字段

| 字段英文名 | 中文名 | 类型 | Shopee | TikTok Shop | TEMU | 说明 |
|-----------|--------|------|--------|-------------|------|------|
| order_id | 订单编号 | string | order_id | order_id | order_id | 唯一订单标识 |
| buyer_name | 买家名称 | string | buyer_name | buyer_name | buyer_name | 购买者账号 |
| order_items | 订单商品 | object | order_items | order_items | order_items | 商品标题/规格/数量/金额 |
| total_amount | 总金额 | decimal | total_amount | total_amount | total_amount | 多币种 |
| amount_cny | CNY金额 | decimal | amount_cny | amount_cny | amount_cny | 统一CNY存储 |
| payment_method | 支付方式 | string | payment_method | payment_method | — | 按国别 |
| order_status | 订单状态 | enum | order_status | order_status | fulfillment_status | 待付款/待出货/运送中/已完成/退货退款取消 |
| shipping_channel | 物流渠道 | string | shipping_method | shipping_method | logistics_channel | Express International等 |
| tracking_number | 运单号 | string | tracking_no | tracking_no | tracking_no | 物流追踪号 |
| dispatch_deadline | 发货时限 | datetime | parcel_ready_time | fulfill_by_time | ship_by_time | 发货截止时间 |
| cancel_reason | 取消原因 | string | cancel_reason | cancel_reason | — | 取消原因 |

#### 8.7.4 资金相关字段

| 字段英文名 | 中文名 | 类型 | Shopee | TikTok Shop | TEMU | 说明 |
|-----------|--------|------|--------|-------------|------|------|
| finance_record_id | 资金记录ID | string | transaction_id | transaction_id | settlement_id | 唯一标识 |
| settlement_date | 结算日期 | date | settlement_date | settlement_date | settlement_date | 结算日期 |
| commission | 平台佣金 | decimal | commission | commission | commission | 平台抽取佣金 |
| shipping_fee | 运费 | decimal | shipping_fee | shipping_fee | shipping_fee | 物流费用 |
| refund_amount | 退款金额 | decimal | refund_amount | refund_amount | refund_amount | 退款金额 |
| transaction_type | 交易类型 | enum | income/refund/commission/service_fee/deposit | — | — | 收入/退款/佣金/服务费/保证金 |

#### 8.7.5 平台特有字段

| 字段英文名 | 中文名 | 类型 | Shopee | TikTok Shop | TEMU | 妙手ERP | 说明 |
|-----------|--------|------|--------|-------------|------|---------|------|
| ssp_id | SSP编号 | string | ✅ | — | — | — | 标准商品编号，关联Hot Listing |
| hot_listing_status | Hot Listing状态 | string | ✅ | — | — | — | 热门商品推广状态 |
| smart_diagnosis | Smart Diagnosis | string | ✅ | — | — | — | 商品健康度诊断 |
| new_item_boost | 新品扶持 | boolean | ✅ | — | — | — | 新品90天流量扶持 |
| advance_fulfillment_stock | 预发货库存 | integer | ✅ | — | — | — | Advance Fulfillment Stock |
| account_security_password | 安全密码 | secret | ✅ | — | — | — | Shopee财务页面需额外密码验证 |
| sps_score | SPS评分 | decimal | — | ✅ | — | — | 卖家体验分 |
| crm_enabled | CRM功能解锁 | boolean | — | ✅ | — | — | 聊天营销（SPS≥3.5+GMV>0） |
| chat_plan_template | 聊天计划模板 | enum | — | ✅ | — | — | 一次性计划/自动计划 |
| chat_gmv | 聊天GMV | decimal | — | ✅ | — | — | 聊天GMV |
| spu_id | SPU ID | string | — | — | ✅ | — | 标准产品单元ID |
| skc_id | SKC ID | string | — | — | ✅ | — | 标准颜色单元ID |
| supply_price_cny | 供货价(CNY) | decimal | — | — | ✅ | — | 申报价格 |
| retail_price_suggested | 建议零售价 | decimal | — | — | ✅ | — | Temu建议零售价 |
| price_status | 价格状态 | enum | — | — | ✅ | — | 开款价格状态（已生效/待审核） |
| warehouse_group | 备货仓组 | string | — | — | ✅ | — | 平台指定仓库 |
| stocking_logic | 备货逻辑 | enum | — | — | ✅ | — | JIT/VMI |
| daily_posting_quota_used | 当日发品额度已用 | integer | — | — | ✅ | — | 如0/400 |
| qualification_status | 商品资质状态 | enum | — | — | ✅ | — | 待上传/上传失败 |
| live_photo_status | 商品实拍图状态 | enum | — | — | ✅ | — | 待上传/有异常 |
| compliance_info_status | 商品合规信息状态 | enum | — | — | ✅ | — | 待补充 |
| is_sensitive | 敏感属性 | boolean | — | — | ✅ | — | 是否敏感商品 |
| optimization_tips | 商品优化事项 | text | — | — | ✅ | — | 高价商品流量下降/建议零售价待填写/分类错误等 |
| inventory_available | 仓内可用库存 | integer | — | — | ✅ | — | Temu仓内可用 |
| inventory_reserved | 仓内预占用库存 | integer | — | — | ✅ | — | Temu仓内预占用 |
| inventory_blocked | 仓内暂不可用库存 | integer | — | — | ✅ | — | Temu仓内暂不可用 |
| inventory_physical | 仓内实物库存 | integer | — | — | ✅ | — | Temu仓内实物 |
| suggested_stock_days | 建议目标库存天数 | integer | — | — | ✅ | — | Temu建议备货天数 |
| suggested_reorder_qty | 建议备货量 | integer | — | — | ✅ | — | Temu建议备货数量 |
| days_of_supply | 库存可售天数 | integer | — | — | ✅ | — | Temu库存可售天数 |
| source_price | 货源价格 | decimal | — | — | — | ✅ | 采集来源商品价格 |
| main_article_no | 主货号 | string | — | — | — | ✅ | 商家自定义货号 |
| collect_source | 采集来源 | string | — | — | — | ✅ | 采集箱来源 |
| title_optimization | 标题优化状态 | enum | — | — | — | ✅ | 妙手ERP特有 |
| product_group | 商品分组 | string | — | — | — | ✅ | 妙手ERP特有 |
| shop_region | 店铺区域 | enum | — | ✅ | ✅ | — | Cross Border/本地店/全托管/半托管 |
| voucher_type | 优惠券类型 | enum | ✅ | — | — | — | 店铺券/商品券/直播券/短视频券/新买家券/回购买家券/关注礼券 |
| discount_activity_type | 折扣活动类型 | enum | ✅ | — | — | — | 套装优惠/我的折扣活动/分类折扣 |
| flash_sale_slot | 秒杀时段 | datetime | ✅ | — | — | — | Flash Sale时段 |
| commission_rate | 佣金比例 | decimal | — | ✅ | ✅ | — | 联盟营销佣金/平台服务费 |
| affiliate_commission | 联盟佣金 | decimal | ✅ | ✅ | — | — | 商品级佣金设置 |
| content_issues | 内容问题数 | integer | ✅ | — | — | — | 1 Content Issue To Fix + Optimise |
| return_refund_id | 退货申请编号 | string | ✅ | ✅ | ✅ | — | 售后单号 |
| return_package_id | 退货包裹单号 | string | ✅ | ✅ | ✅ | — | 退货包裹管理 |

#### 8.7.6 选品引擎相关字段

| 字段英文名 | 中文名 | 类型 | 说明 |
|-----------|--------|------|------|
| strategy_id | 策略ID | string | BS-01~LC-08 |
| strategy_name | 策略名称 | string | 策略显示名 |
| data_feasibility | 数据可行性等级 | char(1) | A/B/C/D |
| composite_strategy_id | 复合策略ID | uuid | 所属复合策略 |
| job_uuid | 选品任务UUID | uuid | 选品任务标识 |
| strategy_scores | 策略得分 | jsonb | 各策略得分详情 |
| composite_score | 综合得分 | decimal | 加权综合得分 |
| lifecycle_stage | 生命周期阶段 | string | 新品期/成长期/成熟期/衰退期 |
| risk_level | 风险等级 | string | low/medium/high |
| benchmark_type | 标杆类型 | string | best_sales/best_margin/best_trend/best_blue_ocean |
| benchmark_score | 标杆得分 | decimal | 标杆评价分数 |
| recommendation_note | 推荐说明 | text | AI推荐说明 |
| w_sales | 销量权重 | decimal | 0-1 |
| w_profit | 利润权重 | decimal | 0-1 |
| w_competition | 竞争度权重 | decimal | 0-1 |
| w_trend | 趋势权重 | decimal | 0-1 |
| w_repurchase | 复购权重 | decimal | 0-1 |
| w_compliance | 合规权重 | decimal | 0-1 |
| negative_filter_ids | 负向规则ID列表 | text[] | NF-01~NF-08 |
| excluded_by_negative_filter | 被负向规则排除 | boolean | 是否被排除 |
| excluded_reason | 排除原因 | string | 被哪个规则排除 |

---

## 九、开发落地顺序、重构优先级、迭代建议

### 9.1 总体开发阶段

| 阶段 | 内容 | 周期 | 交付物 |
|------|------|------|--------|
| **P0** | 64条原生策略入库 + D级策略配置 + 统一商品数据模型 | 2周 | 策略库CRUD、商品数据模型 |
| **P1** | 基础运算引擎（交集/并集/差集/加权） | 2周 | 选品引擎核心 |
| **P2** | A级数据源接入（TikTok/Shopee/Temu公域） | 3周 | 公域爬虫采集 |
| **P3** | 复合策略嵌套 + 保存复用 + 版本管理 | 2周 | 嵌套策略树 |
| **P4** | B级API数据源接入 | 3周 | 店铺授权同步 |
| **P5** | C级Excel导入 + D级预留激活 + 复购/生命周期策略 | 2周 | 人工导入工具 |
| **P6** | UI/UX完善（股票选股器范式） | 3周 | 现代化选品器UI |
| **P7** | 动态权重系统 + 预设模板 | 2周 | 权重滑块 |
| **P8** | 负向筛选规则 + 正负向组合运算 | 2周 | 负向筛选引擎 |
| **P9** | 策略胜率统计 + 回测数据追踪 | 3周 | 胜率看板 |
| **P10** | 策略一键衍生 + 相似策略推荐 | 2周 | 衍生引擎 |
| **P11** | AI辅助复合策略生成 | 3周 | NL→策略树 |
| **P12** | 策略市场与共享 | 2周 | 策略市场 |

**总计约33周（约8个月）**

> **旧路线替代说明**：本方案中 P0~P12 开发优先级完全替代 `02_功能开发方案总文档` 中早期的 v1 路线图。旧路线以"统一底座+各平台独立开发"为假设，未覆盖选品引擎、动态权重、负向筛选、策略胜率回溯等新模块。本次升级将旧路线整体替换为本方案的 P0~P12 阶段划分，确保所有开发任务统一在一个排期体系中执行。

### 9.2 重构优先级

| 优先级 | 模块 | 重构内容 | 周期 |
|--------|------|----------|------|
| **P0** | 统一商品数据模型 | Product主表+SKU子表+platform_extension+country_config | 2周 |
| **P0** | 平台适配器框架 | PlatformAdapter接口+四个平台适配器实现 | 2周 |
| **P1** | 动态表单引擎 | Schema驱动动态表单+平台适配器注入 | 2周 |
| **P1** | 弹窗式编辑 | 统一编辑弹窗+标签页/步骤导航 | 2周 |
| **P2** | 批量编辑功能 | 采集箱+批量发布/编辑/设置类目/设置售价 | 2周 |
| **P2** | 图片编辑器集成 | iframe嵌入易可图或自研基础版 | 2周 |
| **P3** | 订单状态机统一 | 各平台状态映射表+统一枚举 | 1周 |
| **P3** | 多币种定价引擎 | CNY存储+国别格式化+汇率更新 | 1周 |
| **P4** | 选品器基础模块 | 64策略入库+运算引擎+A级数据源 | 7周 |
| **P5** | 选品器高级功能 | 权重/负向筛选/胜率/衍生/AI | 14周 |

### 9.3 迭代建议

**第一期（8周）**：完成统一底座重构 + 基础选品器上线
- 商品数据模型+适配器框架+动态表单+弹窗编辑
- 64策略入库+基础运算引擎+A级数据源
- 让系统"能跑起来"

**第二期（8周）**：完善选品器高级功能 + 批量操作
- 复合策略嵌套+保存复用+B级API接入
- 动态权重+负向筛选+UI/UX完善
- 采集箱+批量编辑+图片编辑器

**第三期（8周）**：智能化 + 全链路打通
- 策略胜率+回测+衍生+AI生成
- 选品→素材库→商品编辑→定价→上架→订单→回款全链路打通
- 策略市场与共享

**第四期（9周）**：长期规划 + 预留功能激活
- D级策略数据源开发
- 平台官方API对接
- NLP/跨平台比对算力投入
- 实时汇率API/HS编码API

---

## 十、长期可扩展规划

### 10.1 选品策略持续迭代

- **策略库扩展**：新增策略类别（如供应链策略、仓储策略、客服策略）
- **算法优化**：引入机器学习预测销量/复购率/生命周期
- **策略市场**：用户自研策略发布/订阅/积分收益分成
- **A/B测试**：策略效果对比验证

### 10.2 数据源持续接入

| 数据源类型 | 当前状态 | 未来规划 |
|-----------|----------|----------|
| 公域爬虫 | A级部分可用 | 自动化定时采集、反爬对抗 |
| 平台官方API | B级部分可用 | 直连TikTok/Shopee/TEMU开放平台 |
| 第三方数据SaaS | C级人工导入 | 购买行业报告、竞品数据 |
| NLP分析 | D级预留 | 评论情感分析、差评关键词提取 |
| 实时汇率API | C级手动配置 | 接入实时汇率服务 |
| HS编码/关税API | C级手动导入 | 接入关税数据库 |

### 10.3 技术架构演进

- **微服务化**：选品引擎、数据采集、策略运算、AI生成拆分为独立服务
- **向量检索**：pgvector/Milvus用于策略相似度检索
- **实时计算**：Flink/Spark Streaming处理实时销量/趋势数据
- **多租户隔离**：tenant_id字段加入所有业务表
- **容器化部署**：Docker/Kubernetes部署选品引擎和数据采集服务

### 10.4 商业模式拓展

- **策略市场**：用户贡献策略获得积分/收益分成
- **数据服务**：提供行业报告、竞品分析、趋势预测等付费数据
- **API服务**：向第三方ERP/工具提供选品数据API
- **SaaS订阅**：高级功能（AI生成、胜率分析、策略市场）订阅制

---

## 附录：10份调研文档内容索引

| 文档 | 核心内容 | 在本方案中的位置 |
|------|----------|-----------------|
| 01_多平台电商后台调研汇总 | Shopee/TikTok/TEMU/妙手ERP后台调研（导航、商品、营销、订单、资金、国别差异、特殊规则、编辑页面深度对比） | 第一、三、四、七章 |
| 02_功能开发方案总文档 | 混合框架法架构、发布流程、弹窗式编辑、动态表单、SKU管理、国别方案 | 第二、三、四、七章 |
| 03_字段标准对照表 | 110+字段的标准/非标准分类、跨平台映射规则 | 第八章（字段标准字典） |
| 04_UIUX交互设计指导 | 全局设计规范（色彩/字体/间距）、商品管理页面布局/卡片/表格/筛选/批量/权限、编辑弹窗完整结构、活动配置页、订单资金页、响应式/i18n | 第七章（全部） |
| 05_开发建设指导意见 | 技术栈、数据库SQL、适配器TypeScript接口、动态表单Schema代码、多币种计算引擎、开发路线图 | 第二章、第八章、第九章 |
| 06_上次调研缺失功能补充对照表 | 功能缺口分析、图片编辑器补充、四平台编辑页对比 | 第六章（补齐模块） |
| 07_跨境选品_全量策略全集_数据可行性分级表 | 64条策略+ABCD分级+五维数据资产+复合策略运算规则+参数化配置示例 | 第五章、第八章 |
| 08_选品选股器核心架构_策略数据解耦方案 | 四层架构+v2智能引擎（动态权重/负向筛选/策略衍生/胜率/AI生成）+开发优先级P0-P12 | 第二、五、九章 |
| 09_选品器UIUX交互规范_股票选股器范式 | 选品器四栏动态布局、策略库/工作区/结果/智能面板交互、股票选股器对标映射 | 第七章（选品器交互） |
| 10_选品模块数据库完整设计 | 16张表SQL设计+ER关系+关键设计特点 | 第八章（数据库） |

---

**文档版本**: v2.0  
**最后更新**: 2026-07-21  
**整合范围**: 01~10号调研设计文档全部有效内容  
**输出定位**: 针对现有系统的可落地升级重构方案，前后端可直接据此进行下一阶段完整开发迭代

# CBHunter 产品编辑模块开发指导意见

> **文档类型**: 开发指导  
> **研究基础**: Shopee / TikTok Shop / TEMU / 妙手ERP 四平台产品编辑页面深度调研  
> **版本**: v1.0  
> **日期**: 2026-07-21

---

## 一、核心结论

CBHunter产品编辑模块应采用**"统一底座 + 平台适配器 + 弹窗式编辑"**架构，以妙手ERP的双层弹窗模式为交互骨架，吸收Shopee的步骤式表单结构、TEMU的三层SKU模型、TikTok的多站点差异化能力，构建一个既能批量操作又能平台定制的统一编辑系统。

**关键设计原则**：
1. **弹窗优先**：在列表页内完成编辑，不跳转页面（参考妙手ERP）
2. **Schema驱动动态表单**：类目选择后动态加载字段（参考Shopee）
3. **三层SKU模型**：SPU→SKC→SKU兼容TEMU全托管，两行规格兼容普通平台
4. **图片编辑器解耦**：iframe嵌入，支持批量编辑（参考妙手ERP+易可图）
5. **JSONB扩展字段**：平台差异通过JSONB存储，避免硬编码

---

## 二、产品编辑页面架构设计

### 2.1 整体布局

```
┌─────────────────────────────────────────────────────────────────┐
│                    产品编辑弹窗 (ElDialog / Modal)               │
├──────────────────────┬──────────────────────────────────────────┤
│                      │                                        │
│   左侧步骤导航        │            右侧内容区                     │
│   (Shopee风格)       │                                          │
│                      │  ┌────────────────────────────────────┐  │
│  ① 基本信息           │  │ 标签页: 基本信息 | 销售资料 | 图片  │  │
│  ② 销售资料           │  │              | 物流 | 其他          │  │
│  ③ 图片管理           │  └────────────────────────────────────┘  │
│  ④ 物流设置           │                                          │
│  ⑤ 其他属性           │  [取消] [保存草稿] [创建/更新] [发布]    │
│                      │                                          │
├──────────────────────┴──────────────────────────────────────────┤
│  iframe: 图片编辑器组件（可切换自研/易可图）                       │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 弹窗层级结构

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

---

## 三、数据模型设计

### 3.1 核心表结构

```sql
-- 商品主表
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    seller_id BIGINT NOT NULL,
    platform_code VARCHAR(20) NOT NULL,  -- shopee/tiktok temu
    country_code VARCHAR(10),           -- PH/SG/MY/TH/VN/ID/US/UK
    product_name VARCHAR(500),
    description TEXT,
    category_path JSONB,                -- 类目路径
    brand VARCHAR(100),
    images JSONB,                       -- 主图数组
    video_url VARCHAR(500),
    status VARCHAR(30),                 -- draft/published/offline/deleted
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- SKU子表
CREATE TABLE skus (
    id BIGINT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    sku_id VARCHAR(100),                -- 平台分配SKU ID
    seller_sku_code VARCHAR(100),       -- 商家货号
    variant_attrs JSONB,                -- {spec1: "颜色", spec2: "尺寸"}
    price_cny DECIMAL(10,2),
    stock_qty INTEGER,
    dimensions JSONB,                   -- {length, width, height}
    weight_g INTEGER,
    sku_images JSONB,                   -- SKU级别图片
    supply_price_cny DECIMAL(10,2),     -- TEMU供货价
    status VARCHAR(30),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 平台扩展字段表
CREATE TABLE product_extensions (
    id BIGINT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    platform_code VARCHAR(20) NOT NULL,
    ssp_id VARCHAR(100),                -- Shopee标准商品编号
    hot_listing_status VARCHAR(30),     -- Hot Listing状态
    sps_score DECIMAL(3,1),             -- TikTok卖家体验分
    spu_id VARCHAR(100),                -- TEMU SPU ID
    skc_id VARCHAR(100),                -- TEMU SKC ID
    supply_price_cny DECIMAL(10,2),     -- TEMU申报价格
    price_status VARCHAR(30),           -- TEMU开款价格状态
    warehouse_group VARCHAR(100),       -- TEMU备货仓组
    stocking_logic VARCHAR(20),         -- JIT/VMI
    qualification_status VARCHAR(30),   -- TEMU商品资质状态
    live_photo_status VARCHAR(30),      -- TEMU实拍图状态
    compliance_info_status VARCHAR(30), -- TEMU合规信息状态
    custom_fields JSONB,                -- 其他平台特有字段
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 国别配置表
CREATE TABLE country_configs (
    id BIGINT PRIMARY KEY,
    country_code VARCHAR(10) UNIQUE,
    currency_code VARCHAR(10),
    currency_symbol VARCHAR(10),
    tax_rate DECIMAL(5,2),
    payment_methods JSONB,
    logistics_channels JSONB,
    category_tree_version VARCHAR(50),
    compliance_requirements JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 3.2 字段映射策略

| CBHunter标准字段 | Shopee | TikTok | TEMU | 妙手 |
|-----------------|--------|--------|------|------|
| product_name | title | name | product_name | 标题 |
| images | main_images | main_images | images | 产品图片 |
| category_path | category_id | category_id | category_path | 预发布类目 |
| skus[] | variations | variants | SPU/SKC/SKU | 规格一/二 |
| price_cny | selling_price | selling_price | supply_price_cny | 售价 |
| stock_qty | quantity | quantity | warehouse_stock | 库存 |
| description | description | description | description | 描述 |
| dimensions | — | — | volume_weight | 体积重量 |
| brand | brand | brand | — | — |

---

## 四、动态表单引擎设计

### 4.1 Schema驱动机制

```typescript
// 类目属性Schema示例
interface CategoryAttributeSchema {
  category_id: string;
  platform_code: string;
  attributes: AttributeField[];
}

interface AttributeField {
  key: string;
  label: string;
  type: 'text' | 'number' | 'select' | 'multi_select' | 'image' | 'richtext';
  required: boolean;
  options?: Array<{label: string, value: string}>;
  validation?: ValidationRule;
  platform_specific?: boolean;  // 是否平台特有
}

// 动态表单渲染器
class DynamicFormRenderer {
  render(schema: CategoryAttributeSchema): React.Component[] {
    return schema.attributes.map(attr => {
      switch(attr.type) {
        case 'text': return <TextInput field={attr} />;
        case 'select': return <SelectInput field={attr} />;
        case 'image': return <ImageUpload field={attr} />;
        // ...
      }
    });
  }
}
```

### 4.2 平台适配器注入

```typescript
interface PlatformAdapter {
  getExtensions(categoryId: string): AttributeField[];
  validate(product: Product): ValidationResult;
  transformToPlatform(product: UnifiedProduct): PlatformPayload;
}

// Shopee适配器
class ShopeeAdapter implements PlatformAdapter {
  getExtensions(categoryId: string) {
    return [
      {key: 'ssp_id', label: 'SSP编号', type: 'text', platform_specific: true},
      {key: 'hot_listing_status', label: 'Hot Listing', type: 'select', options: [...]}
    ];
  }
}

// TEMU适配器
class TemuAdapter implements PlatformAdapter {
  getExtensions(categoryId: string) {
    return [
      {key: 'spu_id', label: 'SPU ID', type: 'text'},
      {key: 'skc_id', label: 'SKC ID', type: 'text'},
      {key: 'supply_price_cny', label: '申报价格(CNY)', type: 'number', required: true},
      {key: 'qualification_status', label: '商品资质', type: 'upload', required: true}
    ];
  }
}
```

---

## 五、SKU/变体管理设计

### 5.1 两层规格模式（Shopee/TikTok/妙手）

```
规格一：颜色（红色/蓝色/绿色）
规格二：尺寸（小号/中号/大号）

生成SKU矩阵：
┌─────────┬─────────┬─────────┬─────────┐
│ 红色    │ 蓝色    │ 绿色    │         │
├─────────┼─────────┼─────────┼─────────┤
│ 小号    │ 红-小   │ 蓝-小   │ 绿-小   │
│ 中号    │ 红-中   │ 蓝-中   │ 绿-中   │
│ 大号    │ 红-大   │ 蓝-大   │ 绿-大   │
└─────────┴─────────┴─────────┴─────────┘
```

### 5.2 三层SKU模式（TEMU）

```
SPU（标准产品单元）
├── SKC 1（标准颜色单元 - 黑色）
│   ├── SKU 1（黑色/小号）
│   └── SKU 2（黑色/中号）
└── SKC 2（标准颜色单元 - 棕色）
    ├── SKU 3（棕色/小号）
    └── SKU 4（棕色/中号）
```

### 5.3 SKU图片管理

```
主图管理：
[图1] [图2] [图3] [图4] [图5] [图6] [图7] [图8] [图9]
      ↑ 拖拽排序

SKU图片管理：
┌─────────────────────────────────────────┐
│ SKU: 红色/小号                          │
│ [SKU图1] [SKU图2] [SKU图3] [+添加]      │
├─────────────────────────────────────────┤
│ SKU: 蓝色/中号                          │
│ [SKU图1] [SKU图2] [+添加]               │
└─────────────────────────────────────────┘
```

### 5.4 SKU生成规则

参考妙手ERP的灵活规则：
- 默认规则：`{货源ID}_{规格1}_{规格2}`
- 分隔符可选：下划线/横杠/空
- 超限保护：超过100个SKU时提示用户确认，而非自动删除
- 支持Excel批量导入SKU矩阵

---

## 六、图片编辑器集成方案

### 6.1 架构设计

```
ImageEditorManager
├── 内置编辑器（基础版）
│   ├── 上传/预览
│   ├── 裁剪/旋转
│   ├── 尺寸修改
│   ├── 水印添加
│   └── 批量处理（最多10张）
│
└── 外部编辑器（增强版）
    ├── 易可图 iframe
    │   └── https://www.yiketu.com/photo/editor?__idcode={token}
    ├── AI设计
    ├── 智能抠图
    ├── 图片翻译
    └── 主图模板库
```

### 6.2 妙手ERP的启示

妙手ERP将图片编辑器作为独立iframe嵌入批量编辑弹窗，这个设计非常值得借鉴：
- **解耦**：图片编辑器独立维护，不阻塞主表单
- **批量**：支持一次性编辑多张图片
- **功能丰富**：易可图提供AI设计、智能抠图、图片翻译等高级功能
- **会员体系**：免费版每次10张，会员可100张

### 6.3 CBHunter实现建议

**第一阶段（MVP）**：
- 使用内置轻量级编辑器
- 支持：上传、预览、裁剪、旋转、水印
- 图片存储到CDN，返回URL

**第二阶段**：
- 集成易可图或类似SaaS服务
- 支持批量编辑（10张/次）
- 支持AI设计、智能抠图等高级功能

**第三阶段**：
- 根据用户需求自研完整编辑器
- 支持更多电商专用功能（主图模板、商品堆品、切图等）

---

## 七、批量编辑功能设计

### 7.1 批量编辑弹窗

参考妙手ERP的批量编辑弹窗，支持以下批量操作：

| 操作 | 说明 | 实现方式 |
|------|------|----------|
| 批量标题优化 | AI自动优化/关键词随机组合 | NLP API + 规则引擎 |
| 批量图片编辑 | 调用图片编辑器批量处理 | iframe嵌入 |
| 批量SKU修改 | 表格内直接编辑 | 动态表格组件 |
| 批量价格调整 | 公式计算（如统一加价10%） | 计算器组件 |
| 批量类目设置 | 类目选择器 | 下拉选择 |
| Excel粘贴支持 | 产品标题搜索支持逗号分隔 | 文本解析器 |

### 7.2 批量编辑流程

```
1. 用户在列表页勾选多个商品
2. 点击"批量编辑"按钮
3. 打开批量编辑弹窗
4. 选择要编辑的字段（标题/图片/SKU/价格/类目/描述）
5. 在弹窗内编辑（支持表格内直接修改）
6. 点击"保存"批量提交
7. 显示编辑结果（成功/失败数量）
```

---

## 八、平台适配器设计

### 8.1 适配器接口

```typescript
interface PlatformAdapter {
  // 字段映射
  mapFieldsToPlatform(product: UnifiedProduct): PlatformPayload;
  
  // 平台特有字段
  getPlatformExtensions(): ExtensionSchema;
  
  // 验证规则
  validate(payload: PlatformPayload): ValidationResult;
  
  // 提交到平台
  submit(payload: PlatformPayload): Promise<SubmitResult>;
  
  // 同步平台变更回CBHunter
  syncFromPlatform(platformData: any): UnifiedProduct;
  
  // 获取平台类目树
  getCategoryTree(countryCode: string): Promise<CategoryNode[]>;
  
  // 获取平台物流渠道
  getLogisticsChannels(countryCode: string): Promise<LogisticsChannel[]>;
}
```

### 8.2 各平台适配器重点

#### Shopee Adapter
- 注入SSP/Hot Listing字段
- Smart Diagnosis状态同步
- Advance Fulfillment库存管理
- 优惠券/Flash Sale关联

#### TikTok Adapter
- SPS评分关联
- CRM配额管理
- 跨境/本地店权限区分
- 多站点货币/类目/物流切换

#### Temu Adapter
- SPU/SKC/SKU三层模型
- 供货价模式（非零售价）
- 合规强制要求（资质/实拍图/合规信息）
- 备货仓组/JIT/VMI模式
- 建议零售价合规检查

#### Miaoshou Adapter
- 采集箱集成
- 货源价格分离展示
- 批量操作模板
- 标题优化/AI助理

---

## 九、开发优先级与里程碑

### 9.1 P0 - 第一期（4周）

**目标**：完成基础编辑能力

| 任务 | 工时 | 依赖 |
|------|------|------|
| 数据库表设计（products/skus/extensions/country_configs） | 3天 | 无 |
| 商品编辑弹窗框架 | 5天 | 数据库 |
| 基本信息表单（图片/标题/类目/描述） | 5天 | 弹窗框架 |
| SKU管理（两层规格模式） | 5天 | 数据库 |
| 平台适配器框架（字段映射+提交） | 5天 | 数据库 |
| 基础图片上传/预览 | 3天 | 弹窗框架 |

### 9.2 P1 - 第二期（4周）

**目标**：完善动态表单和批量编辑

| 任务 | 工时 | 依赖 |
|------|------|------|
| 动态表单引擎（Schema驱动） | 7天 | P0 |
| TEMU三层SKU模式 | 5天 | P0 |
| 批量编辑功能 | 7天 | P0 |
| 图片编辑器集成（基础版） | 5天 | P0 |
| 国别配置动态加载 | 5天 | P0 |

### 9.3 P2 - 第三期（4周）

**目标**：增强功能和平台特性

| 任务 | 工时 | 依赖 |
|------|------|------|
| 易可图编辑器集成 | 7天 | P1 |
| AI标题优化/关键词组合 | 5天 | P1 |
| 平台特有功能集成 | 7天 | P1 |
| Excel批量导入/导出 | 5天 | P1 |
| 性能优化（懒加载/虚拟滚动） | 5天 | P1 |

---

## 十、风险与注意事项

### 10.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 平台API变更频繁 | 适配器失效 | 抽象接口，快速迭代 |
| SPA页面渲染问题 | 数据采集困难 | DOM扫描+API逆向结合 |
| 图片编辑器跨域限制 | iframe通信复杂 | 使用postMessage通信 |
| SKU矩阵爆炸 | 性能问题 | 限制最大SKU数量，分页加载 |
| 多币种精度问题 | 金额错误 | 统一CNY存储，显示层格式化 |

### 10.2 业务风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 平台合规要求变化 | 商品下架 | 实时监控合规状态 |
| 自动模式限制 | 无法自动操作 | 只读优先，手动确认 |
| 跨平台字段冲突 | 数据不一致 | JSONB扩展字段隔离 |
| 批量操作误操作 | 大量错误 | 二次确认+回滚机制 |

### 10.3 用户体验风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 弹窗过大 | 遮挡内容 | 响应式弹窗，最大宽度限制 |
| 表单过于复杂 | 用户困惑 | 分步引导，必填项标记 |
| 图片加载慢 | 体验差 | CDN加速+懒加载 |
| 批量编辑无反馈 | 不确定结果 | 实时进度条+结果汇总 |

---

## 十一、总结

CBHunter产品编辑模块的核心竞争力在于：

1. **统一编辑体验**：四个平台的商品在一个弹窗内编辑，无需切换系统
2. **批量操作效率**：参考妙手ERP的批量编辑模式，提升运营效率
3. **平台特性兼容**：通过适配器层兼容各平台特有字段和流程
4. **动态扩展能力**：Schema驱动的动态表单，新增平台只需新增适配器
5. **图片编辑集成**：解耦的图片编辑器，支持基础版和增强版切换

**最终建议**：以妙手ERP的双层弹窗架构为基础，吸收Shopee的步骤式表单、TEMU的三层SKU模型、TikTok的多站点能力，构建一个高效、灵活、可扩展的统一产品编辑系统。

# 颐贞 Eregen — 社区老人多维数字身份腕带场景扩展设计（v1.0）

> 编制日期：2026-07-23  
> 版本：v1.0（首次完整方案）  
> 状态：待评审  
> 对应文件：基于 `project/Eregen/2026-07-21-medical-wristband-upgrade-design.md` + `2026-07-22-medical-wristband-regulatory-closure-design.md` 增量扩展  
> 项目性质：在现有医用电子腕带架构基础上，扩展社区老人场景 — 将腕带从"住院患者身份识别工具"升级为"老年人多维数字身份凭证"

---

## 第一部分 业务需求

### 1.1 背景与目标

现有颐贞 Eregen 平台已覆盖两大核心业务线：

| 业务线 | 硬件 | 场景 | 功能 |
|--------|------|------|------|
| **社区老人安全监护** | 三档手环（Starter/Plus/Pro） | 居家安全 | 生理监测、跌倒检测、防走失、SOS |
| **医院住院患者管理** | 医用腕带（ESP32-S3） | 住院医疗 | 身份识别、用药核对、监管闭环 |

本次迭代在以上基础上，新增**第三大业务线 — 社区老人多维数字身份场景**：

> 让社区老人佩戴的电子腕带（同构硬件）成为**统一的身份认证凭证**，在社区医院实现特病认证、按需用药、民政补助签到激活等多重功能，同时保留手环原有的安全监护能力。

**核心目标：**

1. **社区医院特病认证** — 老人到社区医院就诊/取药时，药师/护士通过 Web BLE 扫描腕带，自动识别其特病身份和福利标签，按需发放药物或提供医疗保障服务
2. **民政补助签到激活** — 老人定期到社区医院签到，一次签到同时激活所有福利标签（医疗+民政+残联+公交），系统批量发放补助资金
3. **多部门联动** — 社区医院作为唯一认证入口，民政局/残联/医保局通过数据接口获取认证结果，无需老人跑多个部门
4. **家属透明化** — 家属可通过 APP/小程序查看老人的福利状态、签到记录、补助领取情况
5. **监管合规** — 民政部门可审计福利发放的合规性，防止冒领、重复领取

### 1.2 与现有系统的关系

```
┌─────────────────────────────────────────────────────────────┐
│                    Eregen 平台全景                           │
│                                                             │
│  ┌──────────────────┐   ┌──────────────────────────────┐   │
│  │  现有业务（不动）   │   │  新增社区老人场景（增量）      │   │
│  │                  │   │                              │   │
│  │  手环 Entry/Plus/Pro│  │  社区医疗腕带（独立分支）     │   │
│  │  药盒 Basic/Smart │  │  （同构 ESP32-S3 + Cat1）    │   │
│  │  云平台核心模块    │   │  mode=community              │   │
│  │  家属APP/管理后台/小程序 │ │  社区老人档案 / 福利标签  │   │
│  │  医用腕带 hospital │   │  签到激活 / 药房发药        │   │
│  │  监管专区          │   │  民政联动 / 家属福利视图     │   │
│  └──────────────────┘   └──────────────────────────────┘   │
│                                                             │
│  共享基础设施：                                              │
│  ├── SQLite 主库（现有表 + 医用表 + 社区表）                 │
│  ├── EMQX MQTT Broker（eregen/community/wb/# 新命名空间）   │
│  └── NATS JetStream（eregen.community.wb.# 新主题）         │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 涉及角色与视图矩阵

| 功能模块 | 社区医院药师/护士 | 民政局管理员 | 残联管理员 | 家属（APP/小程序） | 卫健委/监管方 |
|---------|:--------------:|:-----------:|:---------:|:----------------:|:-----------:|
| 社区老人总览 | ✅（本科室） | ❌ | ❌ | ❌ | ✅ |
| 老人档案管理 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 腕带绑定/解绑 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 福利标签管理 | ✅（只读） | ✅ | ✅ | ✅（简化版） | ✅ |
| 签到总览 | ✅（本科室） | ✅ | ❌ | ✅（父母） | ✅ |
| 特病认证/用药 | ✅ | ❌ | ❌ | ✅（简化版） | ❌ |
| 民政补助签到 | ✅ | ✅ | ❌ | ✅（提醒） | ✅ |
| 福利发放记录 | ✅（只读） | ✅ | ✅ | ✅ | ✅ |
| 签到异常告警 | ✅（本科室） | ✅ | ❌ | ❌ | ✅ |
| 穿透审计 | ✅ | ✅ | ✅ | ❌ | ✅ |
| 统计看板 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 数据批量导入 | ✅ | ✅ | ✅ | ❌ | ❌ |

### 1.4 核心业务流程

#### 流程一：社区医院特病认证 + 按需用药

```
老人持腕带到社区医院
    ↓
药师/护士打开管理后台 → 点击"近场核验" → Web BLE 扫描腕带
    ↓
腕带返回: dev_id + elder_id_hash + alert_tags[] + welfare_tags[]
    ↓
云端查询:
  ├── 老人档案（姓名、年龄、身份证号、残疾等级等）
  ├── 福利标签（孤寡/特困/残疾/特病/公交优惠资格）
  ├── 特病用药清单（医生医嘱 + 医保目录）
  └── 当期签到状态（本月是否已签到）
    ↓
系统返回认证结果:
  ├── ✅ 身份认证通过 — 特病等级、福利标签
  ├── 📋 可领取药物清单（基于特病目录 + 当周期医嘱）
  ├── 🏥 可领取医疗保障服务（免费检查项目等）
  └── 📅 签到状态 — 本期是否已签到
    ↓
药师确认发药 → 扫描药物条码 → 系统核销 → 记录发药日志
    ↓
腕带更新: 本地缓存最新用药标签（下次快速显示）
    ↓
监管留痕: 谁发的、给谁的、发了什么、何时发的、费用明细
```

#### 流程二：民政补助签到激活

```
老人到社区医院（无论是否取药）
    ↓
药师扫描腕带 → 触发签到
    ↓
系统检查: 老人当期（月度）签到状态
    ↓
若未签到 → 标记"已签到" → 自动激活本期福利:
  ├── 医疗: 特病用药资格 ✅
  ├── 民政: 贫困补助/特困照顾激活 ✅
  ├── 残联: 残疾补贴激活 ✅
  └── 公交: 当月乘车优惠资格激活 ✅（规划中）
    ↓
批量发放引擎（每月固定日期执行）:
  ├── 扫描所有"本月已签到"的老人
  ├── 生成发放清单
  └── 批量打入各老人绑定的银行账户/民政卡
    ↓
若当月未签到 → 补助暂停 → 次月需补签到才能恢复
    ↓
家属端收到通知: "您的父母已完成本月签到，补助将于 X 日发放"
```

#### 流程三：福利标签联动机制

```
一次社区医院签到 = 全标签联动激活:

社区医院终端扫描腕带
    ↓
云端执行标签联动:
  ├── 医疗标签组:
  │   ├── 特病认定 → 更新医保局目录
  │   ├── 用药清单 → 同步药房库存
  │   └── 免费检查 → 预约体检排期
  ├── 民政标签组:
  │   ├── 孤寡认定 → 更新民政局台账
  │   ├── 特困补助 → 标记本期发放资格
  │   └── 贫困救助 → 激活医疗救助金抵扣
  ├── 残联标签组:
  │   ├── 残疾等级 → 更新残联数据库
  │   └── 残疾补贴 → 标记本期发放资格
  └── 公交标签组（规划中）:
      └── 敬老优惠 → 同步交通局结算系统
    ↓
所有标签变更写入审计日志
    ↓
家属APP实时推送: "父母福利标签已全部更新"
```

### 1.5 深度挖掘 — 更多场景需求

基于对现有系统和上述需求的深入理解，以下场景值得纳入规划：

#### 场景 A：紧急医疗绿色通道

```
老人在社区医院突发急病
    ↓
药师/护士扫描腕带 → 系统立即展示:
  ├── 过敏史（青霉素过敏等）
  ├── 特殊疾病（高血压、糖尿病等）
  ├── 血型
  ├── 紧急联系人（家属电话）
  ├── 当前用药清单（避免药物冲突）
  └── 福利状态（自动触发医疗救助金预审批）
    ↓
系统自动:
  ├── 通知急诊科准备接收
  ├── 预审批医疗救助金（特困/孤寡老人免押金入院）
  └── 推送消息给家属："您的父母正在接受紧急治疗"
```

#### 场景 B：慢病用药依从性管理

```
社区医院为特病老人建立用药档案
    ↓
每次到院取药时:
  ├── 系统记录取药时间、药品、剂量
  ├── 对比医嘱频率，判断是否漏服/过量
  └── 发现异常 → 触发干预
    ↓
干预措施:
  ├── 轻度异常 → 药师口头提醒 + APP推送
  ├── 中度异常 → 护士电话随访
  └── 严重异常 → 医生上门走访 + 家属通知
    ↓
数据沉淀:
  ├── 用药依从性评分（月度/季度）
  ├── 趋势分析（用药规律性变化）
  └── 异常模式识别（突然停药、频繁超量等）
```

#### 场景 C：跨社区医院互认

```
老人跨社区医院就诊（如搬家、出差、探亲）
    ↓
在新社区医院扫描腕带 → 系统识别:
  ├── 原所属社区医院信息
  ├── 跨院认证请求
  └── 原医院共享医疗档案（授权范围内）
    ↓
原医院药师确认放行 → 新医院获得临时访问权限
    ↓
取药/检查完成后，数据回写原医院档案
```

#### 场景 D：福利资格年审自动化

```
传统方式: 老人每年需到多个部门提交材料年审
    ↓
年审期间，社区医院集中办理:
  ├── 扫描腕带 → 调取老人档案
  ├── 系统自动检查: 身份信息、福利标签、银行账户
  ├── 缺失材料 → 提示老人补充
  └── 材料齐全 → 一键提交年审
    ↓
系统自动分发年审请求到各相关部门:
  ├── 民政局 → 孤寡/特困年审
  ├── 残联 → 残疾等级年审
  ├── 医保局 → 特病认定年审
  └── 街道办 → 贫困救助年审
    ↓
各部门在线审核 → 结果同步到腕带标签
```

#### 场景 E：死亡注销联动

```
老人去世后:
  ├── 医院出具死亡证明 → 录入系统
  ├── 系统自动:
  │   ├── 暂停所有福利发放
  │   ├── 通知民政局更新台账
  │   ├── 通知残联更新台账
  │   ├── 通知家属（APP推送）
  │   └── 腕带标记"已注销" → 不可再用于认证
  └── 腕带回收/销毁流程启动
```

#### 场景 F：福利发放异常检测

```
规则引擎新增检测规则:
  ├── R_C01: 重复领取 — 同一老人在不同社区医院重复签到
  ├── R_C02: 冒领嫌疑 — 腕带非本人使用（长时间无生理数据 + 非本人活动轨迹）
  ├── R_C03: 异常高频 — 短期内频繁到社区医院取药/签到
  ├── R_C04: 僵尸账户 — 腕带长期离线 + 老人无签到记录
  ├── R_C05: 补助未到账 — 已激活发放但银行返回失败
  └── R_C06: 跨区领取 — 同一福利标签在多个区县被使用
```

---

## 第二部分 功能设计

### 2.1 管理后台页面结构

在现有管理后台侧边栏"医护工作站"下方新增"社区老人专区"菜单项：

```
管理后台
├── 仪表盘（不动）
├── 设备管理（不动）
├── 用户管理（不动）
├── 订阅管理（不动）
├── 医护工作站（不动，住院患者场景）
├── 监管专区（不动，住院监管）
└── 社区老人专区（【新增】）
    ├── 老人档案管理
    ├── 福利标签管理
    ├── 签到总览
    ├── 药房发药记录
    ├── 民政数据导入
    └── 统计看板
```

### 2.2 社区医院终端交互功能

社区医院终端即管理后台中的"社区老人专区"页面，通过浏览器访问。

#### 2.2.1 腕带扫描认证流程

```
药师/护士打开社区老人专区 → 点击"腕带扫描"
    ↓
浏览器调用 Web BLE API → 扫描附近医用腕带
    ↓
选择目标腕带 → 系统自动读取:
  ├── dev_id（腕带设备 ID）
  ├── elder_id_hash（老人 ID 哈希）
  ├── alert_tags[]（医疗警示标签）
  └── welfare_tags[]（福利标签快照）
    ↓
前端用 elder_id_hash 请求云端 API
    ↓
返回完整老人档案 + 福利标签 + 用药清单
    ↓
药师查看老人信息 → 执行认证操作:
  ├── [✅ 身份认证通过] — 显示特病等级、福利状态
  ├── [📋 领取药物] — 显示可领取清单，确认后发药
  ├── [🏥 领取服务] — 显示可领取的免费检查项目
  ├── [📅 签到激活] — 手动触发当期签到
  └── [❌ 认证失败] — 腕带异常/无档案/福利过期
```

#### 2.2.2 老人档案快速查看

```
┌─────────────────────────────────────┐
│  老人：张秀兰                       │
│  身份证号：******1234                │
│  性别：女  年龄：76 岁              │
│  户籍：XX市XX区XX街道               │
├─────────────────────────────────────┤
│  身份标签：                         │
│  ● 孤寡老人（民政局认定）            │
│  ● 特困户（2025-2028有效）           │
│  ● 残疾二级（残联认定）              │
│  ● 特病门诊（医保认定）              │
├─────────────────────────────────────┤
│  福利状态（本期）:                   │
│  ● 贫困补助 — 已激活（7月）          │
│  ● 残疾补贴 — 已激活（7月）          │
│  ● 公交优惠 — 已激活（7月）          │
│  ● 医疗救助 — 已激活（7月）          │
├─────────────────────────────────────┤
│  用药清单（特病）:                   │
│  ● 氨氯地平 5mg po qd              │
│  ● 二甲双胍 500mg po bid           │
│  ● 阿司匹林 100mg po qd            │
├─────────────────────────────────────┤
│  最近签到: 2026-07-15               │
│  下次签到截止: 2026-08-15           │
├─────────────────────────────────────┤
│  [📋 完整档案]  [📅 签到记录]  [💊 用药记录] │
└─────────────────────────────────────┘
```

### 2.3 民政数据批量导入

#### 2.3.1 导入模板

街道/居委会定期（月度/季度）提供以下 Excel/CSV 模板：

```csv
姓名,身份证号,福利类型,认定等级,有效期开始,有效期结束,备注
张秀兰,510101195001011234,特困,一级,2025-01-01,2028-12-31,
李建国,510101194805055678,残疾,二级,2024-06-01,2027-05-31,肢体残疾
王美芳,510101195503039012,孤寡,NA,2026-01-01,2027-12-31,
```

#### 2.3.2 导入流程

```
街道/居委会上传 Excel/CSV
    ↓
系统校验:
  ├── 身份证号格式
  ├── 福利类型枚举值
  ├── 日期合法性
  ├── 重复记录检测
  └── 与现有老人档案匹配
    ↓
校验结果:
  ├── 匹配成功 → 自动赋予福利标签
  ├── 匹配失败 → 标记"待人工审核"
  └── 格式错误 → 返回错误行号及原因
    ↓
人工审核后 → 批量生效 → 腕带标签同步更新
```

### 2.4 批量发放引擎

```
每月固定日期（如每月 15 日）自动执行:
    ↓
1. 扫描所有"本月已签到"的老人
    ↓
2. 生成发放清单:
  ├── 贫困补助: 每人 ¥XXX/月 → 总计 ¥XXX
  ├── 残疾补贴: 每人 ¥XXX/月 → 总计 ¥XXX
  ├── 特困照顾: 每人 ¥XXX/月 → 总计 ¥XXX
  └── 医疗救助金: 按实际发生额 → 总计 ¥XXX
    ↓
3. 调用银行接口批量打款:
  ├── 成功 → 标记"已发放"
  ├── 失败 → 标记"发放失败" + 原因
  └── 重试 → 失败 3 次后转人工处理
    ↓
4. 生成发放报表:
  ├── 发放总数/金额/成功率
  ├── 失败清单及原因
  └── 推送给民政局管理员
```

### 2.5 规则引擎扩展

在现有监管规则引擎（R01-R08）基础上，新增社区场景检测规则：

| 规则编号 | 规则名称 | 检测逻辑 | 告警级别 |
|---------|---------|---------|---------|
| R_C01 | 重复领取 | 同一老人同月内在不同社区医院签到 | 高 |
| R_C02 | 冒领嫌疑 | 腕带认证后无生理数据上报 + 活动轨迹异常 | 高 |
| R_C03 | 异常高频 | 7 天内签到/取药 > 5 次 | 中 |
| R_C04 | 僵尸账户 | 腕带离线 > 30 天 + 无签到记录 | 低 |
| R_C05 | 补助未到账 | 已激活发放但银行返回失败 | 高 |
| R_C06 | 跨区领取 | 同一福利标签在多个区县被使用 | 中 |
| R_C07 | 福利过期未停 | 福利标签已过有效期但仍在使用 | 中 |
| R_C08 | 死亡未注销 | 老人已出具死亡证明但腕带仍活跃 | 高 |

### 2.6 公交优惠场景（规划中，暂不实施）

> 本节仅做架构预留，不在本期实施范围内。

#### 2.6.1 架构预留设计

```
未来公交结算系统对接方案:

腕带 → 公交刷卡机 (BLE) → 本地认证 → 离线记账 → 日终对账
    ↓
或:
腕带 → 社区医院签到 → 云端标记公交资格 → 交通局查询云端状态 → 批量结算
```

**推荐方案：云端标记 + 批量结算**（更安全、更易与公交公司对接）

- 老人到社区医院签到时，系统自动标记"当月公交优惠资格已激活"
- 交通局/公交公司通过 API 查询老人资格状态
- 月底按激活人数与民政局批量结算补贴差额
- 腕带本身不直接用于公交刷卡（避免硬件改造复杂度）

#### 2.6.2 与公交公司结算的安全考量

| 考量点 | 方案 | 说明 |
|--------|------|------|
| **资格验证** | 公交公司调用云端 API 查询 | 腕带不存储公交密钥，避免密钥泄露风险 |
| **防伪造** | API 双向 TLS + 签名 | 公交公司持有证书，非公开接口 |
| **防重放** | 每次查询带时间戳 + nonce | 同一资格不可重复使用 |
| **离线容灾** | 公交刷卡机缓存当日资格列表 | 网络中断时可本地核验，日终补传 |
| **结算对账** | 云端生成月度结算单 | 公交公司确认无误后民政拨款 |

---

## 第三部分 技术设计

### 3.1 云平台社区模块架构

社区模块以内嵌包形式加入 `admin-api`，不新建独立服务：

```
cloud/admin-api/
├── device_mgmt.go            # 【不动】
├── user_mgmt.go              # 【不动】
├── medical_wb/               # 【不动】医用腕带（住院）模块
├── regulatory/               # 【不动】监管专区模块
└── community_wb/             # 【新增】社区老人模块
    ├── handler/
    │   ├── elderly.go            # 老人档案 CRUD
    │   ├── welfare.go            # 福利标签管理
    │   ├── signin.go             # 签到激活
    │   ├── pharmacy.go           # 社区药房发药
    │   └── minzheng.go           # 民政数据导入/发放
    ├── service/
    │   ├── elderly_svc.go        # 老人业务逻辑
    │   ├── welfare_svc.go        # 福利标签同步/匹配
    │   ├── signin_svc.go         # 签到周期管理
    │   ├── pharmacy_svc.go       # 发药核销逻辑
    │   └── batch_pay_svc.go      # 批量发放引擎
    ├── store/
    │   └── sqlite.go             # 社区数据查询封装
    └── router/
        └── community_routes.go   # 路由注册
```

### 3.2 社区 API 接口设计

#### 3.2.1 老人档案管理

```http
# 老人档案登记（社区医院办理腕绑定时录入）
POST /api/v1/community/elders
Request: {
    "name": "张秀兰",
    "id_card": "510101195001011234",
    "gender": 2,
    "age": 76,
    "address": "XX市XX区XX街道XX小区",
    "emergency_contact": "张三 13800138000",
    "bank_account": "6222021001001234567",
    "welfare_tags": ["orphan", "poverty_level_1", "disability_level_2", "special_disease"],
    "device_id": "CW-0001"
}
Response: {"id": "uuid", "status": "registered"}

# 社区老人列表
GET /api/v1/community/elders?status=active&department=&page=&page_size=
Response: {"elders": [...], "total": 200}

# 老人详情
GET /api/v1/community/elders/:id
Response: {...完整档案...}

# 更新老人信息
PUT /api/v1/community/elders/:id
Request: {"name": "张秀兰", "welfare_tags": [...], ...}
Response: {"id": "uuid", "updated_at": "..."}

# 注销（死亡/迁出）
DELETE /api/v1/community/elders/:id
Request: {"reason": "去世"}
Response: {"id": "uuid", "status": "deactivated"}
```

#### 3.2.2 福利标签管理

```http
# 获取福利标签配置
GET /api/v1/community/welfare/tags/config
Response: {
    "tags": [
        {"code": "orphan", "name": "孤寡老人", "issuer": "民政局", "renewal_period_days": 365},
        {"code": "poverty_level_1", "name": "特困一级", "issuer": "民政局", "renewal_period_days": 365},
        {"code": "disability_level_2", "name": "残疾二级", "issuer": "残联", "renewal_period_days": 365},
        {"code": "special_disease", "name": "特病门诊", "issuer": "医保局", "renewal_period_days": 180},
        {"code": "bus_discount", "name": "公交优惠", "issuer": "交通局", "renewal_period_days": 30}
    ]
}

# 赋予/移除福利标签
POST /api/v1/community/elders/:id/welfare-tags
Request: {"action": "add", "tags": ["poverty_level_1"], "valid_from": "2026-07-01", "valid_to": "2027-06-30"}
Response: {"tag_added": "poverty_level_1", "effective_at": "..."}

# 查询老人当前有效标签
GET /api/v1/community/elders/:id/welfare-tags/active?date=2026-07-23
Response: {
    "active_tags": [
        {"code": "orphan", "name": "孤寡老人", "issuer": "民政局", "valid_until": "2028-12-31"},
        {"code": "poverty_level_1", "name": "特困一级", "issuer": "民政局", "valid_until": "2027-06-30"},
        {"code": "disability_level_2", "name": "残疾二级", "issuer": "残联", "valid_until": "2027-05-31"}
    ]
}
```

#### 3.2.3 签到激活

```http
# 触发签到（社区医院终端调用）
POST /api/v1/community/signin/trigger
Request: {"device_id": "CW-0001", "hospital_id": "CH001", "pharmacist_id": "PH-001"}
Response: {
    "signin_id": "uuid",
    "elder_id": "uuid",
    "elder_name": "张秀兰",
    "signin_time": "2026-07-23T10:30:00Z",
    "period": "2026-07",
    "activated_welfare": ["poverty_level_1", "disability_level_2", "special_disease", "bus_discount"],
    "next_signin_deadline": "2026-08-23"
}

# 查询签到历史
GET /api/v1/community/signin/history?elder_id=&start_date=&end_date=
Response: {"signins": [...], "total": 12}

# 查询本期签到状态
GET /api/v1/community/signin/status?elder_id=&period=2026-07
Response: {"signed_in": true, "signed_in_at": "2026-07-23T10:30:00Z", "period": "2026-07"}
```

#### 3.2.4 社区药房发药

```http
# 获取老人可领取药物清单
GET /api/v1/community/pharmacy/prescriptions?elder_id=&period=2026-07
Response: {
    "elder_name": "张秀兰",
    "special_disease_level": "一级",
    "medications": [
        {"drug_name": "氨氯地平", "dosage": "5mg", "frequency": "qd", "qty_allowed": 30, "qty_dispensed": 0},
        {"drug_name": "二甲双胍", "dosage": "500mg", "frequency": "bid", "qty_allowed": 60, "qty_dispensed": 0}
    ]
}

# 确认发药并核销
POST /api/v1/community/pharmacy/dispense
Request: {
    "elder_id": "uuid",
    "dispensed_items": [
        {"drug_name": "氨氯地平", "qty": 30},
        {"drug_name": "二甲双胍", "qty": 60}
    ],
    "pharmacist_id": "PH-001",
    "period": "2026-07"
}
Response: {"dispense_id": "uuid", "status": "completed", "total_cost": 156.80}
```

#### 3.2.5 民政数据批量导入

```http
# 上传民政批量数据
POST /api/v1/community/minzheng/import
Content-Type: multipart/form-data
File: welfare_list_2026_07.csv
Response: {"imported": 150, "matched": 145, "pending_review": 5, "errors": [...]}

# 查看导入任务状态
GET /api/v1/community/minzheng/import/tasks
Response: {"tasks": [{"id": "uuid", "filename": "welfare_list_2026_07.csv", "status": "completed", "created_at": "..."}]}

# 批量生效审核通过的数据
POST /api/v1/community/minzheng/import/:task_id/approve
Response: {"approved": 145, "effective_at": "2026-07-23T00:00:00Z"}
```

#### 3.2.6 批量发放引擎

```http
# 手动触发批量发放（平时由定时任务自动执行）
POST /api/v1/community/batch-pay/execute
Request: {"period": "2026-07", "pay_types": ["poverty_allowance", "disability_subsidy", "medical_assistance"]}
Response: {
    "batch_id": "uuid",
    "total_elders": 500,
    "total_amount": 250000.00,
    "success": 495,
    "failed": 5,
    "failed_details": [{"elder_id": "...", "reason": "bank_account_closed"}]
}

# 查看发放记录
GET /api/v1/community/batch-pay/records?period=2026-07
Response: {"records": [...], "summary": {"total": 500, "amount": 250000.00, "success_rate": 99.0}}
```

### 3.3 数据库表设计

#### 3.3.1 新增社区场景表

```sql
-- ================================
-- 新增：社区老人档案表
-- ================================
CREATE TABLE community_elders (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    id_card TEXT UNIQUE NOT NULL,         -- 身份证号（唯一核心标识）
    gender INTEGER NOT NULL CHECK (gender IN (0, 1, 2)),
    age INTEGER,
    address TEXT,
    emergency_contact TEXT,               -- 紧急联系人
    bank_account TEXT,                    -- 补助发放银行账户
    hospital_id TEXT,                     -- 所属社区医院
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'deactivated', 'deceased')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deactivated_at DATETIME,
    deactivated_reason TEXT
);

CREATE INDEX idx_ce_id_card ON community_elders(id_card);
CREATE INDEX idx_ce_status ON community_elders(status);
CREATE INDEX idx_ce_hospital ON community_elders(hospital_id);

-- ================================
-- 新增：社区腕带设备表
-- ================================
CREATE TABLE community_wristband_devices (
    id TEXT PRIMARY KEY,
    device_id TEXT UNIQUE NOT NULL,       -- CW-XXXX 格式
    firmware_version TEXT,
    mode TEXT DEFAULT 'community' CHECK (mode IN ('hospital', 'community')),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'retired')),
    last_seen DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idxcwd_mode ON community_wristband_devices(mode);
CREATE INDEX idxcwd_status ON community_wristband_devices(status);

-- ================================
-- 新增：老人-腕带绑定关系
-- ================================
CREATE TABLE community_elder_bindings (
    id TEXT PRIMARY KEY,
    elder_id TEXT NOT NULL REFERENCES community_elders(id),
    device_id TEXT NOT NULL REFERENCES community_wristband_devices(id),
    bound_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    unbound_at DATETIME,
    UNIQUE(elder_id, device_id)
);

CREATE INDEX idxceb_elder ON community_elder_bindings(elder_id);
CREATE INDEX idxceb_device ON community_elder_bindings(device_id);

-- ================================
-- 新增：福利标签配置表（社区场景扩展）
-- ================================
CREATE TABLE community_welfare_tag_config (
    id TEXT PRIMARY KEY,
    tag_code TEXT UNIQUE NOT NULL,        -- orphan/poverty_level_1/disability_level_2/special_disease/bus_discount/...
    tag_name TEXT NOT NULL,
    issuer TEXT NOT NULL,                 -- 民政局/残联/医保局/交通局
    renewal_period_days INTEGER,          -- 年审周期（天）
    benefit_amount REAL,                  -- 月度补助金额（可选）
    enabled INTEGER DEFAULT 1 CHECK (enabled IN (0, 1))
);

-- 预置社区福利标签
INSERT INTO community_welfare_tag_config (tag_code, tag_name, issuer, renewal_period_days, benefit_amount) VALUES
('orphan', '孤寡老人', '民政局', 365, NULL),
('poverty_level_1', '特困一级', '民政局', 365, 800.00),
('poverty_level_2', '特困二级', '民政局', 365, 500.00),
('disability_level_1', '残疾一级', '残联', 365, 600.00),
('disability_level_2', '残疾二级', '残联', 365, 400.00),
('disability_level_3', '残疾三级', '残联', 365, 200.00),
('special_disease', '特病门诊', '医保局', 180, NULL),
('bus_discount', '公交优惠', '交通局', 30, NULL),
('medical_assistance', '医疗救助', '民政局', 365, NULL);

-- ================================
-- 新增：老人-福利绑定关系
-- ================================
CREATE TABLE community_elder_welfare (
    id TEXT PRIMARY KEY,
    elder_id TEXT NOT NULL REFERENCES community_elders(id),
    tag_code TEXT NOT NULL REFERENCES community_welfare_tag_config(tag_code),
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    certified_by TEXT,                    -- 认定机构/人员
    certification_doc TEXT,               -- 认定文件编号
    effective_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    revoked_at DATETIME,
    UNIQUE(elder_id, tag_code, valid_from, valid_to)
);

CREATE INDEX idx_cew_elder ON community_elder_welfare(elder_id);
CREATE INDEX idx_cew_tag ON community_elder_welfare(tag_code);
CREATE INDEX idx_cew_valid ON community_elder_welfare(valid_from, valid_to);

-- ================================
-- 新增：签到记录表
-- ================================
CREATE TABLE community_signin_records (
    id TEXT PRIMARY KEY,
    elder_id TEXT NOT NULL REFERENCES community_elders(id),
    device_id TEXT NOT NULL,
    hospital_id TEXT NOT NULL,
    pharmacist_id TEXT,
    signin_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    period TEXT NOT NULL,                 -- YYYY-MM 格式
    activated_tags TEXT DEFAULT '[]',     -- JSON 数组：本次激活的标签代码
    is_medical_signin INTEGER DEFAULT 1 CHECK (is_medical_signin IN (0, 1)),
    is_welfare_signin INTEGER DEFAULT 1 CHECK (is_welfare_signin IN (0, 1)),
    notes TEXT
);

CREATE INDEX idx_csr_elder ON community_signin_records(elder_id);
CREATE INDEX idx_csr_period ON community_signin_records(period);
CREATE INDEX idx_csr_hospital ON community_signin_records(hospital_id);
CREATE INDEX idx_csr_time ON community_signin_records(signin_time);

-- ================================
-- 新增：社区药房发药记录表
-- ================================
CREATE TABLE community_pharmacy_logs (
    id TEXT PRIMARY KEY,
    elder_id TEXT NOT NULL REFERENCES community_elders(id),
    device_id TEXT,
    hospital_id TEXT NOT NULL,
    pharmacist_id TEXT,
    dispense_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    period TEXT NOT NULL,
    items TEXT NOT NULL,                  -- JSON: [{"drug_name":"氨氯地平","qty":30,"cost":45.00},...]
    total_cost REAL DEFAULT 0,
    insurance_covered REAL DEFAULT 0,     -- 医保报销金额
    self_pay REAL DEFAULT 0,              -- 自付金额
    notes TEXT
);

CREATE INDEX idx_cpl_elder ON community_pharmacy_logs(elder_id);
CREATE INDEX idx_cpl_period ON community_pharmacy_logs(period);
CREATE INDEX idx_cpl_time ON community_pharmacy_logs(dispense_time);

-- ================================
-- 新增：民政数据同步日志表
-- ================================
CREATE TABLE community_minzheng_sync (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,                 -- 民政局/残联/医保局
    filename TEXT,
    imported_count INTEGER DEFAULT 0,
    matched_count INTEGER DEFAULT 0,
    pending_review_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'processing' CHECK (status IN ('processing', 'completed', 'failed')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

-- ================================
-- 新增：批量发放记录表
-- ================================
CREATE TABLE community_batch_payments (
    id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL,
    period TEXT NOT NULL,
    pay_type TEXT NOT NULL,               -- poverty_allowance/disability_subsidy/medical_assistance/...
    elder_id TEXT NOT NULL REFERENCES community_elders(id),
    amount REAL NOT NULL,
    bank_account TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'success', 'failed', 'retrying')),
    failure_reason TEXT,
    executed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cbp_batch ON community_batch_payments(batch_id);
CREATE INDEX idx_cbp_period ON community_batch_payments(period);
CREATE INDEX idx_cbp_status ON community_batch_payments(status);
```

### 3.4 腕带固件扩展（独立分支）

在现有 `firmware/medical-wristband/` 目录下新增 `community/` 子目录：

```
firmware/medical-wristband/
├── esp32s3/                    # 【不动】住院模式固件
│   ├── main/
│   ├── protocol/
│   ├── ota/
│   ├── crypto/
│   └── CMakeLists.txt
└── community/                  # 【新增】社区模式固件（独立分支）
    ├── main/
    │   ├── elder_store.c/h         # 老人档案 NVS/Flash 存储
    │   ├── ble_server.c/h          # BLE GATT 服务（社区医院终端读取）
    │   ├── cat1_mqtt.c/h           # Cat1 联网（下行数据写入）
    │   ├── display_oled.c/h        # OLED 显示（老人姓名+福利标签摘要）
    │   ├── led_indicator.c/h       # LED 福利状态灯
    │   ├── nvs_manager.c/h         # 非易失存储管理
    │   ├── security.c/h            # 数据加密/防篡改
    │   └── board_init.c/h          # 板级初始化
    ├── protocol/
    │   ├── community_protocol.h    # 社区专属消息协议定义
    │   ├── message_encode.c/h      # JSON 编码
    │   └── message_decode.c/h      # JSON 解码
    ├── ota/                      # OTA 更新（复用 hospital 模块）
    ├── crypto/                   # 加密（复用 hospital 模块）
    └── CMakeLists.txt
```

**固件编译产物：**

| 产品线 | 固件版本 | 编译产物 | Topic |
|--------|---------|---------|-------|
| 医用腕带 hospital | 1.0.0 | `medical_wristband.bin` | `eregen/medical/wb/{dev_id}/#` |
| 医用腕带 community | 1.0.0 | `community_wristband.bin` | `eregen/community/wb/{dev_id}/#` |

**BLE GATT 服务扩展（community 模式）：**

```
GATT Service UUID: 0001xxxx-0000-1000-8000-00805f9b34fb  （社区专属）
├── Characteristic 1: Device Info
│   UUID: ...-0001
│   属性：Read
│   数据: dev_id, fw_version, battery_pct, mode=community
├── Characteristic 2: Elder Identity
│   UUID: ...-0002
│   属性：Read (需认证)
│   数据: elder_id_hash, name_hash, id_card_hash
├── Characteristic 3: Alert Tags (医疗警示)
│   UUID: ...-0003
│   属性：Read (需认证)
│   数据: JSON 数组 ["allergy","fall_risk"]
├── Characteristic 4: Welfare Tags (福利标签快照)
│   UUID: ...-0004
│   属性：Read (需认证)
│   数据: JSON 数组 ["orphan","poverty_level_1","disability_level_2"]
├── Characteristic 5: Medical Summary
│   UUID: ...-0005
│   属性：Read (需认证)
│   数据: UTF-8 文本，≤256 字节（过敏史+特殊疾病摘要）
└── Characteristic 6: Auth Challenge
    UUID: ...-0006
    属性：Read/Write
    数据: 随机挑战码 + 配对码验证
```

**OLED 显示扩展（community 模式）：**

```
┌─────────────────────────┐
│  老人姓名                │
│  福利标签:               │
│  ● 孤寡 ● 特困 ● 残疾   │  ← 福利标签滚动显示
├─────────────────────────┤
│  本期签到: 已签到 ✅     │  ← 当期签到状态
│  下次签到: 2026-08-23   │
├─────────────────────────┤
│  最后更新: 2026-07-23   │
│  固件版本: 1.0.0-comm   │
└─────────────────────────┘
```

**LED 福利状态灯：**

| 状态 | LED 颜色 | 闪烁模式 | 说明 |
|------|---------|---------|------|
| 本期已签到 | 绿色 | 常亮 | 福利已激活 |
| 本期未签到 | 黄色 | 慢闪（1Hz） | 提醒老人尽快签到 |
| 福利即将过期 | 橙色 | 快闪（2Hz） | 剩余 < 7 天 |
| 福利已过期 | 红色 | 快闪（2Hz） | 需重新认定 |

### 3.5 规则引擎扩展实现

```go
// cloud/admin-api/community_wb/service/engine_svc.go

type CommunityRuleEngine struct {
    store *store.SQLiteStore
}

func (e *CommunityRuleEngine) Run() {
    ticker := time.NewTicker(5 * time.Minute)  // 与住院监管共用调度
    for range ticker.C {
        e.checkDuplicateSignin()     // R_C01: 重复领取
        e.checkFraudSuspect()        // R_C02: 冒领嫌疑
        e.checkHighFrequency()       // R_C03: 异常高频
        e.checkZombieAccount()       // R_C04: 僵尸账户
        e.checkPaymentFailure()      // R_C05: 补助未到账
        e.checkCrossDistrict()       // R_C06: 跨区领取
        e.checkTagExpired()          // R_C07: 福利过期未停
        e.checkDeathUnregistered()   // R_C08: 死亡未注销
    }
}
```

**各规则检测逻辑：**

| 规则 | 检测逻辑 | 数据来源 |
|------|---------|---------|
| R_C01 | 同一 `elder_id` 在同一天内有多条 `community_signin_records` | 签到记录表 |
| R_C02 | 腕带认证后 24h 内无生理数据上报 + 活动轨迹与老人常住地址偏差 > 5km | 腕带心跳 + 位置日志 + 老人档案 |
| R_C03 | 7 天内签到/取药记录 > 5 次 | 签到记录表 + 发药记录表 |
| R_C04 | 腕带 `last_seen` 超过 30 天无心跳 + 无签到记录 | 腕带设备表 + 签到记录表 |
| R_C05 | `community_batch_payments` 中 `status='failed'` 的记录 | 批量发放记录表 |
| R_C06 | 同一 `tag_code` 在多个 `hospital_id`（不同区县）被使用 | 签到记录表 + 医院表 |
| R_C07 | `community_elder_welfare.valid_to < NOW()` 且 `revoked_at IS NULL` | 老人-福利绑定表 |
| R_C08 | 有死亡证明记录但 `community_elders.status != 'deceased'` | 民政数据同步表 + 老人档案表 |

### 3.6 家属端"父母福利"页面

```
家属 APP / 微信小程序 — "父母福利"页面:

┌─────────────────────────────────────┐
│  父母：张秀兰                       │
│  腕带状态: 在线 ✅                  │
│  最近活动: 2026-07-23 10:30 社区医院│
├─────────────────────────────────────┤
│  福利状态:                          │
│  ● 贫困补助 — 7月已激活 ✅          │
│  ● 残疾补贴 — 7月已激活 ✅          │
│  ● 公交优惠 — 7月已激活 ✅          │
│  ● 医疗救助 — 7月已激活 ✅          │
├─────────────────────────────────────┤
│  签到提醒:                          │
│  下次签到截止: 2026-08-23           │
│  [📱 一键设置提醒]                  │
├─────────────────────────────────────┤
│  补助领取记录:                      │
│  2026-07  贫困补助  ¥800  ✅已发放  │
│  2026-07  残疾补贴  ¥400  ✅已发放  │
│  2026-06  贫困补助  ¥800  ✅已发放  │
├─────────────────────────────────────┤
│  用药记录:                          │
│  2026-07-23  氨氯地平 30片          │
│  2026-06-20  二甲双胍 60片          │
└─────────────────────────────────────┘
```

---

## 第四部分 合规依据

### 4.1 社会救助相关政策

| 政策文件 | 发布单位 | 相关要求 | 本方案对应功能 |
|---------|---------|---------|-------------|
| 《社会救助暂行办法》 | 国务院 | 特困人员基本生活最低标准保障 | 贫困补助标签 + 批量发放引擎 |
| 《残疾人保障法》 | 全国人大常委会 | 残疾人两项补贴（生活补贴+护理补贴） | 残疾等级标签 + 补贴激活 |
| 《城市居民最低生活保障条例》 | 国务院 | 低保对象动态管理、定期复核 | 福利标签有效期 + 年审联动 |
| 《关于进一步加强特困人员救助帮扶工作的通知》 | 民政部 | 特困人员身份认定、资金发放留痕 | 签到记录 + 审计日志 |

### 4.2 数据安全与隐私保护

| 合规项 | 实现方式 |
|--------|---------|
| 身份证号加密存储 | AES-256-GCM 存储，近场传输仅 Hash |
| 银行账户信息隔离 | 银行账号独立加密表，仅批量发放引擎可访问 |
| 最小必要原则 | 腕带本地仅存身份 Hash + 福利标签代码，不存完整档案 |
| 知情同意 | 老人/家属签署《个人信息处理同意书》 |
| 访问控制 | RBAC — 社区医院药师仅可查看本科室老人，民政局仅可查看福利相关数据 |
| 审计追踪 | 所有签到、发药、标签变更、数据导入操作均记录审计日志 |

### 4.3 民政资金发放合规

| 合规要求 | 本方案对应措施 |
|---------|-------------|
| 禁止重复领取 | R_C01 规则检测 — 同一老人同月多医院签到告警 |
| 禁止冒领 | R_C02 规则检测 — 腕带非本人使用告警 |
| 禁止虚报 | 签到记录 + 发药记录交叉比对，监管方可穿透审计 |
| 资金可追溯 | 每笔发放生成 `batch_id`，可追溯到具体老人、具体银行卡 |
| 暂停机制 | 未签到 → 补助暂停 → 补签到后恢复，防止长期无人监管 |

---

## 第五部分 迭代实施计划

### 5.1 本次迭代开发范围

| 模块 | 工作内容 |
|------|---------|
| 社区腕带固件 | `firmware/medical-wristband/community/` 独立分支（老人存储、BLE 服务、Cat1 联网、OLED 福利显示、LED 状态灯） |
| 云平台社区模块 | `community_wb/` 内嵌包（Handler/Service/Store/Router） |
| 数据库扩展 | 新增 9 张社区场景表 + 扩展 1 张腕带设备表 |
| 规则引擎扩展 | 新增 8 条社区场景检测规则 |
| 管理后台社区专区 | Vue 3 新增 6 个页面 |
| 家属端福利页面 | Flutter/WXML 新增"父母福利"页面 |
| 批量发放引擎 | 定时任务 + 银行接口对接 |

### 5.2 迭代批次划分

```
第一批（第 1-2 周）：数据层 + 权限扩展
├── 新增社区场景 9 张表
├── 扩展腕带设备表（增加 mode 字段）
├── 社区模块骨架（router/store 框架）
└── 社区腕带固件工程初始化（ESP32-S3 + CMake + NVS）

第二批（第 3-4 周）：固件核心功能
├── 老人档案 NVS 存储（写入/读取/加密/防篡改）
├── BLE GATT 服务（Elder Identity + Welfare Tags + Medical Summary）
├── Cat1 MQTT 下行数据接收（云端下发福利标签到腕带）
├── OLED 福利显示 + LED 状态灯
└── 福利标签批量导入功能

第三批（第 5-6 周）：云端 API + 管理后台
├── 老人 CRUD API + 福利标签管理 API
├── 签到激活 API + 药房发药 API
├── 民政数据导入 API
├── 管理后台社区专区页面开发
├── Web BLE 近场读取集成
└── 家属端"父母福利"页面

第四批（第 7-8 周）：规则引擎 + 批量发放
├── 社区场景 8 条规则引擎实现
├── 批量发放引擎（定时任务 + 银行接口）
├── 端到端联调（腕带扫描→签到→发药→家属通知）
├── 兼容性测试（现有功能回归测试）
└── 安全测试（BLE 认证、数据加密、访问控制）

第五批（第 9-10 周）：灰度发布 + 文档
├── 内部灰度测试（10% 社区腕带设备）
├── 用户手册编写（社区医院操作手册、民政管理员手册）
└── 全量发布准备
```

### 5.3 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| M1：数据层就绪 | 第 2 周末 | 社区表创建完成，角色权限可用 |
| M2：社区腕带固件可用 | 第 4 周末 | 腕带可存储老人档案，BLE 可读福利标签 |
| M3：云端 API 可用 | 第 6 周末 | 老人 CRUD、签到、发药 API 可调用 |
| M4：管理后台可用 | 第 6 周末 | 社区专区页面可操作 |
| M5：规则引擎可用 | 第 8 周末 | 8 条检测规则 + 批量发放引擎 |
| M6：灰度发布 | 第 10 周末 | 内部测试通过，准备灰度 |

### 5.4 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| 民政数据格式不统一 | 批量导入失败率高 | 提供标准化模板 + 错误行提示 + 人工审核兜底 |
| 老人遗忘签到 | 补助断发引发投诉 | 家属APP提醒 + 社区医院主动短信通知 + 补签到机制 |
| 批量发放银行接口不稳定 | 补助延迟发放 | 支持手动发放模式；失败记录转人工处理 |
| 腕带丢失/损坏 | 老人无法认证身份 | 支持"换带不换人" — 新腕带绑定同一老人档案，旧腕带自动注销 |
| 福利标签变更频繁 | 腕带标签与云端不一致 | 每次签到自动同步最新标签到腕带本地缓存 |
| 跨社区医院互认 | 老人跨区就诊数据不通 | MVP 阶段限定在本社区医院范围内；未来扩展互认 |

---

## 附录 A：与原有设计文档的关系

| 原设计文档 | 本方案补充内容 |
|-----------|-------------|
| `2026-07-21-medical-wristband-upgrade-design.md` | 新增 community 固件分支（独立于 hospital）、社区老人档案、福利标签体系、批量发放引擎 |
| `2026-07-22-medical-wristband-regulatory-closure-design.md` | 监管专区新增"社区福利监管"子模块、规则引擎扩展 8 条社区规则 |
| `2026-07-22-medical-wristband-market-research.md` | 市场研究不涉及社区场景，本方案为其独立扩展 |

---

## 附录 B：术语表（扩展）

| 术语 | 说明 |
|------|------|
| RBAC | Role-Based Access Control，基于角色的访问控制 |
| BLE | Bluetooth Low Energy，低功耗蓝牙 |
| GATT | Generic Attribute Profile，BLE 属性配置文件 |
| NVS | Non-Volatile Storage，非易失存储 |
| OTA | Over-The-Air，空中升级 |
| Cat1 | Cellular Type 1，蜂窝通信制式 |
| MQTT | Message Queuing Telemetry Transport，消息队列遥测传输 |
| HIS | Hospital Information System，医院信息系统 |
| PIPL | Personal Information Protection Law，个人信息保护法 |
| 孤寡 | 无子女、无配偶、无监护人的独居老人 |
| 特困 | 无劳动能力、无生活来源、无法定赡养人的低收入群体 |
| 特病 | 特殊疾病，享受门诊特殊慢性病待遇的疾病类别 |
| 批量发放 | 民政补助资金的定期批量银行转账发放机制 |
| 签到激活 | 老人定期签到以维持福利资格有效的机制 |

---

© 2026 Eregen (颐贞). All rights reserved.

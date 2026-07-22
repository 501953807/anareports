# 颐贞 Eregen — 医用电子腕带监管闭环功能需求方案（v1.0）

> 编制日期：2026-07-22  
> 版本：v1.0（首次完整方案）  
> 状态：待评审  
> 对应文件：基于 `project/Eregen/2026-07-21-medical-wristband-upgrade-design.md` 增量扩展  
> 项目性质：业务闭环 + 多角色权限 + 监管抓手 — 零额外硬件投入

---

## 第一部分 业务需求

### 1.1 背景与目标

现有医用电子腕带方案已覆盖住院患者身份识别、护士近场核验、家属端信息查看等核心功能。本次迭代的目标是在**不改变平台架构、不增加额外硬件投入**的前提下，通过**多角色权限管理 + 业务闭环数据留痕 + 规则引擎**，为卫健委/医保等监管部门提供可操作的监管抓手，形成"病人—家属—医院—监管部门"四方闭环。

### 1.2 监管要解决的核心问题

| 问题 | 现有漏洞 | 本次闭环方案 |
|------|---------|-------------|
| **挂床住院** | 病人办了入院但实际不在院，医院虚报在院天数 | 每日在院核验（护士扫码腕带）+ 连续无核验告警 |
| **虚假入院** | 没有病人就造入院记录骗医保 | 入院登记必须绑定腕带设备，住院号唯一校验 |
| **费用与治疗不匹配** | 开了用药/检查记录但实际未执行 | 每次给药/输液/抽血/检查都需扫码核验并记录 |
| **电子围栏越界** | 病人离开医院无人知晓 | Cat1 基站定位 + 围栏计算 + 超时告警 |
| **转科/出院不及时** | 病人已转科或出院，系统状态未更新 | 转科/出院操作触发腕带信息更新和监管通知 |
| **数据不可追溯** | 监管方看不到完整链条 | 所有环节产生审计日志，监管方可穿透查看 |

### 1.3 涉及角色与视图矩阵

| 功能模块 | 医院管理员 | 科室护士 | 卫健委/监管方 | 家属（APP/小程序） |
|---------|:---------:|:-------:|:-----------:|:----------------:|
| 全院在院患者总览 | ✅ | ❌ | ✅ | ❌ |
| 本科室患者列表 | ✅ | ✅ | ✅ | ❌ |
| 腕带绑定/解绑 | ✅ | ❌ | ❌ | ❌ |
| 近场核验 | ✅ | ✅ | ❌ | ❌ |
| 每日诊疗录入 | ✅ | ✅ | ❌ | ❌ |
| 费用清单 | ✅ | ❌ | ✅ 只读 | ✅ 简化版 |
| 用药清单 | ✅ | ❌ | ✅ 只读 | ✅ 简化版 |
| 检测报告 | ✅ | ❌ | ✅ 只读 | ✅ 结果摘要 |
| 电子围栏告警 | ✅ | ✅（本科室） | ✅ | ❌ |
| 异常时长告警 | ✅ | ✅（本科室） | ✅ | ❌ |
| 穿透审计（全链路追溯） | ✅ | ❌ | ✅ | ❌ |
| 统计看板 | ✅ | ✅（本科室） | ✅ | ❌ |
| 规则配置（阈值/围栏） | ✅ | ❌ | ✅ | ❌ |
| 合规审查报表 | ✅ | ❌ | ✅ | ❌ |
| 每日查房记录 | ✅ | ✅ | ❌ | ❌ |
| 过敏史/特殊疾病 | ✅ | ✅ | ❌ | ❌ |
| 位置/围栏数据 | ✅ | ✅ | ✅ | ❌ |

### 1.4 业务闭环流程

```
入院登记 → 绑定腕带 → 写入信息 → 在院核验 → 治疗执行 → 出院注销
  │          │          │          │          │          │
  ▼          ▼          ▼          ▼          ▼          ▼
监管看     监管记     监管录     监管核     监管验     监管留
```

每个环节的监管数据点：

| 环节 | 医院操作 | 监管数据点 | 电子围栏联动 |
|------|---------|-----------|-------------|
| **入院** | 登记患者信息、分配住院号、绑定腕带 | 入院时间、绑定腕带ID、科室、床号 | — |
| **在院** | 每日查房、护士扫码核验 | 核验时间戳、核验类型、护士账号 | 每次核验确认患者在院；超出围栏阈值触发告警 |
| **治疗** | 给药/输液/抽血/检查前扫码核对 | 操作时间、操作类型、腕带快照 | 治疗执行时自动校验位置（必须在院内） |
| **转科** | 修改科室和床号 | 转科时间、原科室、新科室 | 围栏范围随新科室更新 |
| **出院** | 出院操作、清空腕带 | 出院时间、出院原因、腕带清空记录 | 围栏状态解除 |

---

## 第二部分 业务功能设计

### 2.1 管理后台页面结构

在现有管理后台侧边栏"医护工作站"下方新增"监管专区"菜单项：

```
管理后台
├── 仪表盘（不动）
├── 设备管理（不动）
├── 用户管理（不动）
├── 订阅管理（不动）
├── 医护工作站（不动，扩展监管字段）
│   ├── 患者登记
│   ├── 腕带绑定
│   ├── 每日录入
│   └── 核验记录
└── 监管专区（【新增】）
    ├── 在院总览（实时看板）
    ├── 异常告警
    ├── 穿透审计
    ├── 规则配置
    └── 合规审查
```

### 2.2 监管异常检测规则引擎

内置以下检测规则，阈值均可配置：

| 规则编号 | 规则名称 | 检测逻辑 | 告警级别 |
|---------|---------|---------|---------|
| R01 | 挂床住院 | 连续 N 小时无护士扫码核验记录（默认 24h） | 高 |
| R02 | 电子围栏越界 | 定位超出医院围栏且停留 > N 分钟（默认 30min） | 高 |
| R03 | 虚假入院 | 腕带已绑定但 48h 内无核验记录 | 中 |
| R04 | 费用突增 | 单患者日费用 > 科室均值 3 倍 | 中 |
| R05 | 用药与核验不匹配 | 有用药记录但无给药核验记录 | 中 |
| R06 | 频繁转科 | 7 天内转科 > 3 次 | 低 |
| R07 | 腕带异常断开 | 腕带信号突然中断超过 2h | 高 |
| R08 | 长期不在院 | 出院后腕带未清空 | 低 |

### 2.3 电子围栏定位方案（零额外硬件）

MVP 阶段使用 Cat1 蜂窝网络的基站定位能力，腕带无需增加 GPS 芯片：

| 定位方式 | 精度 | 功耗 | 成本 | 适用场景 |
|---------|------|------|------|---------|
| **基站三角定位（MVP）** | 50m–2km | 低（Cat1 已有） | 零增加 | 医院建筑群围栏（半径 200–500m）足够 |
| GPS（未来可选） | 5–10m | 高 | 需换芯片 | 超大型院区 |

**基站定位实现方式：**
- Cat1 模组（如 EC20/AE910）可通过 AT 指令获取当前服务基站的 CID/TAC/LAC 信息
- 云平台查询基站坐标数据库（如工信部基站数据库或第三方 API），将基站 ID 转换为经纬度
- 使用 Haversine 公式计算患者位置与医院中心的距离，判断是否在围栏内

**定位频率策略：**

| 场景 | 上报频率 | 说明 |
|------|---------|------|
| 正常在院 | 每 30 分钟 | 低功耗模式 |
| 接近围栏边界（距围栏 < 500m） | 每 5 分钟 | 自动切换 |
| 已越界 | 每 1 分钟 | 高频追踪 |
| 护士正在核验时 | 实时锁定为 in-fence | 治疗执行期间 |

---

## 第三部分 功能设计

### 3.1 云平台监管模块架构

监管模块以内嵌包形式加入 `admin-api`，不新建独立服务：

```
cloud/admin-api/
├── device_mgmt.go            # 【不动】
├── user_mgmt.go              # 【不动】
├── medical_wb/               # 【不动】医用腕带模块
│   ├── handler/
│   ├── service/
│   ├── store/
│   └── router/
└── regulatory/               # 【新增】监管专区模块
    ├── handler/
    │   ├── dashboard.go          # 在院总览
    │   ├── alert.go              # 异常告警列表/确认
    │   ├── audit.go              # 穿透审计
    │   ├── rule_config.go        # 规则配置 CRUD
    │   └── compliance.go         # 合规审查报表
    ├── service/
    │   ├── fence_svc.go          # 电子围栏计算
    │   ├── engine_svc.go         # 规则引擎定时检测
    │   └── audit_svc.go          # 全链路数据聚合
    ├── store/
    │   └── sqlite.go             # 监管数据查询封装
    └── router/
        └── regulatory_routes.go  # 路由注册
```

### 3.2 监管 API 接口设计

#### 3.2.1 在院总览（实时看板）

```http
# 在院患者总览摘要
GET /api/v1/regulatory/dashboard/patient-overview
    Query: hospital_id=&department=
    Response: {
        "total_admitted": 150,
        "today_admit": 8,
        "today_discharge": 5,
        "by_department": [
            {"name": "心内科", "count": 45, "alert_count": 2},
            {"name": "呼吸科", "count": 38, "alert_count": 0}
        ],
        "fence_violations_today": 3,
        "no_verify_24h": 5
    }

# 在院患者列表（含围栏和告警状态）
GET /api/v1/regulatory/dashboard/patient-list
    Query: department=&status=admitted&page=&page_size=
    Response: {
        "patients": [
            {
                "id": "...",
                "name": "王秀英",
                "admission_no": "20260721001",
                "department": "心内科",
                "bed_no": "12",
                "bound_at": "2026-07-21T08:00:00Z",
                "last_verify": "2026-07-22T06:30:00Z",
                "verify_gap_hours": 24,
                "fence_status": "inside",
                "fence_exit_duration_sec": 0,
                "alert_tags": ["allergy", "fall_risk"],
                "alerts_triggered": ["R01"]
            }
        ],
        "total": 150
    }
```

#### 3.2.2 异常告警

```http
# 告警列表
GET /api/v1/regulatory/alerts
    Query: level=&rule_code=&department=&status=pending&page=&page_size=
    Response: {
        "alerts": [
            {
                "id": "...",
                "rule_code": "R01",
                "rule_name": "挂床住院",
                "patient_id": "...",
                "patient_name": "王秀英",
                "department": "心内科",
                "severity": "high",
                "triggered_at": "2026-07-22T06:00:00Z",
                "detail": "连续24小时无护士扫码核验记录",
                "status": "pending"
            }
        ],
        "total": 12
    }

# 确认告警
POST /api/v1/regulatory/alerts/:id/acknowledge
Request: { "user_id": "regulator-001" }
Response: { "status": "acknowledged" }

# 标记已解决
POST /api/v1/regulatory/alerts/:id/resolve
Request: { "user_id": "regulator-001", "notes": "已核实，患者外出检查" }
Response: { "status": "resolved" }
```

#### 3.2.3 穿透审计（全链路追溯）

```http
# 任意患者全链路数据
GET /api/v1/regulatory/audit/patient/:id
    Response: {
        "patient": { ...完整患者信息... },
        "binding": {
            "device_id": "WB-0001",
            "bound_at": "2026-07-21T08:00:00Z",
            "unbound_at": null
        },
        "verifications": [
            {
                "time": "2026-07-21T09:00:00Z",
                "action": "give_medication",
                "nurse": "护士A",
                "result": "success",
                "read_data": { "dev_id": "WB-0001", "alert_tags": ["allergy"] }
            }
        ],
        "medications": [
            { "drug_name": "氨氯地平", "dosage": "5mg", "executed_at": "2026-07-21T09:05:00Z", "verified": true }
        ],
        "expenses": [
            { "item_name": "CT 检查", "amount": 350, "recorded_date": "2026-07-21" }
        ],
        "daily_entries": [
            { "date": "2026-07-21", "type": "round", "content": "患者血压稳定" }
        ],
        "fence_logs": [
            { "time": "2026-07-21T14:30:00Z", "lat": 30.5, "lng": 104.0, "event": "exited_fence" },
            { "time": "2026-07-21T15:10:00Z", "lat": 30.57, "lng": 104.06, "event": "returned_fence" }
        ],
        "alerts_generated": [
            { "rule_code": "R01", "triggered_at": "2026-07-22T06:00:00Z", "resolved": false }
        ]
    }
```

#### 3.2.4 规则配置

```http
# 获取所有规则配置
GET /api/v1/regulatory/rules
Response: {
    "rules": [
        {
            "code": "R01",
            "name": "挂床住院",
            "enabled": true,
            "config": { "max_verify_gap_hours": 24, "severity": "high" }
        },
        {
            "code": "R02",
            "name": "电子围栏越界",
            "enabled": true,
            "config": { "max_fence_exit_minutes": 30, "severity": "high" }
        }
    ]
}

# 修改规则配置
PUT /api/v1/regulatory/rules/:code/config
Request: { "config": { "max_verify_gap_hours": 48, "severity": "medium" } }
Response: { "code": "R01", "updated_at": "..." }
```

#### 3.2.5 围栏配置

```http
# 配置医院围栏
POST /api/v1/regulatory/fence/config
Request: {
    "hospital_id": "H001",
    "hospital_name": "市中心医院",
    "center_lat": 30.5728,
    "center_lng": 104.0668,
    "radius_meters": 200
}
Response: { "id": "...", "status": "configured" }

# 获取围栏配置
GET /api/v1/regulatory/fence/config?hospital_id=H001
Response: { "hospital_id": "H001", "center_lat": 30.5728, "center_lng": 104.0668, "radius_meters": 200 }
```

#### 3.2.6 合规审查报表

```http
# 周期合规报表
GET /api/v1/regulatory/compliance/report
    Query: hospital_id=&start_date=&end_date=
    Response: {
        "summary": {
            "total_patients_period": 500,
            "avg_stay_days": 5.2,
            "fence_violations": 23,
            "no_verify_alerts": 45,
            "expense_anomalies": 12,
            "med_verify_mismatch": 8,
            "compliance_rate": 94.5
        },
        "department_breakdown": [
            {
                "name": "心内科",
                "total_patients": 45,
                "alerts": 12,
                "compliance_rate": 96.0
            }
        ]
    }
```

### 3.3 数据库表设计

#### 3.3.1 新增监管相关表

```sql
-- ================================
-- 新增：医院围栏配置表
-- ================================
CREATE TABLE regulatory_fence_config (
    id TEXT PRIMARY KEY,
    hospital_id TEXT NOT NULL,
    hospital_name TEXT NOT NULL,
    center_lat REAL NOT NULL,
    center_lng REAL NOT NULL,
    radius_meters INTEGER DEFAULT 200,
    enabled INTEGER DEFAULT 1 CHECK (enabled IN (0, 1)),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hospital_id)
);

-- ================================
-- 新增：位置日志（电子围栏数据来源）
-- ================================
CREATE TABLE regulatory_location_logs (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL REFERENCES medical_wristband_patients(id),
    device_id TEXT NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    accuracy REAL,
    inside_fence INTEGER DEFAULT 1 CHECK (inside_fence IN (0, 1)),
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rll_patient ON regulatory_location_logs(patient_id);
CREATE INDEX idx_rll_time ON regulatory_location_logs(recorded_at);
CREATE INDEX idx_rll_fence ON regulatory_location_logs(inside_fence, recorded_at);

-- ================================
-- 新增：监管告警表
-- ================================
CREATE TABLE regulatory_alerts (
    id TEXT PRIMARY KEY,
    rule_code TEXT NOT NULL,
    patient_id TEXT REFERENCES medical_wristband_patients(id),
    hospital_id TEXT,
    department TEXT,
    severity TEXT CHECK (severity IN ('low', 'medium', 'high')),
    alert_type TEXT NOT NULL CHECK (alert_type IN (
        'no_verify', 'fence_violation', 'fake_admission',
        'expense_spike', 'med_verify_mismatch',
        'frequent_transfer', 'device_disconnect', 'post_discharge'
    )),
    detail TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'acknowledged', 'resolved', 'false_positive')),
    triggered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at DATETIME,
    acknowledged_by TEXT,
    resolved_at DATETIME,
    resolved_by TEXT,
    notes TEXT
);

CREATE INDEX idx_ra_rule ON regulatory_alerts(rule_code);
CREATE INDEX idx_ra_status ON regulatory_alerts(status);
CREATE INDEX idx_ra_patient ON regulatory_alerts(patient_id);
CREATE INDEX idx_ra_triggered ON regulatory_alerts(triggered_at);
CREATE INDEX idx_ra_dept ON regulatory_alerts(department, status);

-- ================================
-- 扩展：患者表新增围栏字段
-- ================================
ALTER TABLE medical_wristband_patients ADD COLUMN last_verify_at DATETIME;
ALTER TABLE medical_wristband_patients ADD COLUMN verify_gap_hours INTEGER DEFAULT 0;
ALTER TABLE medical_wristband_patients ADD COLUMN fence_status TEXT DEFAULT 'inside' CHECK (fence_status IN ('inside', 'outside', 'unknown'));
ALTER TABLE medical_wristband_patients ADD COLUMN fence_exit_at DATETIME;
ALTER TABLE medical_wristband_patients ADD COLUMN fence_exit_duration_sec INTEGER DEFAULT 0;
```

#### 3.3.2 角色权限表扩展

在现有用户表基础上扩展角色：

```sql
-- 现有 users 表增加 role 字段（如果尚未有）
-- role 枚举值：super_admin, hospital_admin, nurse, regulator, family_member

-- 科室权限关联表
CREATE TABLE user_department_bindings (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    department TEXT NOT NULL,
    bound_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- 限制护士只能查看本科室患者，卫健委可查看所有科室
```

### 3.4 规则引擎实现

规则引擎是 `admin-api` 内的一个轻量定时任务，每 5 分钟执行一轮检测：

```go
// cloud/admin-api/regulatory/service/engine_svc.go

type RuleEngine struct {
    store *store.SQLiteStore
}

func (e *RuleEngine) Run() {
    ticker := time.NewTicker(5 * time.Minute)
    for range ticker.C {
        e.checkNoVerify()       // R01: 挂床住院
        e.checkFenceViolation() // R02: 电子围栏越界
        e.checkFakeAdmission()  // R03: 虚假入院
        e.checkExpenseSpike()   // R04: 费用突增
        e.checkMedVerifyMatch() // R05: 用药与核验不匹配
        e.checkFrequentTransfer()
        e.checkDeviceDisconnect()
        e.checkPostDischarge()
    }
}
```

**各规则检测逻辑：**

| 规则 | 检测逻辑 | 数据来源 |
|------|---------|---------|
| R01 | 查询 `medical_wristband_patients` 中 `verify_gap_hours >= 24` 且 `status = admitted` 的记录 | 患者表 + 核验记录表 |
| R02 | 查询 `regulatory_location_logs` 中最近一条 `inside_fence = 0` 且 `记录时间距今 > 30min` 的患者 | 位置日志表 + 围栏配置 |
| R03 | 腕带绑定超过 48h 但 `medical_verifications` 中无任何核验记录 | 绑定关系表 + 核验记录表 |
| R04 | 计算患者当日费用总和，与同科室患者日均费用比较，超过 3 倍 | 费用表 |
| R05 | 对比 `medical_medications` 中的用药记录和 `medical_verifications` 中的给药核验记录 | 用药表 + 核验记录表 |
| R06 | 统计患者 7 天内转科次数 | 患者表（历史状态变更） |
| R07 | 腕带 `last_seen` 超过 2h 无心跳 | 腕带设备表 |
| R08 | 患者 `status = discharged` 但腕带未清空（`medical_wristband_devices` 仍有绑定） | 患者表 + 绑定表 |

### 3.5 电子围栏定位数据流

```
腕带 Cat1 模组
    ↓ AT 指令获取基站 CID/TAC/LAC
    ↓ MQTT 上行: eregen/medical/wb/{dev_id}/location
    ↓
云平台 data-pipeline 消费 location 消息
    ↓ 查询基站坐标数据库 → 转换为 lat/lng
    ↓ 读取 regulatory_fence_config 获取围栏参数
    ↓ Haversine 公式: distance = 2R * arcsin(sqrt(...))
    ↓ 判断 inside_fence = (distance <= radius_meters)
    ↓
    ├── 写入 regulatory_location_logs 表
    ├── 更新 medical_wristband_patients.fence_status
    └── 如果 outside_fence：
        ├── 启动计时器
        ├── 超过 30min → 生成 R02 告警到 regulatory_alerts
        └── 返回围栏内 → 清除计时器，标记 resolved
```

### 3.6 家属端隐私控制

| 数据类型 | 家属可见内容 | 脱敏规则 |
|---------|------------|---------|
| 用药清单 | 药名 + 用法 + 频次 | 不含剂量详情 |
| 费用清单 | 项目名称 + 金额 | 不含诊断关联 |
| 检测报告 | 正常/异常标记 + 结论摘要 | 不含详细指标 |
| 每日查房记录 | ❌ 不开放 | 隐私数据 |
| 过敏史/特殊疾病 | ❌ 不开放 | 敏感医疗信息 |
| 位置/围栏数据 | ❌ 不开放 | 监管数据 |
| 核验记录 | ❌ 不开放 | 医护操作记录 |

---

## 第四部分 合规依据

本方案设计参考以下法规和标准：

### 4.1 医疗质量安全核心制度（国家卫健委）

| 制度名称 | 相关要求 | 本方案对应功能 |
|---------|---------|-------------|
| **查对制度** | 医嘱执行、给药、输血、手术、检查前必须核对患者身份 | 护士扫码腕带核验，记录核验日志 |
| **首诊负责制度** | 患者入院必须有明确的接诊记录和责任人 | 入院登记绑定腕带，记录护士账号 |
| **交接班制度** | 患者状态变化必须交接并记录 | 转科操作触发状态变更和监管通知 |
| **病历管理制度** | 病历书写及时、准确、完整 | 每日诊疗录入，不可篡改 |
| **分级护理制度** | 不同护理级别患者有不同巡视频率 | 警示标签分级（P0/P1/P2），影响核验频率 |

### 4.2 患者安全目标（国家卫健委）

| 目标 | 本方案对应措施 |
|------|-------------|
| 正确识别患者身份 | 住院号唯一标识 + 腕带条码 + BLE 近场读取 |
| 加强用药安全 | 用药前扫码核对 + 过敏警示标签 |
| 加强临床"危重"患者管理 | 跌倒高危、昏迷等标签差异化显示 |
| 确保手术安全 | 手术前核验记录留存 |

### 4.3 医保基金监管条例

| 监管要求 | 本方案对应措施 |
|---------|-------------|
| 禁止虚构医疗服务 | 每日核验记录证明患者真实在院 |
| 禁止分解住院 | 转科操作与入院记录分离，防止拆分 |
| 禁止串换项目 | 费用清单与用药/检测核验记录交叉比对 |
| 禁止挂床住院 | 电子围栏 + 无核验告警 R01 |

### 4.4 个人信息保护法（PIPL）

| 合规要求 | 本方案对应措施 |
|---------|-------------|
| 最小必要原则 | 腕带本地仅存身份标识 + 警示标签，不存完整医疗清单 |
| 知情同意 | 患者入院签署《个人信息处理同意书》 |
| 访问控制 | RBAC 角色权限，医护仅可查看管辖范围 |
| 数据安全 | AES-256-GCM 存储加密 + TLS 1.3 传输加密 |
| 数据删除 | 出院腕带必须清空，不可恢复 |

---

## 第五部分 迭代实施计划

### 5.1 本次迭代开发范围

| 模块 | 工作内容 | 对应原设计文档章节 |
|------|---------|-----------------|
| 监管 API | `regulatory/` 内嵌包（Handler/Service/Store/Router） | 本章第三部分 |
| 规则引擎 | 定时任务，8 条检测规则 | 本章 3.4 |
| 电子围栏 | 基站定位 + 围栏计算 + 告警 | 本章 2.3 + 3.5 |
| 管理后台监管专区 | Vue 3 新增 5 个页面 | 本章 2.1 |
| 数据库扩展 | 新增 3 张表 + 扩展 2 张表 | 本章 3.3 |
| 角色权限扩展 | users 表 role 字段 + 科室绑定 | 本章 3.3.2 |
| 家属端隐私过滤 | 现有"住院治疗"页面增加脱敏逻辑 | 本章 3.6 |

### 5.2 迭代批次划分

```
第一批（第 1 周）：数据层 + 权限扩展
├── 新增监管相关表（regulatory_fence_config / location_logs / alerts）
├── 扩展患者表（围栏字段）
├── 用户角色扩展 + 科室绑定
└── 监管模块骨架（router/store 框架）

第二批（第 2-3 周）：规则引擎 + 围栏
├── 基站定位数据接收 + 围栏计算
├── 规则引擎 8 条规则实现
├── 告警 CRUD API
└── 位置日志存储

第三批（第 4-5 周）：监管前端 + 审计
├── 监管专区 5 个页面（总览/告警/审计/规则/合规）
├── 穿透审计 API（全链路数据聚合）
├── 规则配置前端
└── 合规报表 API

第四批（第 6 周）：联调测试
├── 端到端联调（入院→围栏→告警→审计）
├── 家属端隐私过滤回归测试
├── 兼容性测试（现有功能不受影响）
└── 全量发布准备
```

### 5.3 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| M1：数据层就绪 | 第 1 周末 | 监管表创建完成，角色权限可用 |
| M2：围栏+告警可用 | 第 3 周末 | 电子围栏计算 + 规则引擎 + 告警 API |
| M3：监管前端可用 | 第 5 周末 | 监管专区 5 个页面可操作 |
| M4：全量发布 | 第 6 周末 | 端到端闭环验证通过 |

### 5.4 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| 基站定位精度不足 | 围栏误判（医院建筑密集区可能偏差较大） | MVP 阶段设置较大围栏半径（200-500m），后续升级 GPS |
| 规则引擎误报 | 告警过多导致监管疲劳 | 支持误报标记（false_positive），积累数据后优化阈值 |
| SQLite 并发查询性能 | 穿透审计涉及 6+ 表 JOIN | MVP 阶段限制并发用户数，未来切 PG 解决 |
| 角色权限泄露 | 护士看到其他科室数据 | RBAC 严格校验，每查询加 department 过滤 |

---

## 附录 A：与原有设计文档的关系

| 原设计文档章节 | 本方案补充内容 |
|-------------|-------------|
| 第四部分 医用腕带功能需求规格 | 新增监管角色视图、电子围栏、规则引擎 |
| 第六部分 数据结构与接口设计 | 新增监管表族（3 张新表 + 2 张扩展表）、监管 API（6 组接口） |
| 第七部分 兼容性保障 | 新增角色权限兼容测试项 |
| 第八部分 迭代实施计划 | 新增监管模块实施批次 |

---

## 附录 B：术语表（扩展）

| 术语 | 说明 |
|------|------|
| RBAC | Role-Based Access Control，基于角色的访问控制 |
| Haversine | 球面两点间距离计算公式 |
| Cat1 | Cellular Type 1，蜂窝通信制式 |
| PIPL | Personal Information Protection Law，个人信息保护法 |
| DRG | Diagnosis Related Groups，按疾病诊断相关分组付费 |
| DIP | Diagnosis-Intervention Packet，按病种分值付费 |
| 挂床住院 | 患者办理入院手续但实际不在院的违规行为 |
| 电子围栏 | 基于地理坐标的虚拟边界，用于监控患者位置 |
| 穿透审计 | 监管部门对任意患者的全链路数据追溯能力 |

---

© 2026 Eregen (颐贞). All rights reserved.

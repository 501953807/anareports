# 医用电子腕带监管闭环功能需求方案 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有医用腕带方案基础上，新增多角色权限管理、规则引擎、电子围栏和穿透审计，形成"病人—家属—医院—监管部门"四方闭环。

**Architecture:** 监管模块以内嵌包 `regulatory/` 形式加入 `admin-api`，不新建独立服务；数据库新增 3 张表 + 扩展 2 张表；管理后台新增"监管专区"菜单（5 个页面）。MVP 阶段使用 Cat1 基站定位实现电子围栏，零额外硬件投入。

**Tech Stack:** Go + Gin（后端）、SQLite（数据库）、Vue 3 + Element Plus（前端）、NATS JetStream（事件分发）

## Global Constraints

- 零破坏原则：所有新增内容为增量开发，禁止修改、删减、重构原有项目架构、目录、代码、业务逻辑
- 轻量 MVP 原则：当前不做微服务拆分、分布式、高可用、集群架构设计，拒绝过度设计
- 数据库降级：MVP 阶段全项目使用 SQLite 替代 PostgreSQL/InfluxDB/Redis
- 路由隔离：监管 API 使用 `/api/v1/regulatory/` 前缀，不与现有 `/api/v1/medical/` 冲突
- 数据隔离：监管表使用 `regulatory_` 前缀，与现有 `medical_wristband_` 表族物理隔离
- 角色权限：RBAC 严格校验，每查询加 department 过滤
- 家属端隐私：家属 APP/小程序仅开放用药简化版、费用简化版、检测报告摘要，隐私数据不开放

---

## 文件结构总览

```
cloud/admin-api/
├── regulatory/                    # 【新增】监管专区内嵌包
│   ├── handler/
│   │   ├── dashboard.go           # 在院总览 API
│   │   ├── alert.go               # 异常告警 CRUD
│   │   ├── audit.go               # 穿透审计
│   │   ├── rule_config.go         # 规则配置 CRUD
│   │   └── compliance.go          # 合规审查报表
│   ├── service/
│   │   ├── fence_svc.go           # 电子围栏计算
│   │   ├── engine_svc.go          # 规则引擎定时检测
│   │   └── audit_svc.go           # 全链路数据聚合
│   ├── store/
│   │   └── sqlite.go              # 监管数据查询封装
│   └── router/
│       └── regulatory_routes.go   # 路由注册 + 中间件
apps/admin-web/src/views/
└── regulatory/                    # 【新增】监管专区页面
    ├── Dashboard.vue              # 在院总览
    ├── Alerts.vue                 # 异常告警列表
    ├── AuditDetail.vue            # 穿透审计详情
    ├── RuleConfig.vue             # 规则配置
    └── ComplianceReport.vue       # 合规审查报表
database/
└── migrations/                    # 【新增】数据库迁移脚本
    └── 001_regulatory_closure.sql # 监管闭环 DDL
```

---

### Task 1: 数据库迁移 — 新增监管表族

**Files:**
- Create: `database/migrations/001_regulatory_closure.sql`
- Modify: `cloud/admin-api/regulatory/store/sqlite.go`（后续任务）

**Interfaces:**
- Consumes: （无依赖，本任务是基础）
- Produces: 以下 SQLite 表和索引

**步骤：**

- [ ] **Step 1: 编写 DDL 迁移脚本**

创建 `database/migrations/001_regulatory_closure.sql`：

```sql
-- ================================================
-- 医用电子腕带监管闭环 — 数据库迁移脚本
-- 执行日期：2026-07-22
-- ================================================

-- ================================
-- 新增：医院围栏配置表
-- ================================
CREATE TABLE IF NOT EXISTS regulatory_fence_config (
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
CREATE TABLE IF NOT EXISTS regulatory_location_logs (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
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
CREATE TABLE IF NOT EXISTS regulatory_alerts (
    id TEXT PRIMARY KEY,
    rule_code TEXT NOT NULL,
    patient_id TEXT,
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

-- ================================
-- 扩展：科室权限绑定表
-- ================================
CREATE TABLE IF NOT EXISTS user_department_bindings (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    department TEXT NOT NULL,
    bound_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, department)
);

CREATE INDEX idx_udb_user ON user_department_bindings(user_id);
CREATE INDEX idx_udb_dept ON user_department_bindings(department);
```

- [ ] **Step 2: 验证 SQL 语法正确性**

运行 SQLite 解析检查：

```bash
sqlite3 :memory: < database/migrations/001_regulatory_closure.sql
echo $?
```

预期输出：`0`（无错误）

- [ ] **Step 3: Commit**

```bash
git add database/migrations/001_regulatory_closure.sql
git commit -m "feat(db): add regulatory closure migration scripts"
```

---

### Task 2: 监管模块骨架 — Router + Store

**Files:**
- Create: `cloud/admin-api/regulatory/router/regulatory_routes.go`
- Create: `cloud/admin-api/regulatory/store/sqlite.go`

**Interfaces:**
- Consumes: Task 1 的数据库表结构
- Produces:
  - `RegisterRoutes(gin.RouterGroup)` — 注册所有监管路由
  - `RegulatoryStore` struct — SQLite 操作封装

**步骤：**

- [ ] **Step 1: 创建 regulatory 模块目录结构**

```bash
mkdir -p cloud/admin-api/regulatory/{handler,service,store,router}
```

- [ ] **Step 2: 编写 Store 层 — `store/sqlite.go`**

```go
package store

import (
	"database/sql"
	"fmt"
)

type RegulatoryStore struct {
	db *sql.DB
}

func NewRegulatoryStore(db *sql.DB) *RegulatoryStore {
	return &RegulatoryStore{db: db}
}

// FenceConfig queries fence configuration by hospital_id
func (s *RegulatoryStore) FenceConfig(hospitalID string) (*struct {
	ID             string
	HospitalID     string
	HospitalName   string
	CenterLat      float64
	CenterLng      float64
	RadiusMeters   int
	Enabled        int
}, error) {
	row := s.db.QueryRow(`
		SELECT id, hospital_id, hospital_name, center_lat, center_lng,
		       radius_meters, enabled
		FROM regulatory_fence_config
		WHERE hospital_id = ?`, hospitalID)
	// ... scan into result struct
}

// LocationLogsByPatient returns location logs for a patient within time range
func (s *RegulatoryStore) LocationLogsByPatient(patientID, start, end string) ([]struct {
	ID           string
	PatientID    string
	Lat          float64
	Lng          float64
	InsideFence  int
	RecordedAt   string
}, error) {
	// ... query regulatory_location_logs
}

// PatientsWithNoVerify returns patients with no verification > N hours
func (s *RegulatoryStore) PatientsWithNoVerify(hours int) ([]struct {
	ID              string
	Name            string
	AdmissionNo     string
	Department      string
	BedNo           string
	LastVerifyAt    string
	VerifyGapHours  int
	FenceStatus     string
}, error) {
	// ... query medical_wristband_patients where verify_gap_hours >= hours AND status = 'admitted'
}

// PatientAuditTrail returns all data for a single patient (穿透审计)
func (s *RegulatoryStore) PatientAuditTrail(patientID string) (map[string]interface{}, error) {
	// ... aggregate from:
	//   medical_wristband_patients
	//   medical_wristband_bindings
	//   medical_verifications
	//   medical_medications
	//   medical_expenses
	//   medical_daily_entries
	//   regulatory_location_logs
	//   regulatory_alerts
	// Returns a nested map: {"patient": {...}, "binding": {...}, "verifications": [...], ...}
}
```

- [ ] **Step 3: 编写 Router 层 — `router/regulatory_routes.go`**

```go
package router

import (
	"github.com/gin-gonic/gin"
	"eregen/admin-api/regulatory/handler"
)

// RegisterRoutes registers all regulatory API routes under /api/v1/regulatory
func RegisterRoutes(r *gin.Engine, h *handler.RegulatoryHandler) {
	reg := r.Group("/api/v1/regulatory")
	{
		// 在院总览
		reg.GET("/dashboard/patient-overview", h.DashboardOverview)
		reg.GET("/dashboard/patient-list", h.DashboardPatientList)

		// 异常告警
		reg.GET("/alerts", h.GetAlerts)
		reg.POST("/alerts/:id/acknowledge", h.AcknowledgeAlert)
		reg.POST("/alerts/:id/resolve", h.ResolveAlert)

		// 穿透审计
		reg.GET("/audit/patient/:id", h.PatientAudit)

		// 规则配置
		reg.GET("/rules", h.GetRules)
		reg.PUT("/rules/:code/config", h.UpdateRuleConfig)

		// 围栏配置
		reg.POST("/fence/config", h.CreateFenceConfig)
		reg.GET("/fence/config", h.GetFenceConfig)

		// 合规报表
		reg.GET("/compliance/report", h.ComplianceReport)
	}
}
```

- [ ] **Step 4: 编译验证**

```bash
cd cloud/admin-api && go build ./...
echo $?
```

预期输出：`0`（编译通过）

- [ ] **Step 5: Commit**

```bash
git add cloud/admin-api/regulatory/{router,store}
git commit -m "feat(regulatory): add module skeleton with router and store layer"
```

---

### Task 3: Handler 层 — 在院总览 + 异常告警

**Files:**
- Create: `cloud/admin-api/regulatory/handler/dashboard.go`
- Create: `cloud/admin-api/regulatory/handler/alert.go`

**Interfaces:**
- Consumes:
  - `store.RegulatoryStore.FenceConfig()`
  - `store.RegulatoryStore.PatientsWithNoVerify()`
  - `store.RegulatoryStore.LocationLogsByPatient()`
- Produces:
  - `GET /api/v1/regulatory/dashboard/patient-overview` → JSON 总览摘要
  - `GET /api/v1/regulatory/dashboard/patient-list` → JSON 患者列表（含围栏状态和告警）
  - `GET /api/v1/regulatory/alerts` → JSON 告警列表
  - `POST /api/v1/regulatory/alerts/:id/acknowledge` → 确认告警
  - `POST /api/v1/regulatory/alerts/:id/resolve` → 标记已解决

**步骤：**

- [ ] **Step 1: 编写 Dashboard Handler — `handler/dashboard.go`**

```go
package handler

import (
	"net/http"
	"strconv"
	"time"

	"eregen/admin-api/regulatory/service"
	"github.com/gin-gonic/gin"
)

type DashboardHandler struct {
	fenceSvc *service.FenceService
}

func NewDashboardHandler(fenceSvc *service.FenceService) *DashboardHandler {
	return &DashboardHandler{fenceSvc: fenceSvc}
}

// DashboardOverview returns real-time in-hospital patient summary
func (h *DashboardHandler) DashboardOverview(c *gin.Context) {
	hospitalID := c.Query("hospital_id")
	department := c.Query("department")

	// Query counts from existing medical_wristband_patients table
	// TODO: implement in store layer
	totalAdmitted := 0
	todayAdmit := 0
	todayDischarge := 0
	byDepartment := []gin.H{}
	fenceViolationsToday := 0
	noVerify24h := 0

	c.JSON(http.StatusOK, gin.H{
		"total_admitted":        totalAdmitted,
		"today_admit":           todayAdmit,
		"today_discharge":       todayDischarge,
		"by_department":         byDepartment,
		"fence_violations_today": fenceViolationsToday,
		"no_verify_24h":         noVerify24h,
	})
}

// DashboardPatientList returns paginated list of admitted patients with fence/alert status
func (h *DashboardHandler) DashboardPatientList(c *gin.Context) {
	department := c.Query("department")
	status := c.DefaultQuery("status", "admitted")
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	pageSize, _ := strconv.Atoi(c.DefaultQuery("page_size", "20"))

	if page < 1 {
		page = 1
	}
	if pageSize < 1 || pageSize > 100 {
		pageSize = 20
	}

	offset := (page - 1) * pageSize

	// Query patients with fence_status and alert info
	// TODO: implement in store layer
	patients := []gin.H{}
	total := 0

	c.JSON(http.StatusOK, gin.H{
		"patients": patients,
		"total":    total,
		"page":     page,
		"page_size": pageSize,
	})
}
```

- [ ] **Step 2: 编写 Alert Handler — `handler/alert.go`**

```go
package handler

import (
	"net/http"
	"time"

	"eregen/admin-api/regulatory/service"
	"github.com/gin-gonic/gin"
)

type AlertHandler struct {
	alertSvc *service.AlertService
}

func NewAlertHandler(alertSvc *service.AlertService) *AlertHandler {
	return &AlertHandler{alertSvc: alertSvc}
}

// GetAlerts returns paginated alert list with filters
func (h *AlertHandler) GetAlerts(c *gin.Context) {
	level := c.Query("level")
	ruleCode := c.Query("rule_code")
	department := c.Query("department")
	status := c.DefaultQuery("status", "pending")
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	pageSize, _ := strconv.Atoi(c.DefaultQuery("page_size", "20"))

	if page < 1 {
		page = 1
	}
	if pageSize < 1 || pageSize > 100 {
		pageSize = 20
	}
	offset := (page - 1) * pageSize

	alerts := []gin.H{}
	total := 0

	c.JSON(http.StatusOK, gin.H{
		"alerts": alerts,
		"total":  total,
		"page":   page,
		"page_size": pageSize,
	})
}

// AcknowledgeAlert marks an alert as acknowledged
func (h *AlertHandler) AcknowledgeAlert(c *gin.Context) {
	id := c.Param("id")
	userID := c.GetString("user_id") // from auth middleware

	// Update regulatory_alerts set status='acknowledged', acknowledged_at=now, acknowledged_by=user_id
	// where id=? AND status='pending'

	c.JSON(http.StatusOK, gin.H{"status": "acknowledged"})
}

// ResolveAlert marks an alert as resolved
func (h *AlertHandler) ResolveAlert(c *gin.Context) {
	id := c.Param("id")
	userID := c.GetString("user_id")
	var req struct {
		Notes string `json:"notes"`
	}
	c.ShouldBindJSON(&req)

	// Update regulatory_alerts set status='resolved', resolved_at=now, resolved_by=user_id, notes=?
	// where id=? AND status IN ('pending','acknowledged')

	c.JSON(http.StatusOK, gin.H{"status": "resolved"})
}
```

- [ ] **Step 3: 注册到主路由**

在 `cloud/admin-api/main.go`（或路由入口文件）中导入并注册：

```go
import "eregen/admin-api/regulatory/router"

// 在路由初始化后调用
router.RegisterRoutes(ginEngine, handlerInstance)
```

- [ ] **Step 4: Commit**

```bash
git add cloud/admin-api/regulatory/handler/
git commit -m "feat(regulatory): add dashboard and alert handlers"
```

---

### Task 4: Service 层 — 电子围栏 + 规则引擎

**Files:**
- Create: `cloud/admin-api/regulatory/service/fence_svc.go`
- Create: `cloud/admin-api/regulatory/service/engine_svc.go`

**Interfaces:**
- Consumes:
  - `store.RegulatoryStore.FenceConfig()`
  - `store.RegulatoryStore.LocationLogsByPatient()`
- Produces:
  - `FenceService.CalculateFence(patientLat, patientLng, hospitalID) (inside bool, distance float64)`
  - `RuleEngine.Run()` — 每 5 分钟执行一轮 8 条规则检测

**步骤：**

- [ ] **Step 1: 编写电子围栏服务 — `service/fence_svc.go`**

```go
package service

import (
	"math"
	"time"

	"eregen/admin-api/regulatory/store"
)

const earthRadius = 6371000.0 // meters

type FenceService struct {
	store *store.RegulatoryStore
}

func NewFenceService(st *store.RegulatoryStore) *FenceService {
	return &FenceService{store: st}
}

// CalculateFence checks if a location is within the hospital fence
func (s *FenceService) CalculateFence(lat, lng float64, hospitalID string) (inside bool, distance float64, err error) {
	cfg, err := s.store.FenceConfig(hospitalID)
	if err != nil {
		return false, 0, err
	}

	distance = haversineDistance(lat, lng, cfg.CenterLat, cfg.CenterLng)
	inside = distance <= float64(cfg.RadiusMeters)
	return inside, distance, nil
}

// haversineDistance computes distance between two GPS coordinates in meters
func haversineDistance(lat1, lng1, lat2, lng2 float64) float64 {
	dLat := (lat2 - lat1) * math.Pi / 180.0
	dLng := (lng2 - lng1) * math.Pi / 180.0
	la1 := lat1 * math.Pi / 180.0
	la2 := lat2 * math.Pi / 180.0

	a := math.Sin(dLat/2)*math.Sin(dLat/2) +
		math.Cos(la1)*math.Cos(la2)*
			math.Sin(dLng/2)*math.Sin(dLng/2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))
	return earthRadius * c
}

// ProcessLocationLog handles incoming location data from wristband
func (s *FenceService) ProcessLocationLog(patientID, deviceID, hospitalID string, lat, lng, accuracy float64) error {
	inside, _, err := s.CalculateFence(lat, lng, hospitalID)
	if err != nil {
		return err
	}

	// Insert into regulatory_location_logs
	// ...

	return nil
}
```

- [ ] **Step 2: 编写规则引擎 — `service/engine_svc.go`**

```go
package service

import (
	"time"

	"eregen/admin-api/regulatory/store"
)

type RuleEngine struct {
	store *store.RegulatoryStore
}

func NewRuleEngine(st *store.RegulatoryStore) *RuleEngine {
	return &RuleEngine{store: st}
}

// Run executes one round of all rule checks
func (e *RuleEngine) Run() {
	e.checkNoVerify()       // R01
	e.checkFenceViolation() // R02
	e.checkFakeAdmission()  // R03
	e.checkExpenseSpike()   // R04
	e.checkMedVerifyMatch() // R05
	e.checkFrequentTransfer()
	e.checkDeviceDisconnect()
	e.checkPostDischarge()
}

// Start begins periodic execution (every 5 minutes)
func (e *RuleEngine) Start() {
	go func() {
		ticker := time.NewTicker(5 * time.Minute)
		defer ticker.Stop()
		for range ticker.C {
			e.Run()
		}
	}()
}

func (e *RuleEngine) checkNoVerify() {
	// Query patients with verify_gap_hours >= 24 AND status = 'admitted'
	// For each, insert into regulatory_alerts with rule_code='R01', severity='high'
}

func (e *RuleEngine) checkFenceViolation() {
	// Query location_logs where inside_fence=0 AND recorded_at > now()-30min
	// For each, insert into regulatory_alerts with rule_code='R02', severity='high'
}

func (e *RuleEngine) checkFakeAdmission() {
	// Query bindings where bound_at > 48h ago AND no entries in medical_verifications
}

func (e *RuleEngine) checkExpenseSpike() {
	// Compare daily expense sum vs department average
}

func (e *RuleEngine) checkMedVerifyMatch() {
	// Compare medication records vs verification records
}

func (e *RuleEngine) checkFrequentTransfer() {
	// Count department changes per patient in last 7 days
}

func (e *RuleEngine) checkDeviceDisconnect() {
	// Check wristband_devices.last_seen > 2h ago
}

func (e *RuleEngine) checkPostDischarge() {
	// Check discharged patients still have active bindings
}
```

- [ ] **Step 3: 在 admin-api 启动时启动规则引擎**

在 `cloud/admin-api/main.go` 中：

```go
import "eregen/admin-api/regulatory/service"

// After DB connection is established
engine := service.NewRuleEngine(storeInstance)
engine.Start()
```

- [ ] **Step 4: Commit**

```bash
git add cloud/admin-api/regulatory/service/
git commit -m "feat(regulatory): add fence calculation and rule engine services"
```

---

### Task 5: Handler 层 — 穿透审计 + 规则配置 + 合规报表

**Files:**
- Create: `cloud/admin-api/regulatory/handler/audit.go`
- Create: `cloud/admin-api/regulatory/handler/rule_config.go`
- Create: `cloud/admin-api/regulatory/handler/compliance.go`

**Interfaces:**
- Consumes:
  - `store.RegulatoryStore.PatientAuditTrail()`
- Produces:
  - `GET /api/v1/regulatory/audit/patient/:id` → 全链路数据聚合
  - `GET /api/v1/regulatory/rules` → 规则列表
  - `PUT /api/v1/regulatory/rules/:code/config` → 更新规则
  - `GET /api/v1/regulatory/compliance/report` → 周期合规报表

**步骤：**

- [ ] **Step 1: 编写穿透审计 Handler — `handler/audit.go`**

```go
package handler

import (
	"net/http"

	"eregen/admin-api/regulatory/store"
	"github.com/gin-gonic/gin"
)

type AuditHandler struct {
	store *store.RegulatoryStore
}

func NewAuditHandler(st *store.RegulatoryStore) *AuditHandler {
	return &AuditHandler{store: st}
}

// PatientAudit returns full audit trail for a single patient
func (h *AuditHandler) PatientAudit(c *gin.Context) {
	patientID := c.Param("id")

	data, err := h.store.PatientAuditTrail(patientID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, data)
}
```

- [ ] **Step 2: 编写规则配置 Handler — `handler/rule_config.go`**

```go
package handler

import (
	"net/http"

	"eregen/admin-api/regulatory/store"
	"github.com/gin-gonic/gin"
)

type RuleConfigHandler struct {
	store *store.RegulatoryStore
}

func NewRuleConfigHandler(st *store.RegulatoryStore) *RuleConfigHandler {
	return &RuleConfigHandler{store: st}
}

// GetRules returns all rule configurations
func (h *RuleConfigHandler) GetRules(c *gin.Context) {
	// Query regulatory_alerts for distinct rule_code entries with latest config
	// Return: [{code, name, enabled, config}]
}

// UpdateRuleConfig updates a rule's threshold
func (h *RuleConfigHandler) UpdateRuleConfig(c *gin.Context) {
	code := c.Param("code")
	var req struct {
		Config map[string]interface{} `json:"config"`
	}
	c.ShouldBindJSON(&req)
	// Update rule config in regulatory_alerts or dedicated rule_config table
}
```

- [ ] **Step 3: 编写合规报表 Handler — `handler/compliance.go`**

```go
package handler

import (
	"net/http"
	"time"

	"eregen/admin-api/regulatory/store"
	"github.com/gin-gonic/gin"
)

type ComplianceHandler struct {
	store *store.RegulatoryStore
}

func NewComplianceHandler(st *store.RegulatoryStore) *ComplianceHandler {
	return &ComplianceHandler{store: st}
}

// ComplianceReport returns period compliance summary
func (h *ComplianceHandler) ComplianceReport(c *gin.Context) {
	hospitalID := c.Query("hospital_id")
	startDate := c.Query("start_date")
	endDate := c.Query("end_date")

	// Parse dates, default to last 30 days
	if startDate == "" {
		startDate = time.Now().AddDate(0, 0, -30).Format("2006-01-02")
	}
	if endDate == "" {
		endDate = time.Now().Format("2006-01-02")
	}

	// Aggregate: total_patients, avg_stay_days, fence_violations, no_verify_alerts,
	// expense_anomalies, med_verify_mismatch, compliance_rate
	// Department breakdown

	c.JSON(http.StatusOK, gin.H{
		"summary":              gin.H{},
		"department_breakdown": []gin.H{},
	})
}
```

- [ ] **Step 4: Commit**

```bash
git add cloud/admin-api/regulatory/handler/
git commit -m "feat(regulatory): add audit, rule config, and compliance handlers"
```

---

### Task 6: 前端 — 监管专区页面（Vue 3 + Element Plus）

**Files:**
- Create: `apps/admin-web/src/views/regulatory/Dashboard.vue`
- Create: `apps/admin-web/src/views/regulatory/Alerts.vue`
- Create: `apps/admin-web/src/views/regulatory/AuditDetail.vue`
- Create: `apps/admin-web/src/views/regulatory/RuleConfig.vue`
- Create: `apps/admin-web/src/views/regulatory/ComplianceReport.vue`
- Modify: `apps/admin-web/src/router/index.js`（新增监管专区路由）
- Modify: `apps/admin-web/src/layout/Sidebar.vue`（新增监管专区菜单项）

**Interfaces:**
- Consumes: Task 3-5 的 API 接口
- Produces: 5 个监管专区页面

**步骤：**

- [ ] **Step 1: 新增侧边栏菜单项**

在 `apps/admin-web/src/layout/Sidebar.vue` 中"医护工作站"下方添加：

```vue
<el-sub-menu index="regulatory">
  <template #title>
    <el-icon><Monitor /></el-icon>
    <span>监管专区</span>
  </template>
  <el-menu-item index="/regulatory/dashboard">在院总览</el-menu-item>
  <el-menu-item index="/regulatory/alerts">异常告警</el-menu-item>
  <el-menu-item index="/regulatory/audit">穿透审计</el-menu-item>
  <el-menu-item index="/regulatory/rules">规则配置</el-menu-item>
  <el-menu-item index="/regulatory/compliance">合规审查</el-menu-item>
</el-sub-menu>
```

- [ ] **Step 2: 新增路由配置**

在 `apps/admin-web/src/router/index.js` 中添加：

```javascript
{
  path: 'regulatory/dashboard',
  name: 'RegulatoryDashboard',
  component: () => import('@/views/regulatory/Dashboard.vue'),
  meta: { requiresRole: ['hospital_admin', 'regulator'] }
},
{
  path: 'regulatory/alerts',
  name: 'RegulatoryAlerts',
  component: () => import('@/views/regulatory/Alerts.vue'),
  meta: { requiresRole: ['hospital_admin', 'regulator', 'nurse'] }
},
{
  path: 'regulatory/audit/:id',
  name: 'RegulatoryAudit',
  component: () => import('@/views/regulatory/AuditDetail.vue'),
  meta: { requiresRole: ['hospital_admin', 'regulator'] }
},
{
  path: 'regulatory/rules',
  name: 'RegulatoryRules',
  component: () => import('@/views/regulatory/RuleConfig.vue'),
  meta: { requiresRole: ['hospital_admin', 'regulator'] }
},
{
  path: 'regulatory/compliance',
  name: 'RegulatoryCompliance',
  component: () => import('@/views/regulatory/ComplianceReport.vue'),
  meta: { requiresRole: ['hospital_admin', 'regulator'] }
}
```

- [ ] **Step 3: 编写在院总览页面 — `views/regulatory/Dashboard.vue`**

- 顶部统计卡片：在院总数、今日入院、今日出院、围栏违规数、无核验数
- 科室分布表格：科室名称 | 在院人数 | 告警数
- 在院患者列表：支持按科室筛选，显示患者姓名、住院号、床号、最近核验时间、围栏状态、触发告警
- 实时刷新：每 60 秒自动刷新

- [ ] **Step 4: 编写异常告警页面 — `views/regulatory/Alerts.vue`**

- 告警列表表格：规则名称 | 患者 | 科室 | 级别 | 触发时间 | 状态
- 筛选器：级别、规则编码、科室、状态
- 操作按钮：确认告警、标记已解决
- 颜色区分：高=红色、中=橙色、低=黄色

- [ ] **Step 5: 编写穿透审计页面 — `views/regulatory/AuditDetail.vue`**

- 患者基本信息卡片
- 时间线组件展示：入院→绑定→核验记录→用药→费用→每日录入→围栏日志→告警记录
- 可折叠面板按类别展开

- [ ] **Step 6: 编写规则配置页面 — `views/regulatory/RuleConfig.vue`**

- 规则列表表格：规则编码 | 规则名称 | 启用状态 | 阈值配置 | 操作
- 每个规则可编辑阈值（如挂床住院的 max_verify_gap_hours）
- 启用/禁用开关

- [ ] **Step 7: 编写合规报表页面 — `views/regulatory/ComplianceReport.vue`**

- 日期范围选择器（默认近 30 天）
- 汇总统计卡片：总患者数、平均住院天数、围栏违规数、无核验告警数、费用异常数、合规率
- 科室明细表格
- 导出按钮（CSV/Excel）

- [ ] **Step 8: Commit**

```bash
git add apps/admin-web/src/views/regulatory/
git add apps/admin-web/src/router/index.js
git add apps/admin-web/src/layout/Sidebar.vue
git commit -m "feat(admin): add regulatory专区 5 pages with role-based routing"
```

---

### Task 7: 基站定位数据接入 + 围栏计算集成

**Files:**
- Create: `cloud/admin-api/regulatory/service/location_processor.go`
- Modify: `cloud/admin-api/regulatory/service/fence_svc.go`（已有基础，补充集成）

**Interfaces:**
- Consumes:
  - MQTT 消息 `eregen/medical/wb/{dev_id}/location`
  - NATS 事件 `eregen.medical.wb.location`
- Produces:
  - 将基站 CID/TAC/LAC 转换为 lat/lng
  - 调用 `FenceService.CalculateFence()` 判断是否在围栏内
  - 写入 `regulatory_location_logs`

**步骤：**

- [ ] **Step 1: 编写基站坐标转换服务**

```go
package service

import "fmt"

type BaseStationDB struct {
	// MVP 阶段使用内置映射表，未来可替换为外部 API
	// Key: "TAC:CID" → Value: {Lat, Lng}
}

func (b *BaseStationDB) ConvertToCoords(tac, cid string) (float64, float64, error) {
	key := tac + ":" + cid
	// Query from a config file or database table
	// For MVP: read from a JSON config file
	// In production: query external base station coordinate API
	return 0, 0, fmt.Errorf("base station not found: %s", key)
}
```

- [ ] **Step 2: 编写位置消息处理器**

监听 MQTT/NATS 位置消息：

```go
package service

import (
	"encoding/json"
	"eregen/admin-api/regulatory/service"
)

type LocationMessage struct {
	DeviceID string  `json:"device_id"`
	PatientID string `json:"patient_id"`
	TAC      string  `json:"tac"`
	CID      string  `json:"cid"`
	LAT      float64 `json:"lat,omitempty"`   // 如果模组直接返回GPS坐标
	LNG      float64 `json:"lng,omitempty"`
	Accuracy float64 `json:"accuracy"`
	Timestamp string  `json:"timestamp"`
}

func (p *LocationProcessor) HandleLocation(msg LocationMessage) error {
	var lat, lng float64
	var err error

	if msg.LAT != 0 && msg.LNG != 0 {
		// 模组直接返回 GPS 坐标
		lat, lng = msg.LAT, msg.LNG
	} else {
		// 通过基站 CID/TAC 转换
		lat, lng, err = p.baseStationDB.ConvertToCoords(msg.TAC, msg.CID)
		if err != nil {
			return err
		}
	}

	// 计算围栏
	inside, _, err := p.fenceSvc.CalculateFence(lat, lng, msg.DeviceID)
	if err != nil {
		return err
	}

	// 写入 location_logs
	err = p.store.InsertLocationLog(msg.PatientID, msg.DeviceID, lat, lng, msg.Accuracy, inside)
	if err != nil {
		return err
	}

	// 如果越界，更新患者围栏状态
	if !inside {
		p.store.UpdatePatientFenceStatus(msg.PatientID, "outside", time.Now())
	} else {
		p.store.UpdatePatientFenceStatus(msg.PatientID, "inside", time.Time{})
	}

	return nil
}
```

- [ ] **Step 3: 注册 NATS 订阅**

在 `admin-api` 启动时注册 location 事件订阅：

```go
sub, err := natsConn.Subscribe("eregen.medical.wb.location", func(msg []byte) {
	var loc service.LocationMessage
	json.Unmarshal(msg, &loc)
	locationProcessor.HandleLocation(loc)
})
```

- [ ] **Step 4: Commit**

```bash
git add cloud/admin-api/regulatory/service/location_processor.go
git commit -m "feat(regulatory): add base station location processing and fence integration"
```

---

### Task 8: 角色权限扩展 + 测试 + 联调

**Files:**
- Modify: 现有 users 表（增加 role 枚举扩展）
- Modify: 现有认证中间件（增加 role 校验）
- Create: 监管模块单元测试
- Create: 端到端集成测试

**Interfaces:**
- Consumes: 所有前面的任务产出
- Produces: 完整的监管闭环系统

**步骤：**

- [ ] **Step 1: 扩展用户角色**

在现有 `users` 表中确保有 `role` 字段，枚举值包含：
`super_admin`, `hospital_admin`, `nurse`, `regulator`, `family_member`

如果护士需要科室限制，通过 `user_department_bindings` 表关联。

- [ ] **Step 2: 认证中间件增加角色校验**

在监管路由上挂载 RBAC 中间件：

```go
func RequireRoles(roles ...string) gin.HandlerFunc {
    return func(c *gin.Context) {
        userRole := c.GetString("role")
        allowed := false
        for _, r := range roles {
            if userRole == r {
                allowed = true
                break
            }
        }
        if !allowed {
            c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "insufficient permissions"})
            return
        }
        c.Next()
    }
}
```

各路由的权限要求：

| 路由 | 允许角色 |
|------|---------|
| `/dashboard/*` | hospital_admin, regulator |
| `/alerts` GET | hospital_admin, regulator, nurse |
| `/alerts/:id/acknowledge` | hospital_admin, regulator |
| `/alerts/:id/resolve` | hospital_admin, regulator |
| `/audit/*` | hospital_admin, regulator |
| `/rules/*` | hospital_admin, regulator |
| `/compliance/*` | hospital_admin, regulator |
| `/fence/config` | hospital_admin, regulator |

- [ ] **Step 3: 编写监管模块单元测试**

```go
// cloud/admin-api/regulatory/service/fence_svc_test.go
package service

import "testing"

func TestHaversineDistance(t *testing.T) {
	// Same point → 0
	dist := haversineDistance(30.5728, 104.0668, 30.5728, 104.0668)
	if dist != 0 {
		t.Errorf("expected 0, got %f", dist)
	}

	// Known distance ~111km (1 degree latitude)
	dist = haversineDistance(30.0, 104.0, 31.0, 104.0)
	expected := 111.0 * 1000.0 // ~111km
	if math.Abs(dist-expected) > 1000 {
		t.Errorf("expected ~%f, got %f", expected, dist)
	}
}

func TestCalculateFence(t *testing.T) {
	// Inside fence → true
	inside, _, _ := svc.CalculateFence(30.5728, 104.0668, "H001")
	if !inside {
		t.Error("expected inside=true")
	}

	// Outside fence → false
	inside, _, _ = svc.CalculateFence(30.6, 104.1, "H001")
	if inside {
		t.Error("expected inside=false")
	}
}
```

- [ ] **Step 4: 端到端联调测试**

测试场景清单：

| 场景 | 步骤 | 预期结果 |
|------|------|---------|
| 正常入院 | 登记→绑定腕带→写入→护士核验 | 患者出现在在院总览，围栏状态=inside |
| 挂床检测 | 模拟患者 24h 无核验 | R01 告警生成，出现在告警列表 |
| 围栏越界 | 模拟腕带位置超出围栏 | R02 告警生成 |
| 告警处理 | 确认→标记解决 | 告警状态流转正确 |
| 穿透审计 | 查看任意患者全链路 | 返回 patient+binding+verification+medication+expense+fence+alert |
| 角色隔离 | 用护士账号访问 `/regulatory/audit` | 403 Forbidden |
| 家属隐私 | 家属端查看用药/费用 | 仅简化版数据 |

- [ ] **Step 5: Commit**

```bash
git add cloud/admin-api/regulatory/service/*_test.go
git add cloud/admin-api/regulatory/store/sqlite.go
git commit -m "feat(regulatory): add unit tests and RBAC middleware"

git add .
git commit -m "chore: end-to-end integration testing and final polish"
```

---

## 实施批次与时间线

| 批次 | 任务 | 周期 | 交付物 |
|------|------|------|--------|
| 第一批 | Task 1-2 | 第 1 周 | 数据库就绪 + 模块骨架 |
| 第二批 | Task 3-4 | 第 2-3 周 | 围栏+告警 API + 规则引擎 |
| 第三批 | Task 5-6 | 第 4-5 周 | 审计+合规 API + 监管前端 5 页 |
| 第四批 | Task 7-8 | 第 6 周 | 基站定位集成 + 测试联调 |

---

## 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| 基站定位精度不足 | 围栏误判 | MVP 设置较大围栏半径（200-500m），后续升级 GPS |
| 规则引擎误报 | 告警疲劳 | 支持 false_positive 标记，积累数据优化阈值 |
| SQLite 并发查询性能 | 穿透审计 JOIN 慢 | MVP 限制并发用户数，未来切 PG |
| 角色权限泄露 | 护士看到其他科室数据 | RBAC 严格校验，每查询加 department 过滤 |

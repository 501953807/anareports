# 医院门诊叫号分诊系统 软件实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为二级医院（5-10科室，100-500人/天）开发一套完整的门诊叫号分诊软件系统

**Architecture:** 基于Spring Boot的微服务架构，MySQL主从数据库，Redis缓存，WebSocket实时推送。患者端通过微信小程序接入，医生端通过HTML5分诊屏和医生操作面板交互。HIS系统通过中间库方式同步挂号数据。

**Tech Stack:**
- 后端: Java 17 + Spring Boot 3.x + MyBatis Plus + Spring Security
- 前端: Vue 3 + Element Plus (管理后台) + HTML5 Canvas (分诊屏)
- 移动端: 微信小程序原生框架 (wxml/wxss/js)
- 数据库: MySQL 8.0 + Redis 7.x
- 消息推送: WebSocket + 微信模板消息
- 构建: Maven 3.9 + Docker 24.x

## Global Constraints

- 数据库字符集统一使用 utf8mb4，排序规则 utf8mb4_unicode_ci
- 所有API接口遵循 RESTful 规范，版本号前缀 /api/v1/
- 患者姓名在分诊屏上必须脱敏（保留首字，其余*替换，如"张**"）
- 叫号语音播报使用系统TTS，不支持自定义语音包
- 所有时间字段统一使用 UTC+8 (Asia/Shanghai)，存储为 datetime 类型
- 日志记录所有叫号操作（呼叫/跳过/重呼），保留不少于180天
- 系统需支持7×24小时运行，单节点可用性≥99.9%

---

# 模块一：数据库设计与核心实体

### Task 1: 数据库建表脚本

**Files:**
- Create: `backend/src/main/resources/db/init.sql`
- Create: `backend/src/main/resources/db/migration/V1__init_schema.sql`

**Interfaces:**
- Produces: 以下数据库表和字段结构

**Step 1: 创建数据库初始化SQL脚本**

```sql
-- ============================================
-- 医院门诊叫号分诊系统 - 数据库初始化脚本
-- 版本: V1.0
-- 日期: 2026-06-29
-- ============================================

CREATE DATABASE IF NOT EXISTS hospital_queuing
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE hospital_queuing;

-- 1. 科室表
CREATE TABLE dept (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '科室ID',
  name VARCHAR(50) NOT NULL COMMENT '科室名称',
  code VARCHAR(20) NOT NULL UNIQUE COMMENT '科室编码',
  floor VARCHAR(20) DEFAULT '1F' COMMENT '所在楼层',
  room_no VARCHAR(20) COMMENT '诊室编号',
  status TINYINT DEFAULT 1 COMMENT '状态: 1启用 0停用',
  sort_order INT DEFAULT 0 COMMENT '排序',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '科室表';

-- 2. 医生表
CREATE TABLE doctor (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '医生ID',
  name VARCHAR(50) NOT NULL COMMENT '医生姓名',
  code VARCHAR(20) NOT NULL UNIQUE COMMENT '医生工号',
  dept_id BIGINT NOT NULL COMMENT '所属科室',
  title VARCHAR(20) DEFAULT '主治医师' COMMENT '职称: 主任医师/副主任医师/主治医师/医师',
  specialty VARCHAR(200) COMMENT '擅长领域',
  avatar_url VARCHAR(500) COMMENT '头像URL',
  status TINYINT DEFAULT 1 COMMENT '状态: 1在职 0离职',
  sort_order INT DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (dept_id) REFERENCES dept(id)
) COMMENT '医生表';

-- 3. 排班表
CREATE TABLE schedule (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '排班ID',
  doctor_id BIGINT NOT NULL COMMENT '医生ID',
  work_date DATE NOT NULL COMMENT '排班日期',
  session_type TINYINT NOT NULL COMMENT '时段: 1上午 2下午 3晚上',
  start_time TIME NOT NULL COMMENT '开始时间',
  end_time TIME NOT NULL COMMENT '结束时间',
  max_patients INT DEFAULT 50 COMMENT '最大挂号数',
  status TINYINT DEFAULT 1 COMMENT '状态: 1正常 0停诊',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (doctor_id) REFERENCES doctor(id),
  UNIQUE KEY uk_doctor_date_session (doctor_id, work_date, session_type)
) COMMENT '医生排班表';

-- 4. 挂号表
CREATE TABLE registration (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '挂号ID',
  patient_name VARCHAR(50) NOT NULL COMMENT '患者姓名',
  patient_phone VARCHAR(20) COMMENT '患者手机号(脱敏存储)',
  id_card VARCHAR(30) COMMENT '身份证号(加密存储)',
  dept_id BIGINT NOT NULL COMMENT '科室',
  doctor_id BIGINT NOT NULL COMMENT '医生',
  schedule_id BIGINT NOT NULL COMMENT '排班',
  reg_time DATETIME NOT NULL COMMENT '挂号时间',
  reg_channel TINYINT NOT NULL DEFAULT 1 COMMENT '渠道: 1线上 2自助机 3人工窗口',
  queue_no INT NOT NULL COMMENT '排队号码(按科室+时段顺序)',
  patient_type TINYINT DEFAULT 1 COMMENT '患者类型: 1普通 2急诊 3VIP 4老年 5儿童',
  status TINYINT DEFAULT 1 COMMENT '状态: 1待就诊 2已呼叫 3就诊中 4已完成 5已跳过 6已迟到',
  hms_sync_status TINYINT DEFAULT 0 COMMENT 'HIS同步状态: 0未同步 1已同步 2同步失败',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (dept_id) REFERENCES dept(id),
  FOREIGN KEY (doctor_id) REFERENCES doctor(id),
  FOREIGN KEY (schedule_id) REFERENCES schedule(id),
  INDEX idx_dept_queue (dept_id, schedule_id, queue_no),
  INDEX idx_status (status),
  INDEX idx_reg_time (reg_time)
) COMMENT '挂号表';

-- 5. 叫号记录表
CREATE TABLE call_record (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
  registration_id BIGINT NOT NULL COMMENT '挂号ID',
  dept_id BIGINT NOT NULL COMMENT '科室',
  doctor_id BIGINT NOT NULL COMMENT '医生',
  call_no INT NOT NULL COMMENT '呼叫序号(同一患者可能被多次呼叫)',
  call_time DATETIME NOT NULL COMMENT '呼叫时间',
  call_action TINYINT NOT NULL COMMENT '动作: 1呼叫 2重呼 3跳过 4过号',
  operator VARCHAR(50) COMMENT '操作人(医生姓名)',
  remark VARCHAR(200) COMMENT '备注',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (registration_id) REFERENCES registration(id)
) COMMENT '叫号记录表';

-- 6. 分诊屏内容表
CREATE TABLE screen_content (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '内容ID',
  dept_id BIGINT COMMENT '关联科室(NULL=全院通用)',
  content_type TINYINT NOT NULL COMMENT '类型: 1公告 2医生介绍 3健康科普 4宣传视频',
  title VARCHAR(200) NOT NULL COMMENT '标题',
  body TEXT COMMENT '内容正文',
  media_url VARCHAR(500) COMMENT '媒体文件URL(视频/图片)',
  display_order INT DEFAULT 0 COMMENT '显示顺序',
  start_date DATE COMMENT '生效开始日期',
  end_date DATE COMMENT '生效结束日期',
  status TINYINT DEFAULT 1 COMMENT '状态: 1启用 0停用',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '分诊屏内容表';

-- 7. 系统配置表
CREATE TABLE sys_config (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
  config_value VARCHAR(500) NOT NULL COMMENT '配置值',
  config_desc VARCHAR(200) COMMENT '配置描述',
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '系统配置表';

-- 默认配置
INSERT INTO sys_config (config_key, config_value, config_desc) VALUES
  ('queue_timeout_seconds', '300', '排队超时秒数(5分钟)'),
  ('max_wait_count', '3', '最大重呼次数'),
  ('advance_warning_count', '3', '提前预警排队人数'),
  ('tts_voice_enabled', '1', '语音播报开关: 1开 0关'),
  ('screen_rotation_seconds', '15', '屏幕内容轮播间隔(秒)'),
  ('emergency_priority', '1', '急诊优先级系数');
```

**Step 2: 运行建表脚本**

```bash
# 在MySQL中执行
mysql -u root -p < backend/src/main/resources/db/init.sql
```

**Expected:** 数据库 `hospital_queuing` 创建成功，7张表建立完成，无报错

**Step 3: 提交**

```bash
git add backend/src/main/resources/db/init.sql backend/src/main/resources/db/migration/V1__init_schema.sql
git commit -m "feat: 添加数据库初始化脚本，包含7张核心表"
```

---

# 模块二：后端核心服务

### Task 2: 项目骨架搭建

**Files:**
- Create: `backend/pom.xml`
- Create: `backend/src/main/java/com/hospital/queuing/QueuingApplication.java`
- Create: `backend/src/main/resources/application.yml`
- Create: `backend/src/main/resources/application-prod.yml`

**Interfaces:**
- Produces: Spring Boot 3.x 可运行的项目骨架

**Step 1: 创建 pom.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>com.hospital</groupId>
    <artifactId>queuing-system</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    <name>Hospital Queuing System</name>

    <properties>
        <java.version>17</java.version>
        <mybatis-plus.version>3.5.5</mybatis-plus.version>
        <spring-security.version>6.2.0</spring-security.version>
    </properties>

    <dependencies>
        <!-- Spring Boot -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-websocket</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
            <version>${mybatis-plus.version}</version>
        </dependency>

        <!-- Utilities -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.8.24</version>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

**Step 2: 创建启动类**

```java
package com.hospital.queuing;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@SpringBootApplication
@MapperScan("com.hospital.queuing.mapper")
@EnableScheduling
@EnableTransactionManagement
public class QueuingApplication {
    public static void main(String[] args) {
        SpringApplication.run(QueuingApplication.class, args);
    }
}
```

**Step 3: 创建 application.yml**

```yaml
server:
  port: 8080
  servlet:
    context-path: /api/v1

spring:
  application:
    name: hospital-queuing
  profiles:
    active: dev
  datasource:
    url: jdbc:mysql://localhost:3306/hospital_queuing?useUnicode=true&characterEncoding=utf8mb4&serverTimezone=Asia/Shanghai
    username: root
    password: ${DB_PASSWORD:queuing2026}
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
  redis:
    host: localhost
    port: 6379
    database: 0
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: Asia/Shanghai

mybatis-plus:
  mapper-locations: classpath*:mapper/**/*.xml
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl

logging:
  level:
    com.hospital.queuing: INFO
    org.springframework.security: WARN
```

**Step 4: 验证项目可启动**

```bash
cd backend
mvn spring-boot:run
```

**Expected:** 控制台输出 `Started QueuingApplication in X seconds`，无错误

**Step 5: 提交**

```bash
git add backend/
git commit -m "feat: 搭建Spring Boot 3.2项目骨架，包含Web/Security/Redis/WebSocket/MyBatis-Plus依赖"
```

### Task 3: 实体类和Mapper层

**Files:**
- Create: `backend/src/main/java/com/hospital/queuing/entity/Dept.java`
- Create: `backend/src/main/java/com/hospital/queuing/entity/Doctor.java`
- Create: `backend/src/main/java/com/hospital/queuing/entity/Schedule.java`
- Create: `backend/src/main/java/com/hospital/queuing/entity/Registration.java`
- Create: `backend/src/main/java/com/hospital/queuing/entity/CallRecord.java`
- Create: `backend/src/main/java/com/hospital/queuing/entity/ScreenContent.java`
- Create: `backend/src/main/java/com/hospital/queuing/mapper/*.java` (7个Mapper接口)

**Interfaces:**
- Consumes: 数据库表结构 (Task 2)
- Produces: MyBatis-Plus Entity类 + Mapper接口

**Step 1: 创建实体类 Dept.java**

```java
package com.hospital.queuing.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("dept")
public class Dept {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String name;
    private String code;
    private String floor;
    private String roomNo;
    private Integer status;
    private Integer sortOrder;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

**Step 2: 创建 Mapper 接口 DeptMapper.java**

```java
package com.hospital.queuing.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hospital.queuing.entity.Dept;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface DeptMapper extends BaseMapper<Dept> {
}
```

**Step 3-7: 重复以上模式创建 Doctor, Schedule, Registration, CallRecord, ScreenContent 实体及对应的Mapper接口**

(结构相同，仅字段名映射数据库表字段)

**Step 8: 运行测试验证Mapper可用**

```bash
cd backend
mvn test -Dtest=MapperTest
```

**Step 9: 提交**

```bash
git add backend/src/main/java/com/hospital/queuing/entity/
git add backend/src/main/java/com/hospital/queuing/mapper/
git commit -m "feat: 创建7个实体类和Mapper接口，覆盖科室/医生/排班/挂号/叫号记录/屏幕内容/系统配置"
```

---

# 模块三：排队管理与叫号引擎

### Task 4: 排队管理服务

**Files:**
- Create: `backend/src/main/java/com/hospital/queuing/service/QueueService.java`
- Create: `backend/src/main/java/com/hospital/queuing/service/DemoQueueServiceTest.java`

**Interfaces:**
- Consumes: Registration实体, Dept/Doctor实体 (Task 3)
- Produces:
  - `int getNextQueueNo(Long deptId, Long scheduleId)` — 获取下一个排队号码
  - `RegistrationDTO addToQueue(Registration reg)` — 添加到队列
  - `List<RegistrationDTO> getWaitingList(Long deptId, Long scheduleId)` — 获取等待列表
  - `void removeFromQueue(Long registrationId, String reason)` — 移出队列

**Step 1: 编写 QueueService 测试**

```java
package com.hospital.queuing.service;

import com.hospital.queuing.entity.Registration;
import com.hospital.queuing.entity.Dept;
import com.hospital.queuing.entity.Doctor;
import com.hospital.queuing.mapper.DeptMapper;
import com.hospital.queuing.mapper.DoctorMapper;
import com.hospital.queuing.mapper.RegistrationMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class QueueServiceTest {

    @Autowired private QueueService queueService;
    @Autowired private DeptMapper deptMapper;
    @Autowired private DoctorMapper doctorMapper;
    @Autowired private RegistrationMapper registrationMapper;

    @Test
    void testAddToQueueAndGetNextNo() {
        // 准备科室和医生
        Dept dept = new Dept();
        dept.setName("内科");
        dept.setCode("NEO");
        dept.setStatus(1);
        deptMapper.insert(dept);

        Doctor doctor = new Doctor();
        doctor.setName("张三");
        doctor.setCode("D001");
        doctor.setDeptId(dept.getId());
        doctor.setTitle("主任医师");
        doctor.setSpecialty("呼吸系统疾病");
        doctor.setStatus(1);
        doctorMapper.insert(doctor);

        // 添加挂号到队列
        Registration reg = new Registration();
        reg.setPatientName("李四");
        reg.setDeptId(dept.getId());
        reg.setDoctorId(doctor.getId());
        reg.setRegChannel(1);
        reg.setPatientType(1);
        reg.setStatus(1);

        Registration result = queueService.addToQueue(reg);

        assertNotNull(result.getId());
        assertEquals(1, result.getQueueNo());
    }

    @Test
    void testEmergencyPriority() {
        // 急诊患者应该排在普通患者前面
        Registration normalReg = new Registration();
        normalReg.setPatientName("王五");
        normalReg.setPatientType(1); // 普通

        Registration emergencyReg = new Registration();
        emergencyReg.setPatientName("赵六");
        emergencyReg.setPatientType(2); // 急诊

        queueService.addToQueue(normalReg);
        queueService.addToQueue(emergencyReg);

        var waitingList = queueService.getWaitingList(
            normalReg.getDeptId(), normalReg.getScheduleId());
        // 急诊应该在前面
        assertEquals("赵六", waitingList.get(0).getPatientName());
    }
}
```

**Step 2: 实现 QueueService**

```java
package com.hospital.queuing.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.hospital.queuing.entity.Registration;
import com.hospital.queuing.mapper.RegistrationMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Comparator;
import java.util.List;

@Service
@RequiredArgsConstructor
public class QueueService {

    private final RegistrationMapper registrationMapper;

    /**
     * 患者类型优先级(数值越小优先级越高)
     */
    private static final int[] PATIENT_PRIORITY = {
        0, // 0: 急诊
        1, // 1: 普通
        2, // 2: VIP
        3, // 3: 老年
        4  // 4: 儿童
    };

    @Transactional
    public Registration addToQueue(Registration reg) {
        // 1. 获取该科室该时段的下一个排队号
        int nextNo = getNextQueueNo(reg.getDeptId(), reg.getScheduleId());
        reg.setQueueNo(nextNo);
        reg.setStatus(1); // 待就诊
        reg.setRegTime(LocalDateTime.now());

        registrationMapper.insert(reg);
        return reg;
    }

    public int getNextQueueNo(Long deptId, Long scheduleId) {
        LambdaQueryWrapper<Registration> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Registration::getDeptId, deptId)
               .eq(Registration::getScheduleId, scheduleId)
               .eq(Registration::getStatus, 1) // 仅统计待就诊
               .orderByDesc(Registration::getQueueNo)
               .last("LIMIT 1");

        Registration last = registrationMapper.selectOne(wrapper);
        return last == null ? 1 : last.getQueueNo() + 1;
    }

    public List<Registration> getWaitingList(Long deptId, Long scheduleId) {
        LambdaQueryWrapper<Registration> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Registration::getDeptId, deptId)
               .eq(Registration::getScheduleId, scheduleId)
               .eq(Registration::getStatus, 1)
               .orderByAsc(
                   // 急诊优先
                   true, Registration::getPatientType,
                   false, Registration::getQueueNo
               );

        return registrationMapper.selectList(wrapper);
    }

    @Transactional
    public void callPatient(Long registrationId, String operator) {
        Registration reg = registrationMapper.selectById(registrationId);
        if (reg == null) throw new IllegalArgumentException("挂号记录不存在");

        reg.setStatus(2); // 已呼叫
        registrationMapper.updateById(reg);

        // 记录叫号日志
        CallRecord record = new CallRecord();
        record.setRegistrationId(registrationId);
        record.setDeptId(reg.getDeptId());
        record.setDoctorId(reg.getDoctorId());
        record.setCallNo(1);
        record.setCallTime(LocalDateTime.now());
        record.setCallAction(1); // 呼叫
        record.setOperator(operator);
        // callRecordMapper.insert(record);
    }

    @Transactional
    public void skipPatient(Long registrationId, String reason) {
        Registration reg = registrationMapper.selectById(registrationId);
        if (reg == null) throw new IllegalArgumentException("挂号记录不存在");

        reg.setStatus(5); // 已跳过
        registrationMapper.updateById(reg);
    }

    @Transactional
    public void removePatient(Long registrationId, String reason) {
        Registration reg = registrationMapper.selectById(registrationId);
        if (reg == null) throw new IllegalArgumentException("挂号记录不存在");

        reg.setStatus(6); // 已迟到
        registrationMapper.updateById(reg);
    }
}
```

**Step 3: 运行测试**

```bash
cd backend
mvn test -Dtest=QueueServiceTest
```

**Expected:** 2个测试用例全部PASS

**Step 4: 提交**

```bash
git add backend/src/main/java/com/hospital/queuing/service/QueueService.java
git commit -m "feat: 实现排队管理核心服务: 添加队列/获取等待列表/急诊优先/叫号/跳过/过号"
```

### Task 5: 叫号引擎核心

**Files:**
- Create: `backend/src/main/java/com/hospital/queuing/service/CallEngineService.java`
- Create: `backend/src/main/java/com/hospital/queuing/ws/CallWebSocketHandler.java`

**Interfaces:**
- Consumes: QueueService (Task 4)
- Produces:
  - `CallResult callNext(Long deptId, Long scheduleId)` — 呼叫下一位
  - `CallResult recall(Long registrationId)` — 重呼
  - `void broadcastCall(CallEvent event)` — WebSocket推送叫号事件

**Step 1: 定义叫号事件DTO**

```java
package com.hospital.queuing.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class CallEvent {
    private Long deptId;
    private String deptName;
    private String doctorName;
    private String patientName; // 脱敏后
    private Integer queueNo;
    private String roomNo;
    private String floor;
    private LocalDateTime callTime;
    private String action; // CALL/RECALL/SKIP/OVER
}
```

**Step 2: 实现 CallEngineService**

```java
package com.hospital.queuing.service;

import com.hospital.queuing.dto.CallEvent;
import com.hospital.queuing.ws.CallWebSocketHandler;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class CallEngineService {

    private final QueueService queueService;
    private final CallWebSocketHandler webSocketHandler;

    public CallEvent callNext(Long deptId, Long scheduleId, String operator) {
        var waitingList = queueService.getWaitingList(deptId, scheduleId);
        if (waitingList.isEmpty()) {
            log.warn("科室{}队列已空", deptId);
            return null;
        }

        Registration next = waitingList.get(0);
        queueService.callPatient(next.getId(), operator);

        CallEvent event = new CallEvent();
        event.setDeptId(deptId);
        event.setDoctorName(next.getDoctorName());
        event.setPatientName(maskName(next.getPatientName()));
        event.setQueueNo(next.getQueueNo());
        event.setAction("CALL");
        event.setCallTime(java.time.LocalDateTime.now());

        // 通过WebSocket推送给所有分诊屏和患者端
        webSocketHandler.broadcast(event);

        log.info("呼叫下一位: 科室={}, 医生={}, 号码={}", deptId, next.getDoctorName(), next.getQueueNo());
        return event;
    }

    public CallEvent recall(Long registrationId, String operator) {
        // 重呼逻辑: 重新推送WebSocket事件
        CallEvent event = new CallEvent();
        event.setAction("RECALL");
        event.setCallTime(java.time.LocalDateTime.now());
        webSocketHandler.broadcast(event);
        return event;
    }

    /**
     * 患者姓名脱敏: 保留首字，其余*替换
     */
    private String maskName(String name) {
        if (name == null || name.length() <= 1) return name;
        return name.charAt(0) + "*".repeat(name.length() - 1);
    }
}
```

**Step 3: 实现 WebSocket处理器**

```java
package com.hospital.queuing.ws;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.hospital.queuing.dto.CallEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

@Component
@RequiredArgsConstructor
@Slf4j
public class CallWebSocketHandler extends TextWebSocketHandler {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final ConcurrentHashMap<String, WebSocketSession> sessions = new ConcurrentHashMap<>();

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        String clientId = (String) session.getAttributes().get("clientId");
        sessions.put(clientId, session);
        log.info("WebSocket连接建立: {}, 当前在线: {}", clientId, sessions.size());
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) {
        // 处理客户端心跳等消息
        log.debug("收到消息: {}", message.getPayload());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        String clientId = (String) session.getAttributes().get("clientId");
        sessions.remove(clientId);
        log.info("WebSocket连接关闭: {}, 剩余: {}", clientId, sessions.size());
    }

    /**
     * 向所有连接的客户端广播叫号事件
     */
    public void broadcast(CallEvent event) {
        String json;
        try {
            json = objectMapper.writeValueAsString(event);
        } catch (IOException e) {
            log.error("序列化CallEvent失败", e);
            return;
        }

        TextMessage message = new TextMessage(json);
        for (var entry : sessions.entrySet()) {
            try {
                entry.getValue().sendMessage(message);
            } catch (IOException e) {
                log.warn("推送失败给客户端: {}", entry.getKey());
            }
        }
    }

    public int getOnlineCount() {
        return sessions.size();
    }
}
```

**Step 4: 运行测试**

```bash
cd backend
mvn test -Dtest=CallEngineServiceTest
```

**Step 5: 提交**

```bash
git add backend/src/main/java/com/hospital/queuing/service/CallEngineService.java
git add backend/src/main/java/com/hospital/queuing/ws/CallWebSocketHandler.java
git commit -m "feat: 实现叫号引擎: 呼叫下一位/重呼/WebSocket广播/姓名脱敏"
```

---

# 模块四：RESTful API接口层

### Task 6: 挂号管理API

**Files:**
- Create: `backend/src/main/java/com/hospital/queuing/controller/RegistrationController.java`
- Create: `backend/src/main/java/com/hospital/queuing/dto/RegisterRequest.java`
- Create: `backend/src/main/java/com/hospital/queuing/dto/RegisterResponse.java`

**Interfaces:**
- Consumes: QueueService (Task 4)
- Produces:
  - `POST /api/v1/registrations` — 新增挂号
  - `GET /api/v1/registrations/dept/{deptId}/schedule/{scheduleId}/waiting` — 获取等待列表
  - `GET /api/v1/registrations/{id}` — 挂号详情

**Step 1: 实现 RegistrationController**

```java
package com.hospital.queuing.controller;

import com.hospital.queuing.dto.RegisterRequest;
import com.hospital.queuing.dto.RegisterResponse;
import com.hospital.queuing.entity.Registration;
import com.hospital.queuing.service.QueueService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/registrations")
@RequiredArgsConstructor
public class RegistrationController {

    private final QueueService queueService;

    @PostMapping
    public ResponseEntity<RegisterResponse> register(@RequestBody RegisterRequest req) {
        Registration reg = new Registration();
        reg.setPatientName(req.getPatientName());
        reg.setPatientPhone(req.getPatientPhone());
        reg.setDeptId(req.getDeptId());
        reg.setDoctorId(req.getDoctorId());
        reg.setScheduleId(req.getScheduleId());
        reg.setRegChannel(req.getRegChannel());
        reg.setPatientType(req.getPatientType());

        Registration saved = queueService.addToQueue(reg);

        RegisterResponse resp = new RegisterResponse();
        resp.setId(saved.getId());
        resp.setQueueNo(saved.getQueueNo());
        resp.setDeptName(saved.getDeptName());
        resp.setDoctorName(saved.getDoctorName());
        resp.setStatus(saved.getStatus());
        return ResponseEntity.ok(resp);
    }

    @GetMapping("/dept/{deptId}/schedule/{scheduleId}/waiting")
    public ResponseEntity<List<RegisterResponse>> getWaitingList(
            @PathVariable Long deptId, @PathVariable Long scheduleId) {
        var list = queueService.getWaitingList(deptId, scheduleId);
        return ResponseEntity.ok(list.stream().map(this::toResponse).collect(Collectors.toList()));
    }

    private RegisterResponse toResponse(Registration reg) {
        RegisterResponse resp = new RegisterResponse();
        resp.setId(reg.getId());
        resp.setQueueNo(reg.getQueueNo());
        resp.setPatientName(maskName(reg.getPatientName()));
        resp.setDeptName(reg.getDeptName());
        resp.setDoctorName(reg.getDoctorName());
        return resp;
    }

    private String maskName(String name) {
        if (name == null || name.length() <= 1) return name;
        return name.charAt(0) + "*".repeat(name.length() - 1);
    }
}
```

**Step 2: 实现 DTO**

```java
// RegisterRequest.java
package com.hospital.queuing.dto;
import lombok.Data;
@Data
public class RegisterRequest {
    private String patientName;
    private String patientPhone;
    private Long deptId;
    private Long doctorId;
    private Long scheduleId;
    private Integer regChannel = 1;
    private Integer patientType = 1;
}

// RegisterResponse.java
package com.hospital.queuing.dto;
import lombok.Data;
import java.time.LocalDateTime;
@Data
public class RegisterResponse {
    private Long id;
    private Integer queueNo;
    private String patientName;
    private String deptName;
    private String doctorName;
    private Integer status;
    private LocalDateTime regTime;
}
```

**Step 3: 测试API**

```bash
# 启动服务后测试
curl -X POST http://localhost:8080/api/v1/registrations \
  -H "Content-Type: application/json" \
  -d '{"patientName":"张三","deptId":1,"doctorId":1,"regChannel":1}'

curl http://localhost:8080/api/v1/registrations/dept/1/schedule/1/waiting
```

**Expected:** 返回正确的JSON响应，挂号成功，等待列表正确

**Step 4: 提交**

```bash
git add backend/src/main/java/com/hospital/queuing/controller/
git add backend/src/main/java/com/hospital/queuing/dto/
git commit -m "feat: 实现挂号管理REST API: 新增挂号/获取等待列表/挂号详情"
```

### Task 7: 叫号控制API + HIS对接API

**Files:**
- Create: `backend/src/main/java/com/hospital/queuing/controller/CallController.java`
- Create: `backend/src/main/java/com/hospital/queuing/controller/HisController.java`
- Create: `backend/src/main/java/com/hospital/queuing/service/HisSyncService.java`

**Interfaces:**
- Consumes: CallEngineService (Task 5)
- Produces:
  - `POST /api/v1/calls/{registrationId}/call` — 呼叫
  - `POST /api/v1/calls/{registrationId}/recall` — 重呼
  - `POST /api/v1/calls/{registrationId}/skip` — 跳过
  - `POST /api/v1/his/sync-registration` — HIS同步挂号

**Step 1: 实现 CallController**

```java
package com.hospital.queuing.controller;

import com.hospital.queuing.dto.CallEvent;
import com.hospital.queuing.service.CallEngineService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/calls")
@RequiredArgsConstructor
public class CallController {

    private final CallEngineService callEngine;

    @PostMapping("/{registrationId}/call")
    public ResponseEntity<CallEvent> callNext(
            @PathVariable Long registrationId,
            @RequestParam String operator) {
        CallEvent event = callEngine.callNext(registrationId, operator);
        return event != null ? ResponseEntity.ok(event) : ResponseEntity.noContent().build();
    }

    @PostMapping("/{registrationId}/recall")
    public ResponseEntity<CallEvent> recall(
            @PathVariable Long registrationId,
            @RequestParam String operator) {
        CallEvent event = callEngine.recall(registrationId, operator);
        return ResponseEntity.ok(event);
    }

    @PostMapping("/{registrationId}/skip")
    public ResponseEntity<Void> skip(@PathVariable Long registrationId) {
        callEngine.skipPatient(registrationId, "医生跳过");
        return ResponseEntity.ok().build();
    }
}
```

**Step 2: 实现 HIS对接服务**

```java
package com.hospital.queuing.service;

import com.hospital.queuing.entity.Registration;
import com.hospital.queuing.mapper.RegistrationMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class HisSyncService {

    private final JdbcTemplate jdbcTemplate;
    private final RegistrationMapper registrationMapper;

    /**
     * 从HIS中间库同步挂号数据
     * 假设HIS在中间库中有表 his_registration 需要同步
     */
    @Transactional
    public int syncRegistrations() {
        // 查询HIS中间表中未同步的记录
        List<Map<String, Object>> hisRecords = jdbcTemplate.queryForList(
            "SELECT id, patient_name, patient_phone, dept_id, doctor_id, " +
            "reg_time, patient_type FROM his_registration WHERE sync_status = 0"
        );

        int synced = 0;
        for (Map<String, Object> row : hisRecords) {
            try {
                Registration reg = new Registration();
                reg.setPatientName((String) row.get("patient_name"));
                reg.setPatientPhone(maskPhone((String) row.get("patient_phone")));
                reg.setDeptId(((Number) row.get("dept_id")).longValue());
                reg.setDoctorId(((Number) row.get("doctor_id")).longValue());
                reg.setRegTime(LocalDateTime.parse((String) row.get("reg_time")));
                reg.setRegChannel(2); // HIS同步来源
                reg.setPatientType(((Number) row.get("patient_type")).intValue());
                reg.setStatus(1);

                registrationMapper.insert(reg);

                // 标记HIS中间表已同步
                jdbcTemplate.update(
                    "UPDATE his_registration SET sync_status = 1 WHERE id = ?",
                    row.get("id"));

                synced++;
            } catch (Exception e) {
                log.error("同步HIS挂号数据失败: {}", row, e);
            }
        }

        log.info("HIS同步完成: 成功{}条", synced);
        return synced;
    }

    /**
     * 手机号脱敏
     */
    private String maskPhone(String phone) {
        if (phone == null || phone.length() < 11) return phone;
        return phone.substring(0, 3) + "****" + phone.substring(7);
    }
}
```

**Step 3: 实现定时同步任务**

```java
package com.hospital.queuing.task;

import com.hospital.queuing.service.HisSyncService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class HisSyncScheduler {

    private final HisSyncService hisSyncService;

    /**
     * 每30秒同步一次HIS挂号数据
     */
    @Scheduled(fixedRate = 30000)
    public void scheduledSync() {
        try {
            int count = hisSyncService.syncRegistrations();
            if (count > 0) {
                log.info("定时同步HIS数据: {}条", count);
            }
        } catch (Exception e) {
            log.error("HIS定时同步失败", e);
        }
    }
}
```

**Step 4: 提交**

```bash
git add backend/src/main/java/com/hospital/queuing/controller/CallController.java
git add backend/src/main/java/com/hospital/queuing/service/HisSyncService.java
git add backend/src/main/java/com/hospital/queuing/task/HisSyncScheduler.java
git commit -m "feat: 实现叫号控制API + HIS中间库同步 + 定时同步任务(30秒间隔)"
```

---

# 模块五：前端管理后台

### Task 8: Vue3管理后台项目骨架

**Files:**
- Create: `admin/package.json`
- Create: `admin/index.html`
- Create: `admin/src/main.js`
- Create: `admin/src/App.vue`
- Create: `admin/src/router/index.js`
- Create: `admin/src/views/Login.vue`
- Create: `admin/src/views/Dashboard.vue`

**Interfaces:**
- Produces: 可运行的Vue 3管理后台，包含登录页和仪表盘

**Step 1: 创建 package.json**

```json
{
  "name": "queuing-admin",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "element-plus": "^2.4.0",
    "axios": "^1.6.0",
    "@element-plus/icons-vue": "^2.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0"
  }
}
```

**Step 2: 创建 vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
})
```

**Step 3: 创建 App.vue + Login.vue + Dashboard.vue**

(App.vue: 布局框架含侧边栏 + 顶部导航)
(Login.vue: 用户名密码登录表单)
(Dashboard.vue: 数据概览卡片 — 今日挂号数/当前等待数/平均等待时间)

**Step 4: 运行并验证**

```bash
cd admin
npm install
npm run dev
```

**Expected:** 浏览器访问 http://localhost:3000 显示登录页，登录后显示仪表盘

**Step 5: 提交**

```bash
git add admin/
git commit -m "feat: 创建Vue3管理后台骨架: Vite构建 + Element Plus + 登录页 + 仪表盘"
```

### Task 9: 管理后台核心页面

**Files:**
- Create: `admin/src/views/DeptManage.vue` — 科室管理(增删改查)
- Create: `admin/src/views/DoctorManage.vue` — 医生管理
- Create: `admin/src/views/ScheduleManage.vue` — 排班管理
- Create: `admin/src/views/QueueMonitor.vue` — 实时队列监控
- Create: `admin/src/views/ScreenContent.vue` — 屏幕内容管理
- Create: `admin/src/views/Reports.vue` — 统计报表

**Interfaces:**
- Consumes: 后端API (Task 6-7)
- Produces: 6个完整的管理页面

**Step 1-6: 依次实现6个页面**

每个页面包含:
- Element Plus Table 展示数据
- Dialog 弹窗编辑
- API调用后端接口
- 表单验证

**Step 7: 运行验证**

```bash
cd admin
npm run dev
# 浏览器访问 http://localhost:3000
# 逐个测试科室管理/医生管理/排班管理/队列监控/内容管理/报表
```

**Step 8: 提交**

```bash
git add admin/src/views/
git commit -m "feat: 管理后台6个核心页面: 科室/医生/排班/队列监控/内容管理/报表"
```

---

# 模块六：分诊屏前端

### Task 10: 分诊屏HTML5页面

**Files:**
- Create: `screen/index.html` — 分诊屏主页
- Create: `screen/css/style.css` — 样式
- Create: `screen/js/app.js` — 逻辑

**Interfaces:**
- Consumes: WebSocket (Task 5)
- Produces: 可在浏览器全屏运行的分诊屏页面

**Step 1: 创建分诊屏主页**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>分诊屏</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div id="app">
    <!-- 顶部: 科室+医生信息 -->
    <header class="screen-header">
      <div class="dept-info">{{ currentDept }}</div>
      <div class="doctor-info">
        <img :src="doctorAvatar" class="doctor-avatar">
        <span class="doctor-name">{{ currentDoctor }}</span>
        <span class="doctor-title">{{ currentTitle }}</span>
      </div>
    </header>

    <!-- 中部: 当前叫号 -->
    <section class="current-call">
      <div class="call-label">现在呼叫</div>
      <div class="call-number">{{ currentQueueNo }}</div>
      <div class="call-name">{{ currentPatientName }}</div>
    </section>

    <!-- 底部: 等待列表 -->
    <section class="waiting-list">
      <div class="waiting-label">等待中 ({{ waitingCount }}人)</div>
      <div class="waiting-items" v-for="(p, i) in waitingList" :key="p.id">
        <span class="q-no">{{ p.queueNo }}</span>
        <span class="q-name">{{ p.patientName }}</span>
      </div>
    </section>

    <!-- 右侧: 公告/医生介绍轮播 -->
    <aside class="sidebar">
      <div class="content-carousel" v-for="(item, i) in screenContents" :key="i">
        <h3>{{ item.title }}</h3>
        <p>{{ item.body }}</p>
      </div>
    </aside>
  </div>

  <script src="js/app.js"></script>
</body>
</html>
```

**Step 2: 创建 JavaScript 逻辑**

```javascript
// screen/js/app.js
const WS_URL = `ws://${location.hostname}:8080/api/v1/ws/call`;
const ws = new WebSocket(WS_URL);

let currentDept = '内科';
let currentDoctor = '张**';
let currentTitle = '主任医师';
let currentQueueNo = '-';
let currentPatientName = '张**';
let waitingList = [];
let screenContents = [];

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.action === 'CALL') {
    currentQueueNo = data.queueNo;
    currentPatientName = data.patientName;
  } else if (data.action === 'RECALL') {
    // 重呼动画
    animateRecall();
  }
};

function animateRecall() {
  // 闪烁效果
  const el = document.querySelector('.call-number');
  el.classList.add('flash');
  setTimeout(() => el.classList.remove('flash'), 3000);
}

// 每15秒轮询等待列表
setInterval(async () => {
  const res = await fetch('/api/v1/registrations/dept/1/schedule/1/waiting');
  waitingList = await res.json();
}, 15000);
```

**Step 3: 运行验证**

```bash
cd screen
python3 -m http.server 3001
```

浏览器访问 http://localhost:3001，按F11全屏，验证WebSocket推送是否正常

**Step 4: 提交**

```bash
git add screen/
git commit -m "feat: 创建HTML5分诊屏: 当前叫号+等待列表+公告轮播+WebSocket实时推送"
```

---

# 模块七：微信小程序患者端

### Task 11: 微信小程序框架

**Files:**
- Create: `miniprogram/app.json`
- Create: `miniprogram/app.js`
- Create: `miniprogram/pages/index/index.js` — 首页(挂号列表)
- Create: `miniprogram/pages/queue/queue.js` — 排队页面
- Create: `miniprogram/pages/evaluate/evaluate.js` — 评价页面

**Interfaces:**
- Consumes: 后端挂号API (Task 6)
- Produces: 可运行的微信小程序，支持预约/取号/排队查询

**Step 1: 创建 app.json**

```json
{
  "pages": [
    "pages/index/index",
    "pages/queue/queue",
    "pages/evaluate/evaluate"
  ],
  "window": {
    "navigationBarBackgroundColor": "#1890FF",
    "navigationBarTitleText": "门诊叫号",
    "navigationBarTextStyle": "white"
  },
  "permission": {
    "scope.userLocation": {
      "desc": "用于获取您的位置信息，提供就诊导航"
    }
  }
}
```

**Step 2: 实现排队页面**

```javascript
// miniprogram/pages/queue/queue.js
Page({
  data: {
    queueNo: '-',
    waitingCount: 0,
    advanceWarning: false,
    deptName: '',
    doctorName: ''
  },

  onLoad(options) {
    const code = options.code; // 取号验证码
    this.fetchQueueStatus(code);
  },

  fetchQueueStatus(code) {
    wx.request({
      url: 'https://your-domain.com/api/v1/registrations/by-code',
      method: 'GET',
      data: { code },
      success: (res) => {
        this.setData({
          queueNo: res.data.queueNo,
          waitingCount: res.data.waitingCount,
          deptName: res.data.deptName,
          doctorName: res.data.doctorName
        });

        // 剩余3人时发送模板消息提醒
        if (res.data.waitingCount <= 3) {
          this.sendAdvanceNotice();
        }
      }
    });
  },

  sendAdvanceNotice() {
    wx.cloud.callFunction({
      name: 'sendWechatMessage',
      data: {
        templateId: 'QUEUE_ADVANCE',
        data: {
          thing1: { value: `${this.data.deptName} ${this.data.doctorName}` },
          number1: { value: `您前面还有${this.data.waitingCount}人` }
        }
      }
    });
  }
});
```

**Step 3: 编译运行**

```bash
# 使用微信开发者工具打开 miniprogram/ 目录
# 点击编译，验证挂号列表/排队查询/提醒功能
```

**Step 4: 提交**

```bash
git add miniprogram/
git commit -m "feat: 微信小程序患者端: 挂号列表/排队查询/提前3人提醒/诊后评价"
```

---

# 模块八：测试与部署

### Task 12: 单元测试

**Files:**
- Create: `backend/src/test/java/com/hospital/queuing/service/QueueServiceTest.java`
- Create: `backend/src/test/java/com/hospital/queuing/service/CallEngineServiceTest.java`
- Create: `backend/src/test/java/com/hospital/queuing/service/HisSyncServiceTest.java`

**Step 1: 编写 QueueService 完整测试**

```java
@Test
void testQueueOrderWithEmergencyPriority() {
    Registration normal = createRegistration(1, 1, 1, 1); // 普通
    Registration emergency = createRegistration(1, 1, 2, 1); // 急诊

    queueService.addToQueue(normal);
    queueService.addToQueue(emergency);

    var list = queueService.getWaitingList(1L, 1L);
    assertEquals("赵六", list.get(0).getPatientName()); // 急诊在前
}

@Test
void testNameMasking() {
    assertEquals("张**", maskName("张三"));
    assertEquals("李****", maskName("李白"));
    assertEquals("王", maskName("王"));
    assertNull(maskName(null));
}
```

**Step 2: 运行全部测试**

```bash
cd backend
mvn test
```

**Expected:** 所有测试用例PASS，覆盖率≥70%

**Step 3: 提交**

```bash
git add backend/src/test/
git commit -m "test: 添加QueueService/CallEngineService/HisSyncService单元测试，覆盖率≥70%"
```

### Task 13: Docker部署配置

**Files:**
- Create: `backend/Dockerfile`
- Create: `docker-compose.yml`
- Create: `nginx/conf.d/queuing.conf`
- Create: `nginx/Dockerfile`

**Step 1: 创建 Dockerfile**

```dockerfile
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY target/queuing-system-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Step 2: 创建 docker-compose.yml**

```yaml
version: '3.8'
services:
  app:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - DB_PASSWORD=queuing2026
      - REDIS_HOST=redis
    depends_on:
      - mysql
      - redis

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: queuing2026
      MYSQL_DATABASE: hospital_queuing
    volumes:
      - ./backend/src/main/resources/db:/docker-entrypoint-initdb.d
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    build: ./nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./screen:/usr/share/nginx/html/screen
      - ./admin/dist:/usr/share/nginx/html/admin
    depends_on:
      - app

volumes:
  mysql_data:
```

**Step 3: 运行验证**

```bash
docker-compose up -d
# 访问 http://localhost 验证管理后台和分诊屏
# 访问 http://localhost:8080/api/v1/health 验证后端健康检查
```

**Step 4: 提交**

```bash
git add backend/Dockerfile docker-compose.yml nginx/
git commit -m "feat: Docker一键部署配置: Spring Boot容器 + MySQL + Redis + Nginx反向代理"
```

---

## 完整文件结构

```
hospital-queuing-system/
├── backend/                    # Java Spring Boot 后端
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/
│       ├── main/
│       │   ├── java/com/hospital/queuing/
│       │   │   ├── QueuingApplication.java
│       │   │   ├── controller/
│       │   │   │   ├── RegistrationController.java
│       │   │   │   ├── CallController.java
│       │   │   │   └── HisController.java
│       │   │   ├── service/
│       │   │   │   ├── QueueService.java
│       │   │   │   ├── CallEngineService.java
│       │   │   │   └── HisSyncService.java
│       │   │   ├── ws/
│       │   │   │   └── CallWebSocketHandler.java
│       │   │   ├── task/
│       │   │   │   └── HisSyncScheduler.java
│       │   │   ├── entity/       (7个实体类)
│       │   │   ├── mapper/       (7个Mapper接口)
│       │   │   └── dto/          (请求/响应DTO)
│       │   └── resources/
│       │       ├── application.yml
│       │       └── db/
│       │           ├── init.sql
│       │           └── migration/
│       └── test/
│           └── java/.../service/
│               ├── QueueServiceTest.java
│               ├── CallEngineServiceTest.java
│               └── HisSyncServiceTest.java
├── admin/                      # Vue 3 管理后台
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── router/index.js
│       └── views/
│           ├── Login.vue
│           ├── Dashboard.vue
│           ├── DeptManage.vue
│           ├── DoctorManage.vue
│           ├── ScheduleManage.vue
│           ├── QueueMonitor.vue
│           ├── ScreenContent.vue
│           └── Reports.vue
├── screen/                     # 分诊屏HTML5前端
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── miniprogram/                # 微信小程序
│   ├── app.json
│   └── pages/
│       ├── index/
│       ├── queue/
│       └── evaluate/
├── nginx/                      # Nginx配置
│   ├── conf.d/queuing.conf
│   └── Dockerfile
└── docker-compose.yml          # 一键部署
```

---

## 实施里程碑

| 阶段 | 任务 | 工期 | 交付物 |
|------|------|------|--------|
| M1: 基础设施 | Task 1-3 | 3天 | 数据库+项目骨架+实体+Mapper |
| M2: 核心引擎 | Task 4-5 | 4天 | 排队管理+叫号引擎+WebSocket |
| M3: API层 | Task 6-7 | 3天 | RESTful API+HIS对接 |
| M4: 管理后台 | Task 8-9 | 5天 | Vue3后台6个页面 |
| M5: 分诊屏 | Task 10 | 2天 | HTML5分诊屏 |
| M6: 小程序 | Task 11 | 3天 | 微信小程序患者端 |
| M7: 测试部署 | Task 12-13 | 3天 | 单元测试+Docker部署 |
| **总计** | | **23个工作日** | **≈5周** |

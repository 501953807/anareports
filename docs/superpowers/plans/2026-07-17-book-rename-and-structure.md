# AnaReports 书籍命名重构与目录结构重组

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 11 本书和 11 份看板统一重命名为学术化/行业分析风格，修复 TOC 乱跳问题，在总纲 index.html 按四大分类重新组织。

**Architecture:** 所有修改通过 Python 脚本批量处理——先做文件名重命名（git mv），再做文件内部文本替换（title/tags/description），最后重写 index.html 的分类结构。每本书独立处理，可并行执行。

**Tech Stack:** Python 3, git mv, Bash find/grep, sed-style HTML editing

## Global Constraints

- 单一版本规则：每个文件只能有一个版本，禁止创建 -v2、-final 等变体副本
- 所有书名必须像真实出版的学术著作或行业研究报告
- 书名要能准确反映内容，内容也能从书名反推出来
- 名称要有文化内涵和学术针对性
- 看板与书籍一一对应，文件名和内部 title 标签同步更新
- 所有链接必须保持一致，index.html 中的 href 路径必须正确指向新的文件名
- 修复后的章节编号必须连续，不允许再出现乱跳

---

## 最终命名对照表（已确认）

### 第一辑 · 地域市场分析

| # | 目录/文件 | 旧书名 | 新书名 | 旧看板文件 | 新看板文件 |
|---|----------|--------|--------|-----------|-----------|
| 1 | `chongqing/` | 重庆产业全景分析与未来展望书 | 《重庆产业格局与未来展望：成渝双城经济圈深度研判》 | 重庆产业全景分析与未来展望看板.html | 《重庆产业全景研判看板：成渝经济圈·制造业·人口结构》 |
| 2 | `guangzhou/` | 广州吃喝玩乐+供应链全景书 | 《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》 | 广州吃喝玩乐+供应链全景看板.html | 《大湾区民生经济全景看板：广府消费·供应链·三产结构》 |

### 第二辑 · 学术与文化研究

| # | 目录/文件 | 旧书名 | 新书名 | 旧看板文件 | 新看板文件 |
|---|----------|--------|--------|-----------|-----------|
| 3 | `traditional-academics/` | 中华古典学术理论全景书 | 《中华古典学术源流与理论体系：从易经八卦到宋明理学》 | 中华古典学术理论全景看板.html | 《中华古典学术体系看板：易学·中医·儒道·阴阳五行》 |
| 4 | `money-laundering/` | 地下钱庄与洗钱全景书 | 《全球地下金融与洗钱机制研判：渠道·追踪·合规与反制》 | 全球地下钱庄与洗钱全景风险看板.html | 《全球地下金融与洗钱风险研判看板：渠道图谱·链上追踪·执法合规》 |

### 第三辑 · 宏观经济分析

| # | 目录/文件 | 旧书名 | 新书名 | 旧看板文件 | 新看板文件 |
|---|----------|--------|--------|-----------|-----------|
| 5 | `china-japan/` | 中日经济周期对比与个人投资出路书 | 《中日经济周期比较研究：日本失去的三十年与中国路径选择》 | 中日经济周期对比与个人投资出路看板.html | 《中日经济周期对比看板：宏观数据·政策应对·投资策略》 |

### 第四辑 · 产业专题研究

| # | 目录/文件 | 旧书名 | 新书名 | 旧看板文件 | 新看板文件 |
|---|----------|--------|--------|-----------|-----------|
| 6 | `creators/` | 创作者经济全景书 | 《全球创作者经济生态与变现模式研究：十大行当·八大手段·平台图谱》 | 全球创作者经济全景赚钱行当与平台看板.html | 《全球创作者经济生态看板：赚钱行当·平台矩阵·变现模型》 |
| 7 | `creators-ai/` | AI时代创作者经济全景书 | 《AI时代的创作者经济与数字版权保护：法律·技术·商业化全链路》 | 全球创作者经济AI时代个人变现与版权保护看板.html | 《AI创作者经济与数字版权看板：版权法·区块链认证·侵权维权》 |
| 8 | `ev-motorcycle/` | 新能源汽车与电动摩托车全产业链书 | 《中国新能源汽车与电动摩托车产业链全景：从上游矿产到出海战略》 | 中国新能源汽车与电动摩托车全产业链全景看板.html | 《新能源整车产业链看板：NEV·电动摩托·电池·电机·电控·出海》 |
| 9 | `pharma/` | 中国医药产业全球竞争力与中药发展全景书 | 《中国医药产业全球竞争力与中药现代化路径研究》 | 中国医药产业全球竞争力与中药发展全景看板.html | 《中国医药产业竞争力看板：全球格局·中药现代化·前沿赛道》 |
| 10 | `smart-devices/` | 智能手环与智能药盒产品开发全景书 | 《智能健康硬件产品开发与商业化研究：手环·药盒·健康监测》 | 智能手环与智能药盒产品开发全景看板.html | 《智能健康硬件开发看板：产品规划·技术方案·市场竞争·商业策略》 |
| 11 | `last-mile-commerce/` | 最后五公里商业模式全景书 | 《即时配送与最后一公里商业模式研究：平台博弈·经济学研判与全球比较》 | 最后五公里商业模式全景看板.html | 《即时配送与最后一公里商业看板：O2O·社区团购·积分经济·平台博弈》 |

---

## Phase 1: 书名/看板名重命名 + 总纲分类重组

### Task 1: 创建重命名工具脚本

**Files:**
- Create: `scripts/rename_books.py`

This script orchestrates all renaming. It uses a data-driven approach — the naming table above is embedded as Python data structures.

```python
#!/usr/bin/env python3
"""
AnaReports book renaming orchestrator.
Renames all 11 books and 11 kanban files, updates internal titles,
fixes TOC ordering, and rewrites index.html with classification groups.
"""

import os
import re
import shutil
from pathlib import Path

BASE = Path(__file__).parent.parent

# ============================================================
# BOOK RENAMING TABLE
# Each entry: (dir_name, old_book_title, new_book_title,
#              subtitle_for_card_desc, old_kanban_file, new_kanban_file,
#              old_kanban_title, new_kanban_title,
#              card_color, tags, page_count, chart_count)
# ============================================================

BOOKS = [
    {
        "dir": "chongqing",
        "old_index": "index.html",
        "book_title": "《重庆产业格局与未来展望：成渝双城经济圈深度研判》",
        "book_title_short": "重庆产业格局与未来展望",
        "card_desc": "重庆人口与户籍制度深度解析、GDP与产业结构全景、成渝双城经济圈协同、汽车制造与电子信息两大支柱产业、新兴产业发展路径、人口预测与风险预警。",
        "tags": ["成渝经济圈", "汽车制造", "电子信息"],
        "color": "cyan",
        "icon": "fas fa-city",
        "pages": 32,
        "charts": 32,
        "kanban_old": "重庆产业全景分析与未来展望看板.html",
        "kanban_new": "重庆产业全景研判看板_成渝经济圈_制造业_人口结构.html",
        "kanban_title": "重庆产业全景研判看板 — 成渝经济圈·制造业·人口结构",
    },
    {
        "dir": "guangzhou",
        "old_index": "index.html",
        "book_title": "《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》",
        "book_title_short": "粤港澳大湾区民生经济与消费产业研究",
        "card_desc": "广东省第一二三产业全景分析，广府美食文化经济、旅游消费、供应链批发市场（街道级详解）、跨境电商基地、六大城区商贸格局与大湾区协同。",
        "tags": ["大湾区", "民生经济", "供应链"],
        "color": "green",
        "icon": "fas fa-store",
        "pages": 31,
        "charts": 9,
        "kanban_old": "广州吃喝玩乐+供应链全景看板.html",
        "kanban_new": "大湾区民生经济全景看板_广府消费_供应链_三产结构.html",
        "kanban_title": "大湾区民生经济全景看板 — 广府消费·供应链·三产结构",
    },
    {
        "dir": "traditional-academics",
        "old_index": "index.html",
        "book_title": "《中华古典学术源流与理论体系：从易经八卦到宋明理学》",
        "book_title_short": "中华古典学术源流与理论体系",
        "card_desc": "八卦起源与伏羲神农、周易文王系辞、阴阳五行经典体系、中医藏象经络病机、道教修炼功法、儒家孟子女心学——从先秦到宋明理学的全景梳理。",
        "tags": ["易经", "中医", "儒道"],
        "color": "gold",
        "icon": "fas fa-scroll",
        "pages": 32,
        "charts": 21,
        "kanban_old": "中华古典学术理论全景看板.html",
        "kanban_new": "中华古典学术体系看板_易学_中医_儒道_阴阳五行.html",
        "kanban_title": "中华古典学术体系看板 — 易学·中医·儒道·阴阳五行",
    },
    {
        "dir": "money-laundering",
        "old_index": "index.html",
        "book_title": "《全球地下金融与洗钱机制研判：渠道·追踪·合规与反制》",
        "book_title_short": "全球地下金融与洗钱机制研判",
        "card_desc": "地下钱庄对敲、哈瓦拉体系、虚拟币混币、贸易洗钱、离岸空壳公司——六大渠道全解析，含链上犯罪追踪、东南亚杀猪盘资金链路、反洗钱合规指南。",
        "tags": ["反洗钱", "地下金融", "虚拟币"],
        "color": "cyan",
        "icon": "fas fa-building-columns",
        "pages": 30,
        "charts": 8,
        "kanban_old": "全球地下钱庄与洗钱全景风险看板.html",
        "kanban_new": "全球地下金融与洗钱风险研判看板_渠道图谱_链上追踪_执法合规.html",
        "kanban_title": "全球地下金融与洗钱风险研判看板 — 渠道图谱·链上追踪·执法合规",
    },
    {
        "dir": "china-japan",
        "old_index": "index.html",
        "book_title": "《中日经济周期比较研究：日本失去的三十年与中国路径选择》",
        "book_title_short": "中日经济周期比较研究",
        "card_desc": "中国经济周期演进、日本失去的三十年经验教训、GDP/工资/资产价格数据对比、政策应对时间线、个人投资出路与资产配置策略。",
        "tags": ["经济周期", "中日对比", "投资策略"],
        "color": "pink",
        "icon": "fas fa-chart-line",
        "pages": 30,
        "charts": 12,
        "kanban_old": "中日经济周期对比与个人投资出路看板.html",
        "kanban_new": "中日经济周期对比看板_宏观数据_政策应对_投资策略.html",
        "kanban_title": "中日经济周期对比看板 — 宏观数据·政策应对·投资策略",
    },
    {
        "dir": "creators",
        "old_index": "index.html",
        "book_title": "《全球创作者经济生态与变现模式研究：十大行当·八大手段·平台图谱》",
        "book_title_short": "全球创作者经济生态与变现模式研究",
        "card_desc": "十大赚钱行当深度解析，20+ 主流平台全景图谱，八大变现手段拆解，创作者收入金字塔与新手起步路线图。涵盖自媒体、游戏、网文、播客、课程、自由职业等全领域。",
        "tags": ["创作者经济", "变现手段", "平台图谱"],
        "color": "purple",
        "icon": "fas fa-palette",
        "pages": 32,
        "charts": 10,
        "kanban_old": "全球创作者经济全景赚钱行当与平台看板.html",
        "kanban_new": "全球创作者经济生态看板_赚钱行当_平台矩阵_变现模型.html",
        "kanban_title": "全球创作者经济生态看板 — 赚钱行当·平台矩阵·变现模型",
    },
    {
        "dir": "creators-ai",
        "old_index": "index.html",
        "book_title": "《AI时代的创作者经济与数字版权保护：法律·技术·商业化全链路》",
        "book_title_short": "AI时代的创作者经济与数字版权保护",
        "card_desc": "AI 创作者经济全景图谱、版权法与合理使用原则、AI 生成内容版权归属、区块链数字水印认证、侵权监测与取证、合同条款与保险保护、商业化 IP 策略。",
        "tags": ["AI版权", "区块链认证", "侵权维权"],
        "color": "green",
        "icon": "fas fa-robot",
        "pages": 32,
        "charts": 32,
        "kanban_old": "全球创作者经济AI时代个人变现与版权保护看板.html",
        "kanban_new": "AI创作者经济与数字版权看板_版权法_区块链认证_侵权维权.html",
        "kanban_title": "AI创作者经济与数字版权看板 — 版权法·区块链认证·侵权维权",
    },
    {
        "dir": "ev-motorcycle",
        "old_index": "index.html",
        "book_title": "《中国新能源汽车与电动摩托车产业链全景：从上游矿产到出海战略》",
        "book_title_short": "中国新能源汽车与电动摩托车产业链全景",
        "card_desc": "新能源整车产业链、电池/电机/电控核心技术、电动摩托车出海战略、全球市场竞争格局、智能化发展趋势与政策环境分析。",
        "tags": ["新能源车", "电动摩托", "全产业链"],
        "color": "red",
        "icon": "fas fa-car",
        "pages": 29,
        "charts": 11,
        "kanban_old": "中国新能源汽车与电动摩托车全产业链全景看板.html",
        "kanban_new": "新能源整车产业链看板_NEV_电动摩托_电池_电机_电控_出海.html",
        "kanban_title": "新能源整车产业链看板 — NEV·电动摩托·电池·电机·电控·出海",
    },
    {
        "dir": "pharma",
        "old_index": "index.html",
        "book_title": "《中国医药产业全球竞争力与中药现代化路径研究》",
        "book_title_short": "中国医药产业全球竞争力与中药现代化路径",
        "card_desc": "全球医药产业格局、中国医药竞争力分析、中药现代化发展路径、十大前沿医药赛道深度、原料药霸权、创新药管线、CXO 与 GLP-1 赛道。",
        "tags": ["医药产业", "中药", "全球化"],
        "color": "orange",
        "icon": "fas fa-pills",
        "pages": 31,
        "charts": 10,
        "kanban_old": "中国医药产业全球竞争力与中药发展全景看板.html",
        "kanban_new": "中国医药产业竞争力看板_全球格局_中药现代化_前沿赛道.html",
        "kanban_title": "中国医药产业竞争力看板 — 全球格局·中药现代化·前沿赛道",
    },
    {
        "dir": "smart-devices",
        "old_index": "index.html",
        "book_title": "《智能健康硬件产品开发与商业化研究：手环·药盒·健康监测》",
        "book_title_short": "智能健康硬件产品开发与商业化研究",
        "card_desc": "智能手环产品规划、智能药盒技术方案、健康监测功能设计、产品开发全流程、市场竞争分析、AI 算法应用与商业化策略。",
        "tags": ["智能硬件", "产品开发", "健康监测"],
        "color": "gold",
        "icon": "fas fa-microchip",
        "pages": 30,
        "charts": 9,
        "kanban_old": "智能手环与智能药盒产品开发全景看板.html",
        "kanban_new": "智能健康硬件开发看板_产品规划_技术方案_市场竞争_商业策略.html",
        "kanban_title": "智能健康硬件开发看板 — 产品规划·技术方案·市场竞争·商业策略",
    },
    {
        "dir": "last-mile-commerce",
        "old_index": "index.html",
        "book_title": "《即时配送与最后一公里商业模式研究：平台博弈·经济学研判与全球比较》",
        "book_title_short": "即时配送与最后一公里商业模式研究",
        "card_desc": "六大板块全景解析：即时配送、社区团购、即时零售、积分经济、平台博弈与技术驱动。覆盖美团/Douyin/饿了么等平台，12+经济学流派交叉研判，63页深度分析。",
        "tags": ["O2O", "即时配送", "平台博弈", "AI调度"],
        "color": "cyan",
        "icon": "fas fa-truck-fast",
        "pages": 63,
        "charts": 20,
        "kanban_old": "最后五公里商业模式全景看板.html",
        "kanban_new": "即时配送与最后一公里商业看板_O2O_社区团购_积分经济_平台博弈.html",
        "kanban_title": "即时配送与最后一公里商业看板 — O2O·社区团购·积分经济·平台博弈",
    },
]


def update_html_file(filepath, replacements):
    """Replace strings in an HTML file in-place."""
    path = Path(filepath)
    if not path.exists():
        print(f"  SKIP: {filepath} does not exist")
        return False
    content = path.read_text(encoding="utf-8")
    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"  UPDATED: {filepath}")
        return True
    else:
        print(f"  NO CHANGES: {filepath}")
        return False


def rename_book_dir(book):
    """Rename all chapter HTML files in a book directory according to numbering fix."""
    dir_path = BASE / book["dir"]
    if not dir_path.exists():
        print(f"  SKIP: directory {book['dir']} does not exist")
        return []

    renamed_files = []
    for html_file in sorted(dir_path.glob("*.html")):
        if html_file.name == "index.html":
            continue
        # Check if filename needs renumbering (for TOC fix)
        renamed_files.append(html_file)

    return renamed_files


def main():
    print("=" * 60)
    print("AnaReports Book Renaming Orchestrator")
    print("=" * 60)

    # Step 1: Rename root-level kanban files
    print("\n[Step 1] Renaming root-level kanban files...")
    for book in BOOKS:
        old_path = BASE / book["kanban_old"]
        new_path = BASE / book["kanban_new"]
        if old_path.exists():
            old_path.rename(new_path)
            print(f"  RENAMED: {book['kanban_old']} -> {book['kanban_new']}")
        else:
            print(f"  SKIP: {book['kanban_old']} does not exist")

    # Step 2: Update kanban file internal titles
    print("\n[Step 2] Updating kanban file internal <title> tags...")
    for book in BOOKS:
        kanban_path = BASE / book["kanban_new"]
        if kanban_path.exists():
            replacements = {
                f"<title>{book['kanban_old'].replace('.html', '')}</title>": f"<title>{book['kanban_title']}</title>",
            }
            update_html_file(kanban_path, replacements)

    # Step 3: Rename book directories' index.html titles
    print("\n[Step 3] Updating book index.html files...")
    for book in BOOKS:
        idx_path = BASE / book["dir"] / "index.html"
        if idx_path.exists():
            short_name = book["book_title_short"]
            full_name = book["book_title"]
            replacements = {
                "<title>": f"<title>{full_name} ",
                f"{book['book_title_short']}": short_name,
                # Update card title in index
                '"card-title">': f'"card-title">{short_name}',
                # Update card description
                '"card-desc">': f'"card-desc">\n      {book["card_desc"]}\n    ',
                # Update tags
            }
            update_html_file(idx_path, replacements)

    print("\nDone!")


if __name__ == "__main__":
    main()
```

**Why this approach:** A single orchestrator script ensures consistency — every rename, title replacement, and link update happens atomically per book. The data-driven design makes it easy to verify all 11 renames against the naming table.

- [ ] **Step 1: Write the orchestrator script**

Create `scripts/rename_books.py` with the full content above.

- [ ] **Step 2: Dry-run mode — verify all file existence before actual renaming**

Add `--dry-run` flag support and run:
```bash
cd /Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports
python3 scripts/rename_books.py --dry-run
```
Expected output: lists all source files that exist and all target paths they would map to, with no filesystem changes.

- [ ] **Step 3: Execute actual renaming**

Run without `--dry-run`:
```bash
python3 scripts/rename_books.py
```
Expected output: 11 kanban files renamed, 11 book index.html files updated, all internal `<title>` tags changed.

- [ ] **Step 4: Verify no broken links**

Run a grep to confirm no references remain to old filenames:
```bash
grep -r "全球创作者经济全景赚钱行当与平台看板" . --include="*.html" --exclude-dir=".git"
grep -r "广州吃喝玩乐" . --include="*.html" --exclude-dir=".git"
```
Expected: zero matches outside of `.git/` history.

- [ ] **Step 5: Commit Phase 1 Part A**

```bash
git add -A
git commit -m "refactor: rename all 11 books and 11 kanbans to academic/professional titles"
```

---

### Task 2: 修复 TOC 乱跳（章节编号连续性）

**Files:**
- Modify: `ev-motorcycle/index.html` — 重新排序 TOC 链接
- Modify: `guangzhou/index.html` — 重新排序 TOC 链接
- Modify: `chongqing/index.html` — 调整 21a-21h 附录位置
- Modify: `smart-devices/index.html` — 重新排序 TOC 链接

**Problem analysis per book:**

**ev-motorcycle/ TOC current order:**
```
01-market-overview → 11-nev-market-detail → 12-two-wheel-market-detail → 13-price-analysis
→ 02-nev-supply-chain → 14-upstream-minerals → 15-battery-materials → 16-semiconductor → 17-chassis-components
→ 03-parts-catalog → 21-battery-system-deep → 22-electric-drive-deep → 23-thermal-management → 24-smart-driving
→ 04-two-wheel → 25-yadea-deep → 26-aima-deep → 27-battery-tech-compare
→ 05-clusters → 31-nev-cluster-deep → 32-two-wheel-cluster-deep
→ 06-maintenance → 33-nev-maintenance-deep → 34-two-wheel-maintenance-deep
→ 07-global-market → 35-europe-market → 36-southeast-asia-market → 37-policy-analysis → 38-india-market
```

**Logical grouping (what it SHOULD be):**
```
第一章：市场概览 (01)
第二章：NEV市场深度 (11-13)
第三章：产业链上游 (02, 14-17)
第四章：零部件目录 (03, 21-24)
第五章：电动摩托 (04, 25-27)
第六章：产业集群 (05, 31-32)
第七章：维护保养 (06, 33-34)
第八章：全球市场 (07, 35-38)
```

The chapter numbers (01-07 = overview chapters, 11-38 = deep-dive chapters) are intentional grouping scheme. The TOC just needs to list them in logical reading order: all overview first, then all deep-dives grouped by theme.

**guangzhou/ TOC current order:**
```
01-city-overview → 02-food → 09-food-tea → 10-food-roast → 11-food-street-snacks
→ 12-food-old-brands → 13-food-streets → 03-attractions → 14-attractions-history
→ 15-attractions-modern → 16-attractions-night → 04-nightlife-shopping → 05-supply-category
→ 19-supply-clothing-detail → 20-supply-leather-detail → 21-supply-jewelry-detail
→ 22-supply-tea-detail → 23-supply-electronics-detail → 24-supply-beauty-detail
→ 17-supply-food-detail → 18-supply-automotive-detail → 06-supply-districts
→ 07-cross-border → 25-cross-border-platforms → 26-cross-border-logistics
→ 27-cross-border-services → 28-logistics-hub → 29-cultural-tourism → 30-future-guangzhou
→ 31-guangzhou-internationalization → 08-travel-routes
```

**Logical grouping (what it SHOULD be):**
```
第一章：城市概览 (01)
第二章：美食地图 (02, 09-13)
第三章：旅游景点 (03, 14-16)
第四章：夜生活购物 (04, 08)
第五章：供应链品类 (05, 17-24)
第六章：城区商贸格局 (06)
第七章：跨境电商 (07, 25-28)
第八章：文旅与未来 (29-31)
```

**chongqing/ TOC issue:**
```
21-income-levels → 21a-hotpot-economy → 21b-xiaomian-industry → ... → 21h-individual-merchants
→ 22-housing-affordability → ...
```
The 21a-21h appendices break the 21→22 flow. They should be placed AFTER chapter 21's logical group ends, or renamed to 22a-22h and integrated into the sequence.

**smart-devices/ TOC current order:**
```
01-market-overview → 11-heart-monitor-depth → 12-sleep-tracking-depth → 13-gps-tracker-depth
→ 02-user-profile → 03-system-architecture → 04-competitive-analysis
→ 05-supply-chain-bom → 06-app-development → 07-regulations → 08-business-model → 09-roadmap → 10-risk-assessment
→ 14-sensor-technology → 15-bluetooth-wifi-nfc → 16-battery-tech → 17-waterproof-design
→ 18-materials-selection → 19-factory-quality → 20-elderly-user-experience
→ 21-family-app-ecosystem → 22-health-data-analytics → 23-ai-algorithm
→ 24-cloud-platform → 25-iot-smart-home → 26-manufacturing-process → 27-brand-marketing
→ 28-after-sales-service → 29-partnership-hospital → 30-global-certification
```

**Logical grouping:**
```
第一章：市场概览 (01)
第二章：用户画像 (02)
第三章：系统架构 (03)
第四章：竞争分析 (04)
第五章：供应链 (05)
第六章：App开发 (06)
第七章：法规 (07)
第八章：商业模式 (08)
第九章：产品路线图 (09)
第十章：风险评估 (10)
第十一章：健康监测深度 (11-13)
第十二章：传感器技术 (14-23)
第十三章：云平台与IoT (24-25)
第十四章：制造与品牌 (26-30)
```

**Fix strategy:** For each book, rewrite the sidebar TOC section in `index.html` to list chapters in logical reading order. Do NOT rename the actual HTML files (their numbering encodes the grouping scheme). Just reorder the TOC links.

- [ ] **Step 1: Fix ev-motorcycle TOC**

Read `ev-motorcycle/index.html`, identify the sidebar TOC `<ul>` block, reorder links to: 01 → 11-13 → 02 → 14-17 → 03 → 21-24 → 04 → 25-27 → 05 → 31-32 → 06 → 33-34 → 07 → 35-38.

- [ ] **Step 2: Fix guangzhou TOC**

Read `guangzhou/index.html`, reorder sidebar TOC links to: 01 → 02 → 09-13 → 03 → 14-16 → 04 → 08 → 05 → 17-24 → 06 → 07 → 25-28 → 29-31.

- [ ] **Step 3: Fix chongqing TOC**

Read `chongqing/index.html`, move 21a-21h after 21 or integrate them as sub-items under 21-income-levels section. Reorder: 01-20 → 21 → 21a-21h → 22-31.

- [ ] **Step 4: Fix smart-devices TOC**

Read `smart-devices/index.html`, reorder sidebar TOC links to: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11-13 → 14-23 → 24-25 → 26-30.

- [ ] **Step 5: Verify all TOCs render correctly**

Open each book's index.html in browser and verify sidebar shows correct sequential order.

- [ ] **Step 6: Commit TOC fixes**

```bash
git add ev-motorcycle/index.html guangzhou/index.html chongqing/index.html smart-devices/index.html
git commit -m "fix: reorder TOC links in ev-motorcycle, guangzhou, chongqing, smart-devices books"
```

---

### Task 3: 重写总纲 index.html 分类结构

**Files:**
- Modify: `/Users/tangxiaochuan/AIWorkspace/ClaudeWorkspace/AnaReports/index.html`

This is the most critical change — reorganizing the entire landing page into four classification groups.

**New structure:**

```html
<!-- Hero section: update stats from "10 套" to "11 套" and "12 份" to "11 份" -->

<!-- 第一辑 · 地域市场分析 -->
<h2 class="section-title"><i class="fas fa-map-marked-alt"></i> 第一辑 · 地域市场分析</h2>
<div class="books-grid">
  <!-- chongqing card -->
  <!-- guangzhou card -->
</div>

<!-- 第二辑 · 学术与文化研究 -->
<h2 class="section-title"><i class="fas fa-landmark"></i> 第二辑 · 学术与文化研究</h2>
<div class="books-grid">
  <!-- traditional-academics card -->
  <!-- money-laundering card -->
</div>

<!-- 第三辑 · 宏观经济分析 -->
<h2 class="section-title"><i class="fas fa-chart-area"></i> 第三辑 · 宏观经济分析</h2>
<div class="books-grid">
  <!-- china-japan card -->
</div>

<!-- 第四辑 · 产业专题研究 -->
<h2 class="section-title"><i class="fas fa-industry"></i> 第四辑 · 产业专题研究</h2>
<div class="books-grid">
  <!-- creators card -->
  <!-- creators-ai card -->
  <!-- ev-motorcycle card -->
  <!-- pharma card -->
  <!-- smart-devices card -->
  <!-- last-mile-commerce card -->
</div>

<!-- Kanban section: update all 11 links to point to new filenames -->
<div class="kanban-section">
  <h2 class="section-title"><i class="fas fa-th-large"></i> 独立看板（单页版）</h2>
  <div class="kanban-grid">
    <!-- 11 kanban cards with NEW filenames -->
  </div>
</div>

<!-- Footer: update "11 套全景书 · 400+ 页内容 · 11 份独立看板" -->
```

**Card mapping (with new titles and colors):**

| 分类 | 目录 | 卡片标题(显示用) | 颜色 | 图标 |
|------|------|----------------|------|------|
| 地域市场 | chongqing | 重庆产业格局与未来展望 | cyan | fas fa-city |
| 地域市场 | guangzhou | 粤港澳大湾区民生经济与消费产业研究 | green | fas fa-store |
| 学术研究 | traditional-academics | 中华古典学术源流与理论体系 | gold | fas fa-scroll |
| 学术研究 | money-laundering | 全球地下金融与洗钱机制研判 | cyan | fas fa-building-columns |
| 宏观经济 | china-japan | 中日经济周期比较研究 | pink | fas fa-chart-line |
| 产业专题 | creators | 全球创作者经济生态与变现模式研究 | purple | fas fa-palette |
| 产业专题 | creators-ai | AI时代的创作者经济与数字版权保护 | green | fas fa-robot |
| 产业专题 | ev-motorcycle | 中国新能源汽车与电动摩托车产业链全景 | red | fas fa-car |
| 产业专题 | pharma | 中国医药产业全球竞争力与中药现代化路径 | orange | fas fa-pills |
| 产业专题 | smart-devices | 智能健康硬件产品开发与商业化研究 | gold | fas fa-microchip |
| 产业专题 | last-mile-commerce | 即时配送与最后一公里商业模式研究 | cyan | fas fa-truck-fast |

- [ ] **Step 1: Read current index.html and extract existing card HTML blocks**

Read lines 313-535 (the books-grid section) to get the exact HTML structure of each card.

- [ ] **Step 2: Rewrite index.html books section with 4 classification groups**

Replace the single `<div class="books-grid">` with four sections, each having its own `<h2 class="section-title">` header and its own `<div class="books-grid">`. Each card gets the new title, new description, and updated href paths.

- [ ] **Step 3: Update kanban section with new filenames**

Replace all 11 kanban card `href` attributes with the new filenames from the naming table. Update kanban titles accordingly.

- [ ] **Step 4: Update hero stats bar**

Change `10 套` to `11 套`, `12 份` to `11 份`.

- [ ] **Step 5: Update footer**

Change `11 套全景书 · 400+ 页内容 · 12 份独立看板` to `11 套全景书 · 400+ 页内容 · 11 份独立看板`.

- [ ] **Step 6: Verify index.html renders correctly**

Open http://localhost:8766 in browser, verify all 4 classification headers display, all 11 cards have correct new titles, all links work.

- [ ] **Step 7: Commit index.html rewrite**

```bash
git add index.html
git commit -m "feat: restructure index.html with 4 classification groups — regional markets, academic research, macroeconomics, industry studies"
```

---

## Phase 2: guangzhou 内容重构（待后续执行）

**Scope:** 将 `guangzhou/` 目录下的 31 页内容从"广州吃喝玩乐+供应链"扩展为"粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局"。

**Key changes:**
1. 保留美食和旅游章节但大幅缩减（从 ~12 页压缩到 ~5 页）
2. 新增广东省一二三产业民生行业分析章节（~10 页）
3. 将"广州供应链"扩展到"广东供应链网络"（~5 页）
4. 新增粤港澳大湾区经济协同章节（~3 页）
5. 看板同步重构

**This phase requires content creation, not just structural changes.** It will be planned and executed separately after Phase 1 is approved and committed.

---

## Execution Order

1. **Task 1** — Rename all files and update titles (orchestrated by Python script)
2. **Task 2** — Fix TOC ordering in 4 books
3. **Task 3** — Rewrite index.html classification structure
4. **Phase 2** — guangzhou content restructuring (separate plan)

Each task should be committed separately for clean git history.

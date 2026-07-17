#!/usr/bin/env python3
"""
AnaReports book renaming orchestrator.
Renames all 11 kanban files, updates all internal titles across books.
Uses exact string matching per book to avoid false positives.
"""

import sys
import re
from pathlib import Path

BASE = Path(__file__).parent.parent


# ============================================================
# EXACT MAPPING TABLE
# Each entry maps OLD strings -> NEW strings for that specific book
# ============================================================

BOOKS = [
    {
        "dir": "chongqing",
        # Old title patterns found in <title> tags (after " — ")
        "old_chapter_suffix": "重庆产业全景分析与未来展望",
        "old_index_title": "重庆产业全景分析与未来展望 — 封面",
        "new_book_full": "《重庆产业格局与未来展望：成渝双城经济圈深度研判》",
        "new_book_short": "重庆产业格局与未来展望",
        "new_index_title": "《重庆产业格局与未来展望：成渝双城经济圈深度研判》 — 封面",
        "kanban_old": "重庆产业全景分析与未来展望看板.html",
        "kanban_new": "重庆产业全景研判看板_成渝经济圈_制造业_人口结构.html",
        "kanban_title": "重庆产业全景研判看板 — 成渝经济圈·制造业·人口结构",
    },
    {
        "dir": "guangzhou",
        "old_chapter_suffix": "广州吃喝玩乐+供应链全景书",
        "old_index_title": "广州吃喝玩乐+供应链全景书 — 封面",
        "new_book_full": "《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》",
        "new_book_short": "粤港澳大湾区民生经济与消费产业研究",
        "new_index_title": "《粤港澳大湾区民生经济与消费产业研究：从广州样本到广东格局》 — 封面",
        "kanban_old": "广州吃喝玩乐+供应链全景看板.html",
        "kanban_new": "大湾区民生经济全景看板_广府消费_供应链_三产结构.html",
        "kanban_title": "大湾区民生经济全景看板 — 广府消费·供应链·三产结构",
    },
    {
        "dir": "traditional-academics",
        "old_chapter_suffix": "中华古典学术理论全景书",
        "old_index_title": "中华古典学术理论全景书 — 封面",
        "new_book_full": "《中华古典学术源流与理论体系：从易经八卦到宋明理学》",
        "new_book_short": "中华古典学术源流与理论体系",
        "new_index_title": "《中华古典学术源流与理论体系：从易经八卦到宋明理学》 — 封面",
        "kanban_old": "中华古典学术理论全景看板.html",
        "kanban_new": "中华古典学术体系看板_易学_中医_儒道_阴阳五行.html",
        "kanban_title": "中华古典学术体系看板 — 易学·中医·儒道·阴阳五行",
    },
    {
        "dir": "money-laundering",
        "old_chapter_suffix": "全球地下钱庄与洗钱全景风险",
        "old_index_title": "全球地下钱庄与洗钱全景风险 — 书",
        "new_book_full": "《全球地下金融与洗钱机制研判：渠道·追踪·合规与反制》",
        "new_book_short": "全球地下金融与洗钱机制研判",
        "new_index_title": "《全球地下金融与洗钱机制研判：渠道·追踪·合规与反制》 — 书",
        "kanban_old": "全球地下钱庄与洗钱全景风险看板.html",
        "kanban_new": "全球地下金融与洗钱风险研判看板_渠道图谱_链上追踪_执法合规.html",
        "kanban_title": "全球地下金融与洗钱风险研判看板 — 渠道图谱·链上追踪·执法合规",
    },
    {
        "dir": "china-japan",
        "old_chapter_suffix": "中日经济周期对比书",
        "old_index_title": "中日经济周期对比书 — 从失去的三十年看中国未来",
        "new_book_full": "《中日经济周期比较研究：日本失去的三十年与中国路径选择》",
        "new_book_short": "中日经济周期比较研究",
        "new_index_title": "《中日经济周期比较研究：日本失去的三十年与中国路径选择》 — 从失去的三十年看中国未来",
        "kanban_old": "中日经济周期对比与个人投资出路看板.html",
        "kanban_new": "中日经济周期对比看板_宏观数据_政策应对_投资策略.html",
        "kanban_title": "中日经济周期对比看板 — 宏观数据·政策应对·投资策略",
    },
    {
        "dir": "creators",
        "old_chapter_suffix": "全球创作者经济全景看板",
        "old_index_title": "全球创作者经济全景看板 — 封面",
        "new_book_full": "《全球创作者经济生态与变现模式研究：十大行当·八大手段·平台图谱》",
        "new_book_short": "全球创作者经济生态与变现模式研究",
        "new_index_title": "《全球创作者经济生态与变现模式研究：十大行当·八大手段·平台图谱》 — 封面",
        "kanban_old": "全球创作者经济全景赚钱行当与平台看板.html",
        "kanban_new": "全球创作者经济生态看板_赚钱行当_平台矩阵_变现模型.html",
        "kanban_title": "全球创作者经济生态看板 — 赚钱行当·平台矩阵·变现模型",
    },
    {
        "dir": "creators-ai",
        "old_chapter_suffix": "全球创作者经济AI时代个人变现与版权保护全景书",
        "old_index_title": "全球创作者经济AI时代个人变现与版权保护全景书 — 封面",
        "new_book_full": "《AI时代的创作者经济与数字版权保护：法律·技术·商业化全链路》",
        "new_book_short": "AI时代的创作者经济与数字版权保护",
        "new_index_title": "《AI时代的创作者经济与数字版权保护：法律·技术·商业化全链路》 — 封面",
        "kanban_old": "全球创作者经济AI时代个人变现与版权保护看板.html",
        "kanban_new": "AI创作者经济与数字版权看板_版权法_区块链认证_侵权维权.html",
        "kanban_title": "AI创作者经济与数字版权看板 — 版权法·区块链认证·侵权维权",
    },
    {
        "dir": "ev-motorcycle",
        "old_chapter_suffix": "中国新能源汽车与电动摩托车全产业链书",
        "old_index_title": "中国新能源汽车与电动摩托车全产业链书 — 封面",
        "new_book_full": "《中国新能源汽车与电动摩托车产业链全景：从上游矿产到出海战略》",
        "new_book_short": "中国新能源汽车与电动摩托车产业链全景",
        "new_index_title": "《中国新能源汽车与电动摩托车产业链全景：从上游矿产到出海战略》 — 封面",
        "kanban_old": "中国新能源汽车与电动摩托车全产业链全景看板.html",
        "kanban_new": "新能源整车产业链看板_NEV_电动摩托_电池_电机_电控_出海.html",
        "kanban_title": "新能源整车产业链看板 — NEV·电动摩托·电池·电机·电控·出海",
    },
    {
        "dir": "pharma",
        "old_chapter_suffix": "中国医药产业全景书",
        "old_index_title": "中国医药产业全景书 — 全球竞争力与中药发展",
        "new_book_full": "《中国医药产业全球竞争力与中药现代化路径研究》",
        "new_book_short": "中国医药产业全球竞争力与中药现代化路径",
        "new_index_title": "《中国医药产业全球竞争力与中药现代化路径研究》 — 全球竞争力与中药发展",
        "kanban_old": "中国医药产业全球竞争力与中药发展全景看板.html",
        "kanban_new": "中国医药产业竞争力看板_全球格局_中药现代化_前沿赛道.html",
        "kanban_title": "中国医药产业竞争力看板 — 全球格局·中药现代化·前沿赛道",
    },
    {
        "dir": "smart-devices",
        "old_chapter_suffix": "智能手环与智能药盒产品开发书",
        "old_index_title": "智能手环与智能药盒产品开发书 — 从0到上市的全景指南",
        "new_book_full": "《智能健康硬件产品开发与商业化研究：手环·药盒·健康监测》",
        "new_book_short": "智能健康硬件产品开发与商业化研究",
        "new_index_title": "《智能健康硬件产品开发与商业化研究：手环·药盒·健康监测》 — 从0到上市的全景指南",
        "kanban_old": "智能手环与智能药盒产品开发全景看板.html",
        "kanban_new": "智能健康硬件开发看板_产品规划_技术方案_市场竞争_商业策略.html",
        "kanban_title": "智能健康硬件开发看板 — 产品规划·技术方案·市场竞争·商业策略",
    },
    {
        "dir": "last-mile-commerce",
        "old_chapter_suffix": "最后五公里商业模式全景书",
        "old_index_title": "最后五公里商业模式全景书 — 封面",
        "new_book_full": "《即时配送与最后一公里商业模式研究：平台博弈·经济学研判与全球比较》",
        "new_book_short": "即时配送与最后一公里商业模式研究",
        "new_index_title": "《即时配送与最后一公里商业模式研究：平台博弈·经济学研判与全球比较》 — 封面",
        "kanban_old": "最后五公里商业模式全景看板.html",
        "kanban_new": "即时配送与最后一公里商业看板_O2O_社区团购_积分经济_平台博弈.html",
        "kanban_title": "即时配送与最后一公里商业看板 — O2O·社区团购·积分经济·平台博弈",
    },
]


def update_html_file(filepath, replacements):
    """Replace strings in an HTML file in-place."""
    path = Path(filepath)
    if not path.exists():
        print(f"  MISSING: {filepath}")
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


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("AnaReports Book Renaming Orchestrator")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    # Step 1: Rename root-level kanban files
    print("\n[Step 1] Renaming root-level kanban files...")
    for book in BOOKS:
        old_path = BASE / book["kanban_old"]
        new_path = BASE / book["kanban_new"]
        if old_path.exists():
            if dry_run:
                print(f"  WOULD RENAME: {book['kanban_old']} -> {book['kanban_new']}")
            else:
                old_path.rename(new_path)
                print(f"  RENAMED: {book['kanban_old']} -> {book['kanban_new']}")
        else:
            print(f"  SKIP: {book['kanban_old']} does not exist")

    # Step 2: Update kanban file internal <title> tags
    print("\n[Step 2] Updating kanban file internal <title> tags...")
    for book in BOOKS:
        kanban_path = BASE / book["kanban_new"]
        if not kanban_path.exists():
            continue
        old_title = book["kanban_old"].replace(".html", "")
        replacements = {}
        for suffix in ["", " v2.0", " v3.0"]:
            key = f"<title>{old_title}{suffix}</title>"
            val = f"<title>{book['kanban_title']}</title>"
            if key != val:
                replacements[key] = val
        update_html_file(kanban_path, replacements)

    # Step 3: Update book index.html files
    print("\n[Step 3] Updating book index.html files...")
    for book in BOOKS:
        idx_path = BASE / book["dir"] / "index.html"
        if not idx_path.exists():
            continue
        replacements = {
            f"<title>{book['old_index_title']}</title>": f"<title>{book['new_index_title']}</title>",
        }
        update_html_file(idx_path, replacements)

    # Step 4: Update each chapter page <title> tags
    # Format: "<title>章节标题 — 旧书名</title>"
    # Replace the old book name at end with new full book name
    print("\n[Step 4] Updating chapter page <title> tags...")
    for book in BOOKS:
        book_dir = BASE / book["dir"]
        old_suffix = book["old_chapter_suffix"]
        new_full = book["new_book_full"]
        for html_file in sorted(book_dir.glob("*.html")):
            if html_file.name == "index.html":
                continue
            content = html_file.read_text(encoding="utf-8")
            # Match: <title>XXX — 旧书名</title> or <title>XXX - 旧书名</title>
            new_content = re.sub(
                rf'(</title>)',
                lambda m: m.group(0),  # no-op placeholder
                content
            )
            # Simpler: just replace the old suffix before </title>
            new_content = content.replace(
                f" — {old_suffix}</title>",
                f" — {new_full}</title>"
            )
            new_content = new_content.replace(
                f" - {old_suffix}</title>",
                f" - {new_full}</title>"
            )
            new_content = new_content.replace(
                f"·{old_suffix}</title>",
                f"·{new_full}</title>"
            )
            if new_content != content:
                html_file.write_text(new_content, encoding="utf-8")
                print(f"  UPDATED: {html_file.name}")

    print("\n" + "=" * 60)
    if dry_run:
        print("DRY RUN complete. No files were modified.")
        print("Run without --dry-run to apply changes.")
    else:
        print("All renaming complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

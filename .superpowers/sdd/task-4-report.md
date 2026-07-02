Task: 4.1
Status: DONE
Changes:
- Added Module 4 HTML: Southeast Asia underground banking specialty section with a 5-step fund flow diagram (fraud scam -> P2P crypto purchase -> OTC point distribution -> underground bank on-qiao -> overseas accounts) and 4 country enforcement data cards (Philippines, South Korea/Koan, China Break Card Action, Myanmar/Cambodia)
- Added Module 5 HTML: Global AML enforcement timeline (2020-2025) with 10 major events and compliance advice section with 3 cards (high-risk signal identification, AML system construction key points, cross-border collaboration trends)
- Added footer with data source attribution and disclaimer
- Preserved existing ECharts script block with all 6 charts (chart1-chart6) and responsive resize handler
- Verified correct nesting: module4 section, module5 section, footer, .container close, script, body close, html close

Concerns: None -- plan Step 2 had a typo (`<td>` instead of `</div>` for year 2023 KuCoin timeline item) which was corrected. Also changed `fa-safe-dollar-sign` (non-existent Font Awesome icon) to `fa-building` for the overseas account step. Korean currency display adjusted slightly for clarity (KRW 300亿 vs original). All existing CSS classes (flow-steps, timeline, channel-card, card, grid-2, section-subtitle) were already present in the stylesheet and reused without modification.

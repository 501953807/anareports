Task: 3.1
Status: DONE
Changes:
- Inserted Module 3 HTML section (lines 547-614) after Module 2's closing `</section>` and before `</div><!-- .container -->`. Contains:
  - Two ECharts chart containers: `chart-crypto-trend` (stacked bar, global crypto crime trend 2019-2023) and `chart-crypto-type` (donut pie, 2023 crypto crime type distribution)
  - DeFi Exploited TOP 10 table (Euler, Beanstalk, Rhino Finance, etc., with Wormhole at $3.2B)
  - Cross-chain bridge hack TOP 10 table (Ronin $6.25B, Nomad $1.9B, Wormhole, Multichain, etc.)
  - CEX/DEX AML penalty table (Binance $43B, OKX $10B, KuCoin $4.1B, FTX $80B civil, Tether, Circle)
- Appended chart5 and chart6 ECharts configurations to the existing `<script>` block:
  - chart5: stacked bar showing crypto crime trends by type (scam/fraud, ransomware, darknet markets, mixers, sanctions evasion)
  - chart6: donut pie showing 2023 crypto crime type distribution by percentage
- Updated the `window.addEventListener('resize', ...)` callback to include `chart5.resize()` and `chart6.resize()`
Concerns:
- The file remains a single self-contained HTML with all inline CSS/JS, consistent with the global constraints.
- Chart IDs (`chart-crypto-trend`, `chart-crypto-type`) match the HTML containers and JS initialization exactly.
- Data source attributions are present at the bottom of each table within Module 3.

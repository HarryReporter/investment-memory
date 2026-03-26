---
name: investment-framework
description: 投资决策框架工具。当用户提到"估值"、"仓位"、"风险评估"、"投资决策"、"买入时机"、"止损"、"止盈"、"凯利公式"、"PE分位数"、"PEG"、"市场状态"时自动触发。提供估值检查、仓位计算、风险评估、止损止盈和市场状态检测的结构化方法。
---

# Investment Framework Skill - 投资决策框架

提供结构化的投资决策工具，基于学术研究和业界实践，帮助评估投资机会的风险和收益。

## 框架文档

投资框架知识存储在 `vault/投资框架/` 目录。

## 核心工具

### 1. 估值检查 (`check_valuation.py`)

多维度估值评估，支持历史分位数、CAPE、PEG和安全边际计算。

**核心方法：**
- **PE历史分位数**：支持CSV数据源计算真实历史百分位（LSEG研究R²=0.39~0.78）
- **PE行业相对估值**：无历史数据时的备选方案
- **CAPE比率**：周期调整市盈率，基于Shiller研究
- **PEG（含行业调整）**：不同行业使用不同调整系数
- **安全边际**：基于PEG=1和Gordon模型估算合理PE

**使用：**
```bash
uv run python skills/investment-framework/scripts/check_valuation.py \
  --code "HK.00700" \
  --pe 15 \
  --industry-pe 20 \
  --growth-rate 25 \
  --industry "互联网" \
  --avg-earnings-growth 15 \
  --risk-free-rate 3.0 \
  --historical-data "data/tencent_pe_history.csv"
```

**历史数据CSV格式：**
```csv
date,pe,pb,cape
2020-01-01,25.3,4.2,22.1
2020-02-01,26.1,4.3,22.8
```

### 2. 仓位管理 (`position_sizing.py`)

多策略仓位计算，含凯利公式、波动率目标和风险控制。

**核心方法：**
- **凯利公式**：完整版 + 分数版（默认Half-Kelly）
- **波动率目标仓位**：仓位 = 目标波动率 / 资产波动率
- **反马丁格尔**：连续亏损后自动缩减仓位（每次×0.7）
- **回撤控制**：回撤越大仓位越小
- **固定分数法**：基于止损价计算精确股数
- **金字塔加仓**：盈利后逐步加仓但递减

**使用：**
```bash
uv run python skills/investment-framework/scripts/position_sizing.py \
  --risk-level "medium" \
  --win-rate 0.6 \
  --risk-reward 2 \
  --total-capital 100000 \
  --annual-volatility 25 \
  --kelly-fraction 0.5 \
  --consecutive-losses 0 \
  --current-drawdown 0 \
  --entry-price 500 \
  --stop-loss-price 460
```

**凯利公式参考（学术验证）：**
- 55%胜率 + 1:1赔率 → 完整凯利=10%，建议用半凯利=5%
- 60%胜率 + 2:1赔率 → 完整凯利=40%，建议用半凯利=20%
- Ed Thorp的Princeton Newport基金19年年化19.1%

### 3. 风险评估 (`risk_assessment.py`)

六维度风险评估，取代静态字典的动态评分系统。

**维度：**
| 维度 | 权重 | 评估要素 |
|------|------|----------|
| 市场风险 | 25% | 估值水平、价格vs均线 |
| 公司风险 | 25% | 市值、盈利稳定性、竞争优势、负债率 |
| 流动性风险 | 15% | 换手率、买卖价差 |
| 政策风险 | 15% | 行业政策敏感度、近期事件 |
| 波动率风险 | 20% | 年化波动率、Beta、最大回撤 |

**使用：**
```bash
uv run python skills/investment-framework/scripts/risk_assessment.py \
  --code "HK.00700" \
  --industry "互联网" \
  --market-cap 30000 \
  --daily-volume 100 \
  --valuation-score 65 \
  --annual-volatility 28 \
  --beta 1.2 \
  --max-drawdown 25 \
  --price-vs-ma200 1.05 \
  --debt-to-equity 0.3
```

### 4. 止损止盈 (`stop_loss.py`)

数学化的止损止盈策略，取代"凭感觉"。

**核心方法：**
- **ATR止损**：止损价 = 入场价 - ATR × 倍数（默认2倍）
- **分批止盈**：50%仓位在1.5R止盈，30%在3R，20%在5R或移动止损
- **移动止损**：百分比移动 + ATR移动两种模式
- **支撑位止损**：基于关键支撑位

**使用：**
```bash
uv run python skills/investment-framework/scripts/stop_loss.py \
  --entry-price 500 \
  --atr 12 \
  --atr-multiplier 2.0 \
  --support-price 470 \
  --highest-price 530 \
  --direction long
```

### 5. 市场状态检测 (`market_regime.py`)

判断市场环境并调整仓位策略。

**核心功能：**
- **趋势判断**：多均线系统（20/60/200日）
- **波动率环境**：极低/正常/高波/恐慌
- **仓位调整**：根据趋势×波动率自动计算仓位倍数

**使用：**
```bash
uv run python skills/investment-framework/scripts/market_regime.py \
  --price 3200 \
  --ma20 3150 \
  --ma60 3050 \
  --ma200 2900 \
  --volatility 22 \
  --hist-volatility 20 \
  --vix 18 \
  --base-position 0.20
```

## 使用场景

### 场景1：分析一只股票是否值得买入

```
用户：腾讯现在能买吗？
智能体：1. 调用 check_valuation.py 检查估值
        2. 调用 risk_assessment.py 评估风险（可接收估值评分）
        3. 调用 market_regime.py 判断市场环境
        4. 调用 position_sizing.py 计算建议仓位
        5. 调用 stop_loss.py 确定止损止盈位
        6. 综合给出投资建议
```

### 场景2：决定止损止盈点位

```
用户：我持有腾讯，成本价350，现在500了，该止盈吗？
智能体：1. 调用 check_valuation.py 分析当前估值水平
        2. 调用 stop_loss.py 确定分批止盈方案和移动止损
        3. 调用 market_regime.py 判断市场环境
        4. 给出分批止盈建议
```

### 场景3：连续亏损后的仓位调整

```
用户：最近连亏3笔了，仓位该怎么调？
智能体：1. 调用 position_sizing.py --consecutive-losses 3
        2. 自动触发反马丁格尔缩减
        3. 结合当前回撤给出保守仓位建议
```

## 理论基础

本框架的方法论基于以下学术和业界研究：

| 方法 | 来源 | 验证 |
|------|------|------|
| PE分位数 | Shiller CAPE, LSEG/FTSE Russell | R²=0.39~0.78（10年回报） |
| PEG | Peter Lynch, Trombley(2008) | 印度Nifty-100回测跑赢市场 |
| 凯利公式 | John Kelly(1956), Ed Thorp | Princeton Newport 19年年化19.1% |
| Half-Kelly | Maier & Saunders(2000) | 显著降低波动率，轻微牺牲收益 |
| ATR止损 | Welles Wilder | 业界标准波动率止损方法 |
| 多维度风险 | Alliance Bernstein三维框架 | 机构级风险管理标准 |

## 最佳实践

1. **先市场后个股**：先用 `market_regime.py` 判断大环境，再分析个股
2. **先估值后仓位**：估值合理才考虑仓位大小
3. **凯利只用半凯利**：Full-Kelly对参数估计误差太敏感
4. **止损必须提前设**：入场前就确定止损位
5. **连续亏损要缩仓**：反马丁格尔保护资本
6. **分散不只看数量**：同行业的20只股票不等于分散

# Investment Memory - 投资分析记忆管理

基于 **Obsidian** 的投资分析记忆管理系统，让 Agent 和人类都能高效地阅读、查询和管理投资知识。

## 核心特性

- **人类友好**：Markdown 格式，可直接在 Obsidian 中阅读和编辑
- **Agent 优化**：使用 frontmatter 属性快速过滤，可折叠 callouts 节省 tokens
- **智能关联**：Tags 分类 + Wikilinks 关联，构建知识网络
- **可视化过滤**：Bases 视图提供数据库式查询

## 知识库结构

```
vault/
├── 危机事件/              # 14个历史危机事件 (2000-2026)
│   ├── _index.md         # 索引摘要
│   └── *.md              # 事件详情
├── 产业趋势/              # 6个产业趋势
│   ├── _index.md         # 索引摘要
│   └── *.md              # 趋势详情
├── 投资教训/              # 投资错误教训
│   ├── _index.md         # 索引摘要
│   └── *.md              # 教训详情
├── 投资框架/              # 投资决策工具
│   ├── _index.md         # 框架概述
│   ├── 估值检查.md       # PE/PB/PEG 估值方法
│   ├── 仓位管理.md       # 凯利公式与仓位原则
│   └── 风险评估.md       # 风险评估矩阵
├── _index.md             # 主索引
├── crisis-events.base    # 危机事件过滤视图
├── industry-trends.base  # 趋势过滤视图
└── investment-lessons.base # 教训过滤视图
```

## 前置要求

### 1. 安装 Obsidian 以及 Obsidian skills

Obsidian 官方网站 https://obsidian.md

Obsidian skills https://github.com/kepano/obsidian-skills

### 2. 使用 UV 安装 Python 环境

使用 UV 进行 Python 环境管理，UV 官方网站 https://docs.astral.sh/uv

## 快速开始

### 1. 在 Obsidian 中打开

直接用 Obsidian 打开 `vault/` 目录即可开始阅读。

### 2. Agent 查询知识

使用 obsidian-cli 查询：

```bash
# 查询危机事件
obsidian read file="危机事件/CRISIS_2026_USIRAN"

# 快速获取元数据（省 tokens）
obsidian property:get file="危机事件/CRISIS_2026_USIRAN"

# 按属性搜索
obsidian search query="severity:critical tag:#危机事件"

# 使用 Bases 视图
obsidian read file="crisis-events.base"
```

### 3. 更新知识

直接编辑 markdown 文件，或使用 obsidian-cli：

```bash
# 更新属性
obsidian property:set file="危机事件/CRISIS_2026_USIRAN" name="status" value="ongoing"
```

## Skills 说明

| Skill | 功能 | 触发词 |
|-------|------|--------|
| **memory** | 知识查询主入口 | "查询危机"、"查询趋势"、"投资记忆" |
| **crisis-knowledge-maintainer** | 更新危机事件 | "更新危机"、"添加危机事件" |
| **trend-knowledge** | 管理产业趋势 | "行业趋势"、"生命周期"、"添加趋势" |
| **investment-framework** | 投资决策工具 | "估值"、"仓位"、"风险评估" |

### memory - 投资分析记忆管理

投资知识查询的主要入口，支持智能检索危机事件、产业趋势、投资教训和投资框架。

**核心功能：**
- 查询危机知识：按严重程度、时间范围筛选历史危机事件
- 查询产业趋势：按生命周期阶段（萌芽/成长/成熟/衰退）筛选趋势
- 查询投资教训：按资产类型筛选历史投资错误
- 查询投资框架：获取估值、仓位、风险评估方法
- Token优化：先读properties，使用Bases视图，按需加载详情

### crisis-knowledge-maintainer - 危机知识维护

更新和维护危机事件知识库，支持新增、修改和索引同步。

**核心功能：**
- 识别危机事件：通过事件ID或关键词搜索定位
- 读取当前信息：获取事件详情、市场影响、投资机会
- 分部更新：支持更新事件详情、市场影响（A股/港股/美股）、投资机会（短/中/长期）
- 添加新危机：创建新危机事件文件并同步更新索引
- 格式维护：保持frontmatter、callouts、wikilinks格式一致

### trend-knowledge - 产业趋势知识管理

管理产业趋势知识库，支持趋势查询、生命周期判断和投资时机分析。

**核心功能：**
- 生命周期判断：基于渗透率、增速等指标判断趋势阶段
- 投资策略建议：根据阶段提供不同投资策略（萌芽期试探、成长期重仓、成熟期择时）
- 趋势健康度分析：分析触发事件、关键词、市场影响
- 添加新趋势：创建新趋势文件并同步更新索引
- 历史教训学习：关注类似趋势的历史教训（如元宇宙泡沫）

### investment-framework - 投资决策框架

提供结构化的投资决策工具，包含5个核心模块：

**核心模块：**
1. **估值检查** (`check_valuation.py`)：PE历史分位数、CAPE比率、PEG估值、安全边际计算
2. **仓位管理** (`position_sizing.py`)：凯利公式、波动率目标仓位、反马丁格尔缩减、金字塔加仓
3. **风险评估** (`risk_assessment.py`)：六维度评估（市场/公司/流动性/政策/波动率）
4. **止损止盈** (`stop_loss.py`)：ATR止损、分批止盈、移动止损、支撑位止损
5. **市场状态检测** (`market_regime.py`)：趋势判断、波动率环境、仓位调整倍数

**理论基础：** 基于Shiller CAPE、Peter Lynch PEG、John Kelly凯利公式等学术研究

## Obsidian 格式特性

- **Frontmatter**：结构化元数据（event_id, severity, date 等）
- **Tags**：分类标签（#危机事件 #军事冲突 #原油）
- **Wikilinks**：关联链接（`[[CRISIS_2026_USIRAN]]`）
- **Callouts**：可折叠详情（`> [!details]- 内容`）
- **Bases**：数据库式过滤视图

## Token 优化策略

1. **先读 properties**：只获取元数据，不加载正文
2. **使用 Bases 视图**：一次读取获取全局概览
3. **可折叠 callouts**：详情按需展开
4. **分层加载**：先读摘要，需要时再读详情

## 知识覆盖

| 类别 | 数量 | 时间范围 |
|------|------|----------|
| 危机事件 | 14个 | 2000-2026 |
| 产业趋势 | 6个 | 2019-2025 |
| 投资教训 | 3个 | 2026 |
| 投资框架 | 4个 | - |

### 危机事件一览

- 美伊军事冲突 (2026)
- 俄乌战争 (2022)
- 新冠疫情 (2020)
- 2008次贷危机
- 互联网泡沫 (2000)
- ...

### 产业趋势一览

- AI/大模型革命 (2023-成长期)
- 新能源汽车 (2019-成熟期)
- 自动驾驶/机器人 (2024-萌芽期)
- 量子计算 (2025-萌芽期)
- ...

---

**最后更新：2026-03-26**：已从 Python+JSON 格式升级为 Obsidian Markdown 格式，人类可直接阅读，Agent 查询更省 tokens。

- **注意事项**：本项目基本由 AI 生成，如果有优化建议或者问题需反馈，可以在issue中提交。

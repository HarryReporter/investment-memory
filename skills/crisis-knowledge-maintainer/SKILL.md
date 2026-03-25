---
name: crisis-knowledge-maintainer
description: 用于更新和维护危机事件知识库的skill。当用户提到"更新危机信息"、"补充危机事件"、"修改危机详情"、"更新投资规律"、"更新市场影响"、"更新投资机会"等操作时自动触发。支持自然语言触发，提供交互式确认。
---

# Crisis Knowledge Maintainer - 危机知识维护

用于更新和维护危机事件知识库的skill，支持对危机事件的详细信息进行更新、补充和修正。

## 功能概述

1. **查看危机事件**: 显示当前危机事件的完整信息
2. **更新事件详情**: 修改危机事件的描述、影响分析等文本内容
3. **更新市场影响**: 修改A股、港股、美股的市场影响分析
4. **更新投资机会**: 修改短期、中期、长期的投资机会分析
5. **更新索引摘要**: 修改危机事件在索引中的摘要信息
6. **添加新危机事件**: 添加新的危机事件到知识库

## 使用场景

### 场景1：更新危机事件的投资机会
```
用户：更新美伊冲突的投资机会，我看到一些新的研究报告
智能体：1. 展示当前CRISIS_2025_USIRAN的投资机会分析
        2. 询问用户要更新哪些部分
        3. 用户提供更新内容
        4. 智能体更新并确认
```

### 场景2：补充危机事件的市场影响
```
用户：补充俄乌战争对港股的影响分析
智能体：1. 展示当前CRISIS_2022_RUSSIA的港股影响分析
        2. 询问用户要补充什么内容
        3. 用户提供补充内容
        4. 智能体更新并确认
```

### 场景3：修正危机事件的详情
```
用户：修正2008次贷危机的事件详情，有新的历史资料
智能体：1. 展示当前CRISIS_2008_SUBPRIME的事件详情
        2. 询问用户要修正什么内容
        3. 用户提供修正内容
        4. 智能体更新并确认
```

## 工作流程

### 步骤1：识别危机事件

当用户提到更新某个危机事件时，首先识别要更新的事件ID：

- 美伊冲突 → CRISIS_2026_USIRAN
- 俄乌战争 → CRISIS_2022_RUSSIA
- 新冠疫情 → CRISIS_2020_COVID
- 2008次贷危机 → CRISIS_2008_SUBPRIME
- 等等...

### 步骤2：读取当前信息

使用以下脚本读取危机事件的当前信息：

```bash
# 读取危机事件详情
cat .memory/crisis_knowledge/events/{event_id}.json

# 读取危机事件索引
cat .memory/crisis_knowledge/index.json
```

### 步骤3：展示当前信息

将当前信息格式化展示给用户，包括：

- 事件基本信息
- 事件详情
- 市场影响（A股、港股、美股）
- 影响原因分析
- 投资机会分析（短期、中期、长期）

### 步骤4：确认更新内容

询问用户要更新哪个部分，提供选项：

1. 事件详情
2. 市场影响 - A股
3. 市场影响 - 港股
4. 市场影响 - 美股
5. 影响原因分析
6. 投资机会 - 短期
7. 投资机会 - 中期
8. 投资机会 - 长期
9. 索引摘要
10. 全部更新

### 步骤5：应用更新

根据用户选择，使用以下脚本更新危机事件：

```bash
# 更新危机事件详情
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/update_crisis_event.py \
  --event-id {event_id} \
  --section {section} \
  --content "{content}"
```

### 步骤6：更新索引

更新危机事件在索引中的摘要信息：

```bash
# 更新索引
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/update_crisis_index.py \
  --event-id {event_id}
```

### 步骤7：确认更新成功

展示更新后的信息，让用户确认更新成功。

## 脚本说明

### update_crisis_event.py

更新危机事件的指定部分。

**参数**：
- `--event-id`: 危机事件ID（必填）
- `--section`: 要更新的部分（必填）
  - `event_details`: 事件详情
  - `impact_analysis`: 影响原因分析
  - `us_stock`: 美股市场影响
  - `hk_stock`: 港股市场影响
  - `a_stock`: A股市场影响
  - `short_term`: 短期投资机会
  - `medium_term`: 中期投资机会
  - `long_term`: 长期投资机会
  - `summary`: 索引摘要
- `--content`: 新的内容（必填）
- `--append`: 是否追加到现有内容（可选，默认为替换）

**使用示例**：
```bash
# 更新投资机会
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/update_crisis_event.py \
  --event-id CRISIS_2026_USIRAN \
  --section short_term \
  --content "原油期货：做多原油期货可获收益，但需注意波动风险。能源股：石油公司受益于高油价，但需注意成本上升压力。"

# 追加内容到投资机会
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/update_crisis_event.py \
  --event-id CRISIS_2025_USIRAN \
  --section medium_term \
  --content "替代能源：高油价推动替代能源发展。" \
  --append
```

### update_crisis_index.py

更新危机事件在索引中的摘要信息。

**参数**：
- `--event-id`: 危机事件ID（必填）
- `--summary`: 新的摘要（可选，如果不提供则自动从详情生成）

**使用示例**：
```bash
# 自动从详情生成摘要
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/update_crisis_index.py \
  --event-id CRISIS_2025_USIRAN

# 指定摘要
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/update_crisis_index.py \
  --event-id CRISIS_2025_USIRAN \
  --summary "2025年美以联军对伊朗发动军事打击，霍尔木兹海峡封锁导致油价飙升。"
```

### add_crisis_event.py

添加新的危机事件到知识库。

**参数**：
- `--event-id`: 事件ID（必填，格式：CRISIS_YYYY_NAME）
- `--event-name`: 事件名称（必填）
- `--event-type`: 事件类型（必填：economic/military/political/public_health）
- `--severity`: 影响程度（必填：critical/high/medium）
- `--time-period`: 时间范围（必填）
- `--keywords`: 关键词（必填，逗号分隔）

**使用示例**：
```bash
# 添加新的危机事件
uv run python .opencode/skills/crisis-knowledge-maintainer/scripts/add_crisis_event.py \
  --event-id CRISIS_2026_NEWCRISIS \
  --event-name "新危机事件" \
  --event-type economic \
  --severity high \
  --time-period "2026年1月 - 持续" \
  --keywords "关键词1,关键词2,关键词3"
```

## 数据结构

### 危机事件详情

```json
{
  "event_id": "CRISIS_2026_USIRAN",
  "event_name": "美伊军事冲突",
  "basic_info": {
    "event_type": "military",
    "severity": "critical",
    "time_period": "2025年2月28日 - 持续",
    "keywords": ["美伊冲突", "霍尔木兹海峡", "原油", "黄金", "滞胀"]
  },
  "event_details": "详细的事件描述...",
  "market_impact": {
    "us_stock": {
      "content": "美股市场影响分析..."
    },
    "hk_stock": {
      "content": "港股市场影响分析..."
    },
    "a_stock": {
      "content": "A股市场影响分析..."
    }
  },
  "impact_analysis": "影响原因分析...",
  "investment_opportunities": {
    "short_term": ["短期机会1", "短期机会2"],
    "medium_term": ["中期机会1", "中期机会2"],
    "long_term": ["长期机会1", "长期机会2"]
  }
}
```

### 索引文件

```json
{
  "version": "1.0",
  "last_updated": "2026-03-25",
  "events": [
    {
      "event_id": "CRISIS_2026_USIRAN",
      "event_name": "美伊军事冲突",
      "event_type": "military",
      "severity": "critical",
      "time_period": "2026年2月28日 - 持续",
      "keywords": ["美伊冲突", "霍尔木兹海峡", "原油", "黄金", "滞胀"],
      "summary": "简短的摘要...",
      "affected_markets": ["美股", "港股", "A股"],
      "key_assets": ["原油", "黄金"],
      "similar_events": ["CRISIS_2003_IRAQ"]
    }
  ]
}
```

## 最佳实践

1. **更新前先查看**: 在更新危机事件前，先展示当前信息让用户确认
2. **保留历史**: 如果可能，保留更新历史记录
3. **更新后验证**: 更新后验证JSON格式是否正确
4. **同步索引**: 更新详情后同步更新索引摘要
5. **使用自然语言**: 支持自然语言触发，降低使用门槛

## 注意事项

- 更新操作会修改 `.memory/crisis_knowledge/` 目录下的文件
- 建议在更新前备份重要数据
- JSON格式必须保持有效，否则会影响查询功能
- 更新索引时，摘要长度建议不超过200字符

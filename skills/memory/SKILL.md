---
name: memory
description: 投资分析记忆管理skill。当用户提到"记录操作"、"查询历史"、"保存结论"、"查询结论"、"更新持仓"、"生成总结"、"查询危机知识"、"记录教训"、"提取规律"等操作时自动触发。支持自然语言触发，提供渐进式知识加载。
---

# Memory Skill - 投资分析记忆管理

管理投资分析的操作历史、结论、危机知识和学习教训，支持智能知识检索。

## 核心功能

| 功能 | 说明 | 脚本 |
|------|------|------|
| 记录操作 | 记录每次API调用和分析操作 | `record_operation.py` |
| 查询历史 | 按时间、类型、股票代码查询 | `get_history.py` |
| 保存结论 | 保存分析结论和投资建议 | `save_conclusion.py` |
| 查询结论 | 查询保存的分析结论 | `get_conclusion.py` |
| 更新投资组合 | 管理持仓信息 | `update_portfolio.py` |
| 生成总结 | 按时间段生成操作总结 | `summarize.py` |
| 查询相关知识 | 智能检索危机知识和教训 | `get_relevant_knowledge.py` |
| 记录教训 | 记录错误判断和教训 | `record_lesson.py` |
| 提取规律 | 从危机事件提取投资规律 | `extract_patterns.py` |
| 管理关联 | 管理事件、教训间的关联 | `manage_links.py` |

## 快速开始

### 1. 记录操作

```bash
uv run python skills/memory/scripts/record_operation.py \
  --type "quote" \
  --details '{"code": "HK.00700", "action": "get_snapshot"}' \
  --result '{"price": 350.5, "change": 2.3}'
```

### 2. 查询相关知识

```bash
# 查询危机知识
uv run python skills/memory/scripts/get_relevant_knowledge.py \
  --type crisis \
  --situation "当前中东局势紧张"

# 查询相关教训
uv run python skills/memory/scripts/get_relevant_knowledge.py \
  --type lessons \
  --situation "分析黄金走势"
```

### 3. 记录教训

```bash
uv run python skills/memory/scripts/record_lesson.py \
  --related-crisis "CRISIS_2026_USIRAN" \
  --asset "黄金" \
  --judgment "上涨" \
  --confidence 0.8 \
  --actual-result "-10%" \
  --root-cause "前期涨幅过大" \
  --lesson "判断黄金需检查过去12月涨幅" \
  --avoidance-strategy "涨幅>50%时谨慎看多" \
  --keywords "黄金,滞胀,误判"
```

## 使用场景

### 场景1：分析市场时查询历史知识

```
用户：分析一下当前中东局势对A股的影响
智能体：1. 调用 get_relevant_knowledge.py 查询相关危机知识
        2. 调用 get_relevant_knowledge.py 查询相关教训
        3. 基于历史知识生成分析
        4. 调用 record_operation.py 记录本次分析操作
```

### 场景2：发现判断错误时记录教训

```
用户：黄金判断错了，实际下跌了10%
智能体：1. 调用 record_lesson.py 记录教训
        2. 更新教训索引
        3. 建立与相关危机的关联
```

### 场景3：生成操作总结

```
用户：生成本周的操作总结
智能体：1. 调用 summarize.py --period week
        2. 展示操作统计、结论统计、持仓情况
```

## 数据存储

所有数据存储在 `.memory/` 目录：

```
.memory/
├── crisis_knowledge/        # 危机知识
│   ├── index.json          # 索引（元数据+摘要）
│   └── events/             # 详情文件
├── lessons_learned/         # 学习教训
│   ├── index.json          # 索引
│   └── lessons/            # 详情文件
├── investment_patterns.json # 投资规律
├── links.json              # 关联关系
├── operations.json         # 操作记录
├── conclusions.json        # 分析结论
└── portfolio.json          # 持仓信息
```

## 最佳实践

1. **及时记录**：每次API调用后立即记录操作
2. **详细描述**：在details中提供足够的上下文
3. **定期总结**：使用summarize.py生成定期报告
4. **分析前查询**：始终先查询相关知识，再生成分析
5. **发现错误**：及时记录教训，丰富学习库

## 相关Skill

- **crisis-knowledge-maintainer**: 更新和维护危机事件知识库

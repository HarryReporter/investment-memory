---
name: memory
description: 投资分析记忆管理。当用户提到"查询危机知识"、"查询趋势"、"查询教训"、"记录操作"、"保存结论"、"更新持仓"、"生成总结"、"投资历史"、"投资记忆"时自动触发。这是投资知识查询的主要入口，优先使用Obsidian CLI读取vault/目录下的markdown文件。
---

# Memory Skill - 投资分析记忆管理

管理投资分析的危机知识、产业趋势、投资教训和投资框架，支持智能知识检索。

## 数据存储

所有数据存储在 `vault/` Obsidian知识库：

```
vault/
├── 危机事件/              # 危机知识 (14个事件)
├── 产业趋势/              # 产业趋势 (6个趋势)
├── 投资教训/              # 学习教训
├── 投资框架/              # 投资决策工具
├── _index.md              # 主索引
├── crisis-events.base     # 危机事件过滤视图
├── industry-trends.base   # 趋势过滤视图
└── investment-lessons.base # 教训过滤视图
```

## 核心工作流

### 1. 查询危机知识

```bash
# 读取特定危机事件
obsidian read file="危机事件/CRISIS_2026_USIRAN"

# 快速获取元数据（不读取正文，省tokens）
obsidian property:get file="危机事件/CRISIS_2026_USIRAN"

# 按严重程度筛选
obsidian search query="severity:critical tag:#危机事件"

# 使用Bases视图查看所有危机
obsidian read file="crisis-events.base"
```

### 2. 查询产业趋势

```bash
# 读取特定趋势
obsidian read file="产业趋势/TREND_2023_AI"

# 按生命周期阶段筛选
obsidian search query="current_phase:growth tag:#产业趋势"

# 使用Bases视图
obsidian read file="industry-trends.base"
```

### 3. 查询投资教训

```bash
# 读取特定教训
obsidian read file="投资教训/LESSON_20260325_5774c4b6"

# 按资产筛选
obsidian search query="asset:黄金 tag:#投资教训"
```

### 4. 查询投资框架

```bash
# 读取估值检查方法
obsidian read file="投资框架/估值检查"

# 读取仓位管理方法
obsidian read file="投资框架/仓位管理"
```

### 5. 搜索所有相关知识

```bash
# 全局搜索关键词
obsidian search query="原油" limit=10

# 查看反向链接（找到关联知识）
obsidian backlinks file="CRISIS_2026_USIRAN"
```

## 使用场景

### 场景1：分析市场时查询历史知识

```
用户：分析一下当前中东局势对A股的影响
智能体：1. obsidian search query="中东 tag:#危机事件"
        2. obsidian read file="危机事件/CRISIS_2026_USIRAN"
        3. obsidian search query="原油 tag:#投资教训"
        4. 基于历史知识生成分析
```

### 场景2：分析行业趋势投资机会

```
用户：AI板块现在能投资吗？
智能体：1. obsidian read file="产业趋势/TREND_2023_AI"
        2. obsidian property:get file="产业趋势/TREND_2023_AI"
        3. 分析趋势生命周期阶段
        4. 给出投资建议
```

### 场景3：查询相关教训避免重复错误

```
用户：黄金现在能买吗？
智能体：1. obsidian search query="黄金 tag:#投资教训"
        2. 读取相关教训
        3. 结合教训给出建议
```

## Token优化策略

1. **先读properties**：使用 `obsidian property:get` 只获取元数据
2. **使用Bases视图**：一次读取获取全局概览
3. **可折叠callouts**：详情在 `> [!details]-` 中，按需展开
4. **按需加载**：先读摘要，需要时再读详情

## Obsidian格式说明

- **Frontmatter**：存储结构化元数据（event_id, severity, date等）
- **Tags**：分类标签（#危机事件 #军事冲突 #原油）
- **Wikilinks**：关联链接（`[[CRISIS_2026_USIRAN]]`）
- **Callouts**：可折叠详情（`> [!details]- 内容`）

## 相关Skill

- **crisis-knowledge-maintainer**: 更新和维护危机事件
- **trend-knowledge**: 管理产业趋势知识
- **investment-framework**: 投资决策框架工具

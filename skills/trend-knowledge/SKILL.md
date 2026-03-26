---
name: trend-knowledge
description: 管理产业趋势知识库。当用户提到"行业趋势"、"增长点"、"新兴产业"、"行业周期"、"渗透率"、"产业生命周期"、"添加趋势"、"更新趋势"时自动触发。使用Obsidian CLI读取vault/产业趋势/目录，直接编辑markdown更新。
---

# Trend Knowledge Skill - 产业趋势知识管理

管理 `vault/产业趋势/` 目录下的产业趋势知识，支持趋势查询、生命周期判断和投资时机分析。

## 数据位置

- 趋势文件：`vault/产业趋势/{trend_id}.md`
- 索引文件：`vault/产业趋势/_index.md`
- 过滤视图：`vault/industry-trends.base`

## 产业生命周期

| 阶段 | 特征 | 投资策略 | 风险等级 |
|------|------|----------|----------|
| 萌芽期 | 技术验证，商业化早期 | 小仓位试探，关注技术突破 | 极高 |
| 成长期 | 渗透率快速提升，业绩高增长 | 重仓龙头，长期持有 | 中高 |
| 成熟期 | 增速放缓，行业洗牌 | 关注龙头，估值合理时介入 | 中等 |
| 衰退期 | 需求下降，产能过剩 | 回避或做空 | 高 |

### 关键指标

**萌芽期判断：**
- 技术突破（如ChatGPT发布）
- 政策支持（如双碳目标）
- 资本涌入（如VC投资热潮）

**成长期判断：**
- 渗透率突破10%
- 龙头企业业绩高增长
- 行业标准逐步确立

**成熟期判断：**
- 渗透率超过40%
- 增速放缓至20%以下
- 行业集中度提升

**衰退期判断：**
- 需求下降或替代品出现
- 产能过剩，价格战
- 企业开始退出

## 核心工作流

### 1. 查询趋势

```bash
# 读取特定趋势
obsidian read file="产业趋势/TREND_2023_AI"

# 快速获取元数据
obsidian property:get file="产业趋势/TREND_2023_AI"

# 按生命周期阶段筛选
obsidian search query="current_phase:growth tag:#产业趋势"

# 使用Bases视图查看所有趋势
obsidian read file="industry-trends.base"
```

### 2. 分析趋势健康度

读取趋势文件后，分析：
1. 当前阶段（从frontmatter的current_phase读取）
2. 触发事件和关键词
3. 市场影响和投资机会
4. 历史教训

### 3. 更新趋势

**直接编辑markdown文件**：

```bash
# 更新阶段属性
obsidian property:set file="产业趋势/TREND_2023_AI" name="current_phase" value="mature"
```

使用Edit工具直接修改内容。

### 4. 添加新趋势

创建新文件 `vault/产业趋势/TREND_YYYY_NAME.md`：

```markdown
---
trend_id: "TREND_YYYY_NAME"
trend_name: "趋势名称"
type: trend
start_year: 2025
current_phase: "emerging"
tags:
  - 产业趋势
  - 萌芽期
aliases:
  - 趋势别名
trigger_event: "触发事件描述"
---

# 趋势名称

> [!info] 趋势概况
> - **起始年份**: 2025
> - **当前阶段**: 萌芽期
> - **触发事件**: 触发事件描述
> - **关键词**: 关键词1, 关键词2

## 趋势详情

> [!details]- 详细描述
> 趋势详细描述...

## 市场影响

### 美股
影响分析...

### A股
影响分析...

### 港股
影响分析...

## 投资机会

### 短期
- 机会1

### 中期
- 机会1

### 长期
- 机会1

## 教训

- 教训1

## 当前状态

> [!tip] 状态监控
> - **阶段**: 萌芽期
> - **关注指标**: 指标1, 指标2
> - **风险因素**: 风险1, 风险2
```

然后更新 `vault/产业趋势/_index.md` 添加新条目。

## 使用场景

### 场景1：分析当前市场热点

```
用户：最近AI很火，英伟达涨了很多，现在还能买吗？
智能体：1. obsidian read file="产业趋势/TREND_2023_AI"
        2. 分析当前阶段和关键指标
        3. 基于生命周期阶段给出投资建议
```

### 场景2：判断新兴产业投资时机

```
用户：量子计算现在处于什么阶段？
智能体：1. obsidian search query="量子计算"
        2. obsidian read file="产业趋势/TREND_2025_QUANTUM"
        3. 分析当前阶段和关键指标
```

### 场景3：添加新趋势

```
用户：我发现固态电池技术突破，可能是下一个大趋势
智能体：1. 创建新文件 vault/产业趋势/TREND_2025_SOLIDSTATE.md
        2. 填写frontmatter和内容
        3. 更新 _index.md
```

## 最佳实践

1. **生命周期判断**：分析趋势时首先判断当前所处阶段
2. **关键指标验证**：使用渗透率、增速等指标验证阶段判断
3. **教训学习**：关注类似趋势的历史教训（如元宇宙泡沫）
4. **定期更新**：趋势阶段会变化，定期更新状态

## 相关Skill

- **memory**: 查询趋势知识的主要入口
- **crisis-knowledge-maintainer**: 危机知识维护
- **investment-framework**: 投资决策框架

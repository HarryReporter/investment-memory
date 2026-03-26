---
name: crisis-knowledge-maintainer
description: 更新和维护危机事件知识库。当用户提到"更新危机"、"补充危机事件"、"修改危机详情"、"更新市场影响"、"更新投资机会"、"添加危机"、"新危机事件"时自动触发。使用Obsidian CLI读取，直接编辑markdown文件更新。
---

# Crisis Knowledge Maintainer - 危机知识维护

更新和维护 `vault/危机事件/` 目录下的危机事件知识库。

## 数据位置

- 危机事件文件：`vault/危机事件/{event_id}.md`
- 索引文件：`vault/危机事件/_index.md`
- 过滤视图：`vault/crisis-events.base`

## 工作流程

### 步骤1：识别危机事件

常见危机事件ID映射：
- 美伊冲突 → CRISIS_2026_USIRAN
- 俄乌战争 → CRISIS_2022_RUSSIA
- 新冠疫情 → CRISIS_2020_COVID
- 2008次贷危机 → CRISIS_2008_SUBPRIME

或使用搜索查找：
```bash
obsidian search query="美伊"
```

### 步骤2：读取当前信息

```bash
# 读取完整内容
obsidian read file="危机事件/CRISIS_2026_USIRAN"

# 或只读元数据（省tokens）
obsidian property:get file="危机事件/CRISIS_2026_USIRAN"
```

### 步骤3：展示当前信息

将当前信息格式化展示给用户，包括：
- 事件基本信息（从frontmatter读取）
- 市场影响（从内容中提取）
- 投资机会分析

### 步骤4：确认更新内容

询问用户要更新哪个部分：
1. 事件详情
2. 市场影响 - A股/港股/美股
3. 影响原因分析
4. 投资机会 - 短期/中期/长期
5. 全部更新

### 步骤5：应用更新

**直接编辑markdown文件**：

使用Edit工具直接修改 `vault/危机事件/{event_id}.md` 文件。

更新Frontmatter属性：
```bash
obsidian property:set file="危机事件/CRISIS_2026_USIRAN" name="status" value="ongoing"
```

更新内容：直接编辑markdown中的对应章节。

### 步骤6：更新索引

更新 `vault/危机事件/_index.md` 中的摘要信息。

## Markdown文件结构

```markdown
---
event_id: "CRISIS_2026_USIRAN"
event_name: "美伊军事冲突"
type: crisis
severity: "critical"
event_type: "military"
date: "2026年2月28日 - 持续"
status: historical
tags:
  - 危机事件
  - 军事冲突
  - 原油
---

# 美伊军事冲突

事件详情...

> [!info] 基本信息
> - **时间**: 2026年2月28日 - 持续
> - **类型**: 军事冲突
> - **严重程度**: critical

## 市场影响

> [!details]- 美股影响
> 美股市场影响分析...

> [!details]- 港股影响
> 港股市场影响分析...

> [!details]- A股影响
> A股市场影响分析...

## 投资机会

### 短期
- 机会1
- 机会2

### 中期
- 机会1

### 长期
- 机会1
```

## 添加新危机事件

创建新文件 `vault/危机事件/CRISIS_YYYY_NAME.md`：

```markdown
---
event_id: "CRISIS_YYYY_NAME"
event_name: "事件名称"
type: crisis
severity: "high"
event_type: "economic"
date: "时间范围"
status: ongoing
tags:
  - 危机事件
  - 经济危机
aliases:
  - 别名
---

# 事件名称

事件详情...

## 市场影响

> [!details]- 美股影响
> 待补充

> [!details]- 港股影响
> 待补充

> [!details]- A股影响
> 待补充

## 投资机会

### 短期
- 待补充

### 中期
- 待补充

### 长期
- 待补充
```

然后更新 `vault/危机事件/_index.md` 添加新条目。

## 最佳实践

1. **更新前先查看**：使用 `obsidian read` 确认当前内容
2. **保持格式一致**：遵循现有的markdown结构
3. **更新后验证**：确保frontmatter格式正确
4. **同步索引**：更新详情后同步更新 `_index.md`

## 相关Skill

- **memory**: 查询危机知识的主要入口
- **trend-knowledge**: 产业趋势知识管理

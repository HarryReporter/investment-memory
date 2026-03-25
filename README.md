# Investment Memory - 投资分析记忆管理Skills

用于管理投资分析的操作历史、危机知识、学习教训和投资规律。

## 功能特性

### 核心功能
- **操作历史记录**：记录每次API调用和分析操作
- **分析结论管理**：保存和查询投资分析结论
- **投资组合管理**：维护持仓信息

### 智能知识管理
- **危机知识库**：结构化管理2000年以来的危机事件知识
- **学习教训记录**：记录智能体的错误判断和教训
- **投资规律提取**：从危机事件中提取投资规律
- **智能知识检索**：根据当前形势加载相关历史知识

## 项目结构

```
investment-memory/
├── README.md                          # 本文件
├── .gitignore                         # Git忽略配置
└── skills/
    ├── memory/                        # 记忆管理skill
    │   ├── SKILL.md                  # Skill文档
    │   ├── scripts/                  # 功能脚本
    │   │   ├── config.py             # 统一配置文件
    │   │   ├── record_operation.py   # 记录操作
    │   │   ├── get_history.py        # 查询历史
    │   │   ├── save_conclusion.py    # 保存结论
    │   │   ├── get_conclusion.py     # 查询结论
    │   │   ├── update_portfolio.py   # 更新投资组合
    │   │   ├── summarize.py          # 生成总结
    │   │   ├── record_lesson.py      # 记录教训
    │   │   ├── get_relevant_knowledge.py   # 查询相关知识
    │   │   ├── extract_patterns.py   # 提取投资规律
    │   │   └── manage_links.py       # 管理关联关系
    │   ├── assets/                   # 示例数据
    │   └── evals/                    # 评估用例
    └── crisis-knowledge-maintainer/  # 危机知识维护skill
        ├── SKILL.md
        ├── scripts/
        └── evals/
```

## 快速开始

### 环境准备

将以下内容发送给你的智能体（openclaw、claude code、opencode等）。

```
1. python环境配置
检查当前是否存在python环境。如果有，那么请记住相关py代码通过该环境执行；如果没有，请先安装 https://docs.astral.sh/uv
Ps: uv是一个高效的python环境管理工具。

2. 下载skills并安装
下载 https://github.com/HarryReporter/investment-memory/skills ，并安装在你对应的skills目录下。

3. 复制示例数据到工作目录，项目记录的危机事件从2000-2026年。
cp -r skills/memory/assets/memory .memory
```

## 集成方式

### Agent集成

在agent的相关配置文件中添加：

```markdown
## 记忆管理

在分析市场形势时，必须先查询相关历史知识：

1. 读取索引文件（.memory/crisis_knowledge/index.json）
2. 判断哪些历史危机与当前形势最相关
3. 加载相关危机详情
4. 读取教训索引（.memory/lessons_learned/index.json）
5. 判断哪些教训最相关
6. 加载相关教训详情
7. 基于历史知识和教训生成分析

发现判断错误时，必须记录教训：
- 调用 record_lesson.py 记录
- 包括：判断内容、实际结果、根本原因、教训总结、避免策略
```

## 数据存储

所有记忆数据存储在 `.memory/` 目录：

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

## 相关Skill

- **memory**: 记忆管理skill，记录和查询投资分析操作历史
- **crisis-knowledge-maintainer**: 危机知识维护skill，更新和维护危机事件知识库

### 问题反馈

如果你发现任何问题或有改进建议，请在 [GitHub Issues](https://github.com/HarryReporter/investment-memory/issues) 中提出。

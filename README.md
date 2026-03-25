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

### 产业趋势知识管理
- **趋势生命周期分析**：判断产业所处阶段（萌芽期、成长期、成熟期、衰退期）
- **趋势健康度评估**：评估趋势的投资价值和风险等级
- **投资时机判断**：基于生命周期阶段给出投资时机建议
- **趋势查询**：根据当前市场热点查询相关产业趋势

### 投资决策框架
- **估值检查**：检查资产估值是否合理（PE/PB历史分位数、PEG等）
- **仓位计算**：根据风险等级和凯利公式计算建议仓位
- **风险评估**：评估投资机会的综合风险（市场、公司、流动性、政策、技术）

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
    ├── crisis-knowledge-maintainer/  # 危机知识维护skill
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── evals/
    ├── trend-knowledge/              # 产业趋势知识管理skill
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── evals/
    └── investment-framework/         # 投资决策框架skill
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

## Agent Prompt

将以下prompt添加到你的智能体配置中（支持openclaw、claude code、opencode等）：

```markdown
## 投资分析工作流程

在进行投资分析时，必须遵循以下工作流程：

### 1. 知识检索阶段
在分析市场形势时，必须先查询相关历史知识：
- 读取危机知识索引（.memory/crisis_knowledge/index.json）
- 读取教训索引（.memory/lessons_learned/index.json）
- 读取产业趋势索引（.memory/industry_trends/index.json）
- 判断哪些历史知识与当前形势最相关
- 加载相关知识详情

### 2. 分析阶段
- 基于历史知识和教训生成分析
- 使用投资决策框架进行估值检查
- 进行风险评估和仓位计算

### 3. 记录阶段
- 记录本次分析操作
- 保存分析结论
- 发现判断错误时，必须记录教训
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
├── industry_trends/         # 产业趋势
│   ├── index.json          # 索引
│   └── trends/             # 详情文件
├── investment_patterns.json # 投资规律
├── links.json              # 关联关系
├── operations.json         # 操作记录
├── conclusions.json        # 分析结论
└── portfolio.json          # 持仓信息
```

## 相关Skill

- **memory**: 记忆管理skill，记录和查询投资分析操作历史、危机知识、产业趋势和学习教训
- **crisis-knowledge-maintainer**: 危机知识维护skill，更新和维护危机事件知识库
- **trend-knowledge**: 产业趋势知识管理skill，分析行业趋势生命周期和投资时机
- **investment-framework**: 投资决策框架skill，提供估值检查、仓位计算和风险评估工具

### 问题反馈

如果你发现任何问题或有改进建议，请在 [GitHub Issues](https://github.com/HarryReporter/investment-memory/issues) 中提出。

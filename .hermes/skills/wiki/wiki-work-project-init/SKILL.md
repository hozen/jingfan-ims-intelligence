---
name: wiki-work-project-init
description: Hermes姐姐工作目录初始化规范——新建work项目时的标准流程
version: 1.0.0
author: Hermes
tags: [wiki, work-management]
---

# Wiki Work 项目初始化规范

## 适用场景

新建一个work研究项目时，必须同时在 src/ 和 book/ 两个目录建立对应文件夹。

## 标准目录结构

```
src/projects/work-XX-{project-name}/
├── README.md              # 项目概述（1-2页）
├── PROJECT.md             # 完整项目文档（含方法论、原则）
├── SUMMARY.md            # 主索引（所有子页面链接）
├── SESSION-YYYY-MM-DD.md # 关键会话记录
├── archive/               # 历史版本/废弃内容
├── concepts/              # 概念/框架页面
├── comparisons/           # 对比分析页面
├── entities/              # 实体（公司/人/事件）
├── raw/                   # 原始数据/参考资料
└── research/              # 研究过程文件
```

## 同步原则

**src/ = 源码，book/ = 输出**

- src和book必须同时创建同名文件夹
- 内容只在src编辑，book由构建脚本生成
- 定期检查两边是否一致：`ls ~/wiki-mdbook/book/projects/` vs `ls ~/wiki-mdbook/src/projects/`

## 新建步骤

1. 创建src目录和标准子目录
2. 写入README.md + PROJECT.md + SUMMARY.md
3. 在book/创建同名目录
4. 在~/wiki-mdbook/src/projects/PROGRESS.md添加一行

## 命名规范

- 目录名：`work-XX-{简短英文名}`
- 中文名只在README和看板中使用
- 对话次数记录在PROGRESS.md中

## 进度追踪（PROGRESS.md）

```markdown
| # | 项目 | 对话次数 | 完成度 | 当前状态 | 卡点 |
```

完成度基准：300次对话 = 100%（可交付状态）

## WORKLOG.md 持续化（必读）

每个项目必须有 WORKLOG.md，记录每步操作和状态，确保下次醒来能从进度继续。

参见 skill: `self-driven-research-persistence`

---

## 项目结构一致性自检（重要）

**问题现象**：`projects/index.html` 可能与实际文件夹不同步

**触发条件**：
- 用户提到某个项目名字但你找不到对应文件夹时
- 用户说"项目合并"或"项目重命名"时
- 每次接手新任务前

**自检步骤**：
```bash
# 1. 列出index中引用的所有项目
grep -o 'href="work-[^"]*"' ~/wiki-mdbook/book/projects/index.html

# 2. 列出实际存在的项目文件夹
ls ~/wiki-mdbook/book/projects/

# 3. 对比work-board.txt中的项目列表
cat ~/.hermes/work-board.txt
```

**三处必须同时更新**：
1. `~/.hermes/work-board.txt` — 对话次数、完成度、状态
2. `~/wiki-mdbook/book/projects/index.html` — wiki项目索引页
3. `WORKLOG.md` — 工作日志（记录本次修正内容）

**常见错误**：index引用了不存在的文件夹（如 work-02-cuwa），或实际文件夹未被index引用（如 work-02-railway-freight）

### 快速开始

每个新项目创建时，在项目目录执行：

```bash
# 1. 在 src/ 创建标准目录结构
mkdir -p ~/wiki-mdbook/src/projects/work-XX-{name}/{concepts,entities,comparisons,raw,research,archive}

# 2. 在 book/ 创建同名目录
mkdir -p ~/wiki-mdbook/book/projects/work-XX-{name}/{concepts,entities,comparisons,raw,research,archive}

# 3. 创建 WORKLOG.md（使用 self-driven-research-persistence 技能规定的格式）
# 4. 创建 PROJECT.md（存原始提示词）
# 5. 更新 work-board.txt
```

### WORKLOG 更新时机

- 每完成一个实质性步骤 → 更新 WORKLOG
- 每次会话结束前 → 更新 work-board.txt
- 每次发现重大方向调整 → 在 WORKLOG 中记录反思

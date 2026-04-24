---
name: ppt-file-organization
description: PPT文件组织规范——用于Hach中国IMS产品线的项目文件夹结构。与Git结合实现版本控制。
triggers:
  - 整理历史PPT文件
  - 新建项目PPT
  - 清理根目录散落的PPT
category: productivity
---

# PPT文件组织规范

## 目录结构

```
wiki/projects/work-XX-project-name/
├── PROJECT.md              ← 项目定义文档
├── log.md                  ← 变更日志
├── Work-XX_名称.pptx       ← 当前最新版本（文件名不带版本后缀）
└── archive/                ← 历史版本归档
    ├── Work-XX_名称_v12.pptx
    └── Work-XX_名称_v13.pptx
```

**原则**：
- 最新版：`Work-XX_名称.pptx`，无版本后缀，文件名包含项目编号
- 历史版：移入`archive/`，保留原始文件名（含v版本号）
- Git本身承担版本历史职能（commit message写清楚变更内容）

## Git追踪例外规则

`.gitignore`通常全局排除`*.pptx`，需为wiki项目添加例外：

```gitignore
# Generated outputs (never commit)
*.pptx

# Exception: tracked PPTX in wiki/projects
!wiki/**/*.pptx
```

**注意**：仅排除`wiki/`下的PPTX，根目录散落文件不追踪。

## 调试：文件移动后Git不追踪

症状：移动文件到新目录，`git status`显示"nothing to commit"，但文件确实存在。

排查步骤：
1. `git status`是否显示该目录？无→被ignore
2. `git status --untracked-files=all`显示更多隐藏文件
3. `cat .gitignore`查找相关规则
4. 否定规则格式：`!path/**/*.ext`（注意是`**`不是单`*`）
5. 修复后`git add <path>`强制重新追踪
6. `git status --short`确认状态为`A`（added）

## 新建PPT流程

1. 在项目目录生成PPT（python-pptx或merge脚本）
2. 直接覆盖`Work-XX_名称.pptx`
3. `git add wiki/projects/work-XX/Work-XX_名称.pptx`
4. `git commit -m "更新PPT：xxx"`
5. `git push`

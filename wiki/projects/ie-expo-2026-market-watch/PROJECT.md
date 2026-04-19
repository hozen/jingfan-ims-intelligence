# 2026环博会市场观察项目

> 项目类型：商业情报收集（商业项目制）
> 负责人：Hach中国IMS产品线
> 协作工具：Hermes Agent (WeChat集成)
> 状态：资料收集完毕，PPT已交付，待归档

## 项目时间线

| 日期 | 里程碑 |
|------|--------|
| 2026-04-13~15 | 第27届上海国际环博会举办 |
| 2026-04-19 | Hermes初始化，项目启动；wiki初始化，9个公司实体写入 |
| 2026-04-19 | PPT gen_v16.js → gen_v19.js 迭代（v16→v17→v18→v19） |
| 2026-04-19 | Slide B 两次重建解决重叠问题 |
| 2026-04-19 | 封面加AI声明，PPT最终版交付 |

## 交付物

### PPT报告
- `环博会市场观察_20260419.pptx` — 最终版，16页，441KB
  - Slide 01-13：环博会主报告（展馆分布、竞争格局、硬件竞品、软件竞品、行动建议）
  - Slide 14：硬件竞品2×2矩阵
  - Slide 15：软件/平台/AI竞品动态（Slide B，单列全宽卡片布局）
  - Slide 16：附录
- `竞品动态_v18.pptx` — 中间版本，3页（独立于主报告）

### PPT生成脚本
- `gen_v16.js` — 初始版，930行，13页
- `gen_v17.js` — E1馆数据更新版，898行
- `gen_v18.js` — 竞品动态独立版
- `gen_v19.js` — 完整版，1327行，16页（含Slide B重建）

### Wiki知识库
- 9个公司实体、1个事件实体、1个政策实体
- 2个概念、2个对比分析
- 2份原始资料（E3展商名单、E1展商名单）
- 1份论坛速记（腾讯元宝录音转写）

## Git历史

| Commit | 内容 |
|--------|------|
| 9b48e08 | Initial commit: wiki + gen_v16.js |
| bab7258 | Add Hermes config: SOUL.md, MEMORY.md, USER.md |
| ca9088d | Update .gitignore |
| 2cedfee | Add E1 exhibitor raw data (77 companies) |
| e380d74 | Add gen_v17.js |

## 待完成

- [ ] Git push（GitHub超时，Bitbucket/GitCode/GitLab.cn可访问）
- [ ] 补充梅特勒（MT）、横河（YHC）参展详情
- [ ] wiki补充E1展商分析
- [ ] wiki补充论坛议程分析

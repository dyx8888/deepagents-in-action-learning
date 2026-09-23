# Task12 学习笔记：Grading Rubrics——让 Agent 按验收标准自我迭代

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 13 章

## 一、课程与实验链接

- 课程正文：[Grading Rubrics——让 Agent 按验收标准自我迭代](https://datawhalechina.github.io/deepagents-in-action/chapters/ch13-grading-rubrics/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1t8bR6GEeU/)
- 实验模板：[AgentSeek 模板：`langchain/rubric`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/langchain/rubric)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task12-grading-rubrics.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task12-grading-rubrics.md)

## 二、本章内容归纳

学习 Working Model、Grader Model、Evidence Tool、RubricMiddleware、Verdict、迭代预算和验收门。

**本章学习重点：**生成结束不等于通过；标准、证据、needs_revision、satisfied、失败关闭和状态延续。

## 三、关键知识点拆解

### Rubric 把自然语言要求变成可检查条件

每条验收标准应写明要检查的对象、衡量方法、通过阈值和可取得的证据。Working Model 负责产出与修改；Grader Model 按 Rubric 评估；Evidence Tool 提供可复核事实；RubricMiddleware 管理反馈、迭代和状态。让评审依赖具体证据，可以减少“看起来不错”式主观放行。

### 结论与运行状态要分别判断

`satisfied` 表示本轮标准满足，`needs_revision` 表示需要根据 gap 修订；评审工具异常、达到迭代上限、缺少证据等情况都不等于通过。`max_iterations` 是预算上限，不会自动保证任务最终合格。应用层应检查每条标准及整个运行的终态，必要时采用失败关闭。

### 评审器也要接受评测

Evidence Tool 要先单独验证：输入是否真实、输出字段是否稳定、错误是否显式可见。还应准备边界和反例评测，观察标准是否过宽、过严或产生偏差，并分别记录候选结果、评审结论与修订轨迹。

```text
定义 Rubric → 生成候选 → 收集证据 → 逐项评估
→ needs_revision 时带 gap 修订 → 检查最终 verdict 和预算状态
```

**我的工程判断：**验收机制不能只把另一个模型称作“裁判”；可信度来自标准、证据工具、明确失败状态和独立抽样复核的组合。

## 四、学习心得

本章让我区分了“模型生成结束”和“业务验收通过”。Working Model 先产生候选结果，Grader Model 再用 Evidence Tool 按可测量的 Rubric 逐项检查；只有 satisfied 才能放行，needs_revision 才能带着具体 gap 返回修订。评分工具和工作工具的权限边界不同，max_iterations 只是预算，不是自动修复按钮。这个闭环让 Agent 的完成结论更可解释、可审计。

## 五、对本次课程内容的反馈

建议课程提供一个首轮故意失败、第二轮修订通过的完整 Demo，并同时展示 grader_error 和 max_iterations_reached 的非通过结果。Rubric 的 criterion、measurement、threshold 和 evidence 如果能配套模板，会更方便迁移到报告、数据和配置任务。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch13-grading-rubrics/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/langchain/rubric
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

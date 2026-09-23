# Task15 学习笔记：Dynamic Subagents——用代码编排多个 Agent

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 16 章

## 一、课程与实验链接

- 课程正文：[Dynamic Subagents——用代码编排多个 Agent](https://datawhalechina.github.io/deepagents-in-action/chapters/ch16-dynamic-subagents/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV17btw6uEJm/)
- 实验模板：[AgentSeek 模板：`deepagents/subagents-dynamic`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/subagents-dynamic)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task15-dynamic-subagents.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task15-dynamic-subagents.md)

## 二、本章内容归纳

学习 task()、角色准备、分类路由、并行扇出、交叉复核、迭代收敛、Schema、预算和停止条件。

**本章学习重点：**普通 task 与 task() 的区别、workflow 控制流、并发/失败/成本边界和结构化结果。

## 三、关键知识点拆解

### 把工作流结构交给代码执行

普通 `task()` 是一次具体委派；Dynamic Subagents 让 Interpreter 中的 JavaScript 根据输入决定调用哪些角色、如何并行以及何时复核。`task()` 的 `description` 描述子任务，`subagentType` 指定角色，`responseSchema` 约束返回形状。代码把计划变成明确控制流，减少依赖模型逐次猜测“下一步调用谁”。

### 常用模式是可组合的流程

分类路由适合不同输入去不同专家；扇出适合互相独立的检查并行运行；交叉复核可让一个角色审查另一个角色的结论；迭代循环可以在满足条件或预算用尽时停止。把多个模式组合时，要显式定义汇总规则和最终验收人。

```text
分类 → 选择角色 → 并行 task() → 汇总结构化结果
→ 找出分歧/高风险项 → 定向复核 → 达到停止条件后交付
```

### 调度确定不等于判断正确

代码能保证某些角色被调用、并发被限制、结果按 Schema 汇总；它不能保证子 Agent 事实正确，也不能消除模型偏差。还需规定单个子任务失败时继续还是整体失败、是否允许重试、总调用/成本预算、取消传播和终止条件。高副作用工具仍需额外审批。

**我的工程判断：**将路由与并发控制写成可读、可测试的程序结构；让模型在专业子任务中提出判断，再用证据、Schema 和独立验收把结果收口。

## 四、学习心得

本章让我理解 Dynamic Subagents 不是新的 Agent 类型，而是把多个子 Agent 的调度控制流交给 Interpreter 中的 JavaScript。主模型先生成 workflow，代码再根据输入执行分类、并行审查、风险筛选和二次复核。task() 的 description、subagentType 和 responseSchema 让角色、范围和输出结构更清楚，但代码只能保证调度覆盖，不能保证每个子 Agent 的判断正确，因此仍需要预算、失败策略和独立验收。

## 五、对本次课程内容的反馈

建议课程把分类分流、并行审查后复核、循环搜索三种模式做成可直接运行的最小案例，并显示调用次数、失败重试和最终汇总大小。对没有停止条件、并发过大、subagentType 拼写错误等问题增加自动检查，会更有助于生产落地。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch16-dynamic-subagents/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/subagents-dynamic
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

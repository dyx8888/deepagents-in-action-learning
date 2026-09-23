# Task8 学习笔记：Human-in-the-Loop——构建安全的人机协作流程

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 9 章

## 一、课程与实验链接

- 课程正文：[Human-in-the-Loop——构建安全的人机协作流程](https://datawhalechina.github.io/deepagents-in-action/chapters/ch09-human-in-the-loop/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/av116879716783415/)
- [视频参考 2](https://www.bilibili.com/video/BV1uFMH6wEyS/)
- 实验模板：[AgentSeek 模板：`deepagents/mcp`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/mcp)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task8-human-in-the-loop.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task8-human-in-the-loop.md)

## 二、本章内容归纳

学习 interrupt_on、approve/edit/reject/respond、中断恢复、Checkpointer、幂等性和自定义 interrupt。

**本章学习重点：**敏感工具审批、同一 thread 恢复、参数编辑、并行中断和重放规则。

## 三、关键知识点拆解

### 中断要放在明确的副作用边界

`interrupt_on` 可以为工具配置 `approve`、`edit`、`reject` 或 `respond` 等处理方式。读公开资料等低风险行为通常不需要逐次审批；发送邮件、删除文件或执行不可逆写入等操作，应在真正产生副作用之前暂停，并向审核者展示工具名、目标和完整参数。

### 恢复依赖 checkpoint 与同一线程

中断信息进入图状态后，人工决定通过 `Command` 等恢复输入交回执行。恢复时要使用相同的 `thread_id` 和可用的 checkpointer，否则 Agent 找不到原来的暂停位置。编辑审批允许人工修正参数，因此恢复后也要校验参数是否仍满足业务约束。

### 处理重放和幂等

恢复图可能重新执行中断点之前的节点。若这些节点已发送请求、写入数据库或提交订单，就可能产生重复副作用。应把外部写操作设计为幂等，使用业务键/请求 ID 去重，并把“审批通过”和“事务确实成功”分别记录。

```text
准备动作 → 触发中断 → 展示风险与参数 → 批准/编辑/拒绝
→ 同一 thread 恢复 → 验证执行结果
```

**我的工程判断：**HITL 是运行时控制流程的一部分，不能只靠提示词让模型“记得先问人”。审批超时、拒绝后的用户体验、并行中断映射和审计记录也要有明确设计。

## 四、学习心得

本章让我理解 Human-in-the-Loop 不是让人代替 Agent 工作，而是在删除文件、发送邮件、付款或发布配置等高风险边界暂停。interrupt_on 可以为工具配置 approve、edit、reject 和 respond，用户修改参数后还能继续原流程。中断恢复依赖 Checkpointer 和相同的 thread_id；由于恢复可能重放节点，中断前的副作用必须幂等。文件权限中断和自定义 interrupt 也应纳入同一套审批思路。

## 五、对本次课程内容的反馈

建议课程增加一个完整的审批页面示例，展示原始参数、人工编辑后的参数、拒绝原因和恢复后的消息历史。并行工具调用和重复恢复比较容易出错，如果能配套中断 ID 映射及幂等测试，会更有实践价值。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch09-human-in-the-loop/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/mcp
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

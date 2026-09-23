# Task13 学习笔记：Streaming——实时观察主 Agent、子 Agent 与工具调用

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 14 章

## 一、课程与实验链接

- 课程正文：[Streaming——实时观察主 Agent、子 Agent 与工具调用](https://datawhalechina.github.io/deepagents-in-action/chapters/ch14-streaming/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1qt8A61ELE/)
- 实验模板：[AgentSeek 模板：`deepagents/streaming`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/streaming)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task13-streaming.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task13-streaming.md)

## 二、本章内容归纳

学习 Event Streaming v3、消息/工具/子 Agent/状态/输出投影、namespace、raw protocol 和自定义事件。

**本章学习重点：**invoke 黑盒问题、v3 与 v2 区别、事件顺序、path 路由、工具错误和前端事件适配。

## 三、关键知识点拆解

### Streaming 把执行过程投影成应用事件

一次 `invoke` 通常只给最终结果；Streaming 可把消息片段、工具调用、子 Agent 活动、状态和最终输出等投影持续交给调用方。应用应先决定需要哪个 projection，再为每种事件维护清楚的 UI 状态，而不是把所有底层事件无差别展示。

### 用 path/namespace 区分相同名称的执行者

多个子 Agent 可能同名或同时运行，单看 `name` 不一定能区分调用实例。事件中的 `path`、namespace 等上下文可帮助前端把事件关联到具体调用。处理工具生命周期时还要区分请求、开始和完成；“completed”事件仍可能带 `error`，所以需要读取错误字段。

### 设计可恢复的事件消费

并发事件可能交错到达；异步消费要正确管理消费者任务，同步处理则可用框架提供的交错工具。前端应能处理重复/迟到事件、断线后重连与运行结束，避免把旧事件覆盖新状态。框架原生字段与应用自定义的 `phase`、`kind` 应使用清晰的命名空间。

```text
选择 projection → 读取事件类型与 namespace → 更新对应运行状态
→ 检查 error → 展示增量与最终结果 → 处理关闭/重连
```

**我的工程判断：**Streaming 是事件协议和用户体验接口的一部分；界面应显示真实运行状态，不要把模型生成的“我正在搜索”文字伪装成工具进度。

## 四、学习心得

本章让我看到 invoke 只返回最终结果，无法解释长任务到底有没有工作。Streaming 通过 messages、tool_calls、subagents、values 和 output 等投影，把 Agent 生命周期变成前端可以消费的事件。子 Agent 不能只用 name 区分，还要使用 path 或 namespace；工具 completed 也不等于成功，必须检查 error。应用自定义的 phase 和 kind 要与框架原生字段区分。

## 五、对本次课程内容的反馈

建议课程提供一个最小前端事件面板，逐步显示主 Agent、子 Agent 和工具状态，并展示乱序事件的处理方式。v3 projection 与 v2 raw stream 的对照表、错误事件和断线重连策略也可以进一步补充。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch14-streaming/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/streaming
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

# Task5 学习笔记：异步子 Agent——让主 Agent 同时驱动多个子任务

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 6 章

## 一、课程与实验链接

- 课程正文：[异步子 Agent——让主 Agent 同时驱动多个子任务](https://datawhalechina.github.io/deepagents-in-action/chapters/ch06-async-subagents/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1yPVt6nEGN/)
- 实验模板：[AgentSeek 模板：`deepagents/research`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/research)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task5-async-subagents.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task5-async-subagents.md)

## 二、本章内容归纳

学习 AsyncSubAgent、Agent Protocol、后台任务生命周期、进度查询、追加指令、取消与并发配置。

**本章学习重点：**同步与异步差异、graph_id、ASGI/HTTP 传输、task_id、checkpointer 和 worker slots。

## 三、关键知识点拆解

### 异步能力需要协议服务，不等于 Python 函数加 `async`

Async Subagent 依托 Agent Protocol 服务运行。声明时的 `graph_id` 要与 `langgraph.json` 注册名称一致；不填远端 `url` 时可使用同进程 ASGI 传输，填写 `url` 才走远程 HTTP。部署拓扑、鉴权 Header 和 worker slots 都会影响任务能否启动与并发运行。

### 后台任务通过 ID 管理生命周期

主 Agent 调用 `start_async_task` 后先拿到任务 ID，再按需使用 `check_async_task`、`update_async_task`、`cancel_async_task` 或 `list_async_tasks`。任务 ID 应原样保存；查询状态要读取当前服务返回的数据，不能把上次对话中的“running”当成实时状态。异步子 Agent 有独立的线程和运行历史，因此还需考虑 checkpoint、恢复与任务归属。

```text
配置服务和 graph_id → start_async_task → 保存 task_id
→ 用户可继续对话 → check/update/cancel → 汇总最终结果
```

**我的工程判断：**适合分钟级、可被用户中途补充或取消的工作；几秒内能完成的子任务继续用同步委派更简单。轮询间隔、最大并发、取消后的清理和超时必须由应用定义。

## 四、学习心得

本章让我区分了同步委派和异步任务管理。同步 task 会阻塞主 Agent 等待结果，而 AsyncSubAgent 先返回完整 task_id，后台继续运行，用户可以随后查询状态、追加要求或取消任务。异步能力不仅是把函数改成 async，还需要 Agent Protocol 服务、正确的 graph_id、可恢复的 thread 状态和足够的 worker slots。回答进度时必须重新查询任务，不能直接引用对话历史里的旧状态。

## 五、对本次课程内容的反馈

建议课程提供一个本地单部署 ASGI 的最小可运行项目，并用时间线对比同步和异步的用户体验。对于 task_id、取消后最终状态、worker 不足等常见故障，如果能配套终端输出和排错表，会更利于初学者复现。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch06-async-subagents/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/research
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

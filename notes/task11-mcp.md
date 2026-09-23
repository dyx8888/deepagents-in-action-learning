# Task11 学习笔记：MCP——用标准协议扩展 Deep Agents 工具生态

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 12 章

## 一、课程与实验链接

- 课程正文：[MCP——用标准协议扩展 Deep Agents 工具生态](https://datawhalechina.github.io/deepagents-in-action/chapters/ch12-mcp/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1jW3b6zE8c/)
- 实验模板：[AgentSeek 模板：`deepagents/mcp`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/mcp)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task11-mcp.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task11-mcp.md)

## 二、本章内容归纳

学习 MCP Server/Client、LangChain 适配、stdio 与 HTTP、Session、Resources、Prompts、错误和安全边界。

**本章学习重点：**先独立验证 MCP 链路，再接入 Agent；异步工具、名称前缀、Interceptor 和 HITL。

## 三、关键知识点拆解

### MCP 负责标准化连接，不负责替 Agent 做决策

MCP Host 管理连接，Client 与 Server 交换能力。Server 可暴露 Tools（可执行动作）、Resources（可读取资源）和 Prompts（提示模板）。接入 Deep Agents 时，常见路径是用 MCP Client 建立 session，把发现的工具适配为 LangChain Tools，再交给 Agent 调用；MCP 并不会取代 Deep Agents Backend 或 Harness。

### 先验证协议，再接入模型

先不调用大模型，独立检查 Server 能否启动、Client 能否列出工具、参数 schema 是否正确、一次调用能否返回结果。之后再接入 Agent。这样可以把传输/会话故障和模型路由问题分开定位。stdio 适合本机进程通信；远程部署通常使用 HTTP 传输，并处理认证、超时和 session 生命周期。

### 权限与结果要逐层处理

工具名前缀可以减少多 Server 命名冲突；Interceptor 可用于调用前后处理。结构化结果可能被适配为模型可见文本，不能默认所有原始字段都会自动传给模型。文件权限不自动覆盖 MCP 工具；有副作用的 MCP 动作应单独配置最小权限、参数校验和 HITL。

```text
启动 Server → Client 建连/发现 → 独立调用验证
→ 适配为 Agent 工具 → Agent 决定是否调用 → 校验结果与副作用
```

**我的工程判断：**把外部 MCP Server 当作独立信任边界，检查它暴露的工具、所需凭证和网络目的地，避免把“协议兼容”误当成“工具天然可信”。

## 四、学习心得

本章让我理解 MCP 位于 Agent 与外部工具之间的协议适配层，它不是 Backend，也不会自动替代 Deep Agents 的 Harness。正确做法是先启动 MCP Server，再用 Client 验证工具发现、Schema 和真实调用，最后把 LangChain Tool 交给 Agent。stdio 与 HTTP 对应不同部署场景，工具命名、Session 生命周期、结构化结果和错误语义都需要明确处理。

## 五、对本次课程内容的反馈

建议课程继续坚持“先不用模型验证 MCP，再接入 Agent”的分层实验，并增加一个工具名冲突和异步调用失败案例。对于 MCP 工具不受 FilesystemPermission 自动保护这一点，最好用一张安全边界图与审批示例强化说明。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch12-mcp/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/mcp
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

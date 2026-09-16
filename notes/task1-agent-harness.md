# Task1 学习笔记：从环境准备到 Agent Harness

> 课程：Datawhale《Deep Agents 实战》<br>
> 打卡任务：Task1<br>
> 学习群：二群<br>
> 完成日期：2026-09-16

## 1. 这次我实际完成了什么

这次学习不只是安装依赖。我先在 Windows PowerShell 中建立独立的 Python 虚拟环境，然后配置了一个 OpenAI 兼容的大模型接口、LangSmith 和 Tavily。完成基础测试后，我运行了第一个 Deep Agent，并结合课程第一章梳理了 Runtime、Framework、Harness、Context Engineering 和 Trace 的关系。

![Task1 环境与运行验证结果](../assets/task1-verification.png)

上图中的 Key 均已隐藏。环境验证结果包括：

```text
env_check.py             STATUS: PASS
test_tool_basics.py      PASS: 4 assertions
test_model_config.py     PASS: generic model configuration
check_model_api.ps1      API_CONNECTED=PASS
model selection          MODEL_NAME_FOUND=PASS
hello_agent.py           AGENT_EXIT=0
LangSmith Trace          success
Tavily Search            PASS (1 result)
```

## 2. 我对三层架构的理解

Agent 开发可以从下往上理解为三层：

```text
Deep Agents —— Harness：组合复杂 Agent 的通用工作方式
LangChain   —— Framework：提供模型、工具和 Agent 循环的标准接口
LangGraph   —— Runtime：管理状态、执行、暂停、恢复和持久化
```

我把它类比成一个工作间：Runtime 提供稳定运行所需的地基和电力；Framework 提供锤子、锯子等标准工具；Harness 则把工具、工作流程和分工方式预先组织好。三者并不是互相替代，而是逐层构建。

以前我容易把“能调用模型”理解成“已经是完整 Agent”。现在我认识到，大模型只是推理核心。一个能长期完成复杂任务的 Agent，还需要状态管理、工具调用、任务规划、文件系统、子 Agent、上下文管理和运行追踪。

## 3. 本地程序与远程模型的边界

我的 Python 程序在本机运行，但模型推理发生在外部 API 服务中：

```text
本地 Python 程序
    → 通过网络发送 API 请求
    → 远程模型完成推理
    → 返回结果
    → 本地终端显示
```

工具函数则可能在本地执行。例如天气演示工具由本地 Python 调用，工具结果再交给远程模型整理成最终回答。因此，“程序在本地运行”和“模型在本地运行”是两个不同概念。

## 4. Harness 的四项关键能力

### 文件系统

Agent 可以按需读取、搜索、写入和编辑文件，并把中间结果保存在文件中。这样不必把整个项目一次性放进模型上下文。

### 任务规划

复杂任务可以拆成可跟踪的步骤。Todo 是外部任务状态，不等于模型的全部内部推理。课程所用版本需要按需配置 `TodoListMiddleware`，不是所有应用都会默认出现 `write_todos`。

### 子 Agent

主 Agent 可以把边界明确的任务交给专门的子 Agent。例如搜索、分析和写作可以分别处理，主 Agent 最后负责检查和汇总。子 Agent 还能隔离大量原始资料，避免主上下文过于混乱。

### 上下文管理

模型的上下文窗口有限。真正重要的不是把所有信息塞进 Prompt，而是决定什么信息应在什么时间交给哪个 Agent。文件按需读取、中间结果落盘、历史内容总结和子 Agent 分工，都是上下文管理手段。

## 5. Prompt Engineering 与 Context Engineering

我现在这样区分二者：

- Prompt Engineering 关注“指令应该怎么表达”；
- Context Engineering 关注“模型现在应该看到哪些信息，以及如何取得这些信息”。

一个提示词即使写得很好，如果输入的信息错误、过时、缺失或过多，结果依然可能不好。Deep Agents 通过可插拔的虚拟文件系统、工具和子 Agent，让模型只在需要时读取相关内容。文件后端可以是内存、本地磁盘、数据库或远程沙箱，而 Agent 使用的文件接口可以保持一致。

## 6. LangSmith Trace 为什么重要

最终答案只能说明任务给出了结果，Trace 才能解释结果是怎样产生的。一条完整 Trace 中可能包含：

```text
research 根流程
├── research-agent 子 Agent
├── ChatOpenAI 模型调用
├── tavily_search 工具调用
└── 文件工具或 Middleware
```

排查慢调用时，不能直接把耗时最长的根流程当作瓶颈，因为根流程包含全部子步骤。应分别检查叶子模型 Run 和实际工具 Run 的耗时、状态、输入与输出。

我还遇到过一种情况：Agent 已经在终端返回答案，但 LangSmith Trace 上传失败。这说明 Agent 主流程和可观测性链路是两套相关但不同的能力；前者成功，不代表后者也配置正确。

## 7. Windows 环境配置踩坑记录

### PowerShell 粘贴 API Key 后长度只有 1

旧版 Windows PowerShell 中，直接使用某些快捷键可能把控制字符传给脚本。后来我改为按脚本提示粘贴完整 Key，并检查读取长度，确认不是把界面上的星号当成真实 Key。

### 把 Markdown 链接当成 API 地址

错误形式类似：

```text
[https://api.example.com](https://api.example.com)
```

环境变量中必须保存纯网址：

```text
https://api.example.com
```

Markdown 的方括号和圆括号进入 URL 后，HTTP 客户端会认为地址格式错误。

### 用户环境变量已经保存，当前终端却看不到

Windows 用户环境变量会提供给之后新开的进程，已经打开的 PowerShell 通常仍保留旧环境快照。因此保存变量后需要重新打开 PowerShell，再激活虚拟环境并运行检查程序。

### `PRESENT` 不代表接口一定可用

`env_check.py` 显示 `PRESENT` 只证明变量存在。真实可用性还需要通过模型请求、Tavily 搜索和 LangSmith Trace 上传分别验证。

## 8. 我的阶段总结

通过 Task1，我建立了一个比“安装成功”更完整的判断标准：环境变量存在只是静态准备，真正完成还需要依赖测试、API 连通、Agent 运行和 Trace 观察。我也理解了生产级 Agent 的重点不是单次回答，而是怎样让模型、工具、状态、文件、子 Agent 和可观测性稳定协作。接下来学习第二章时，我会重点观察 `create_deep_agent()` 如何把这些部分组装起来，而不是只关注最终输出。

## 9. 资料来源

- [Datawhale《Deep Agents 实战》GitHub 仓库](https://github.com/datawhalechina/deepagents-in-action)
- [课程在线文档：第1章 Agent Harness](https://datawhalechina.github.io/deepagents-in-action/chapters/ch01-agent-harness/)
- [课程配套视频](https://space.bilibili.com/28357052/lists/7757577?type=season)
- [AgentSeek 官方仓库](https://github.com/ob-labs/agentseek)
- [LangSmith Observability Quickstart](https://docs.langchain.com/langsmith/observability-quickstart)
- [Tavily 官方网站](https://www.tavily.com/)

本文为学习过程中的原创理解、实验记录和踩坑整理；课程概念与引用资料来源已在上方列出。

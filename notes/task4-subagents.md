# Task4 学习笔记：子 Agent 与上下文隔离——让 Agent 学会委派

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 5 章

## 一、课程与实验链接

- 课程正文：[子 Agent 与上下文隔离——让 Agent 学会委派](https://datawhalechina.github.io/deepagents-in-action/chapters/ch05-subagents/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV19A5d6UEqW/)
- 实验模板：[AgentSeek 模板：`deepagents/research`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/research)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task4-subagents.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task4-subagents.md)

## 二、本章内容归纳

学习 Context Quarantine、字典式子 Agent、general-purpose 与 CompiledSubAgent、多 Agent 协作和结构化输出。

**本章学习重点：**子 Agent 的职责、上下文隔离、工具继承与替换、角色描述、结构化返回。

## 三、关键知识点拆解

### 子 Agent 解决的是上下文与职责问题

主 Agent 负责理解总目标、决定是否委派并整合结果；子 Agent 在自己的上下文里执行一个边界清楚的子任务。Context Quarantine 的重点是只把完成主任务需要的摘要、证据和未解决问题带回主线，避免把整段检索过程和噪声都塞回主 Agent。

### 声明要把“做什么”和“能做什么”写清楚

字典式子 Agent 的 `name` 与 `description` 帮主 Agent 判断路由，`system_prompt` 约束工作方法，`tools` 限定可用动作，`model` 可按任务选择。工具列表显式提供时要检查继承和替换语义；不能假设子 Agent 自动拥有主 Agent 的所有工具。若已有 LangGraph 工作流需要作为委派对象，可以用 `CompiledSubAgent` 封装。

### 选择合适的协作模式

相互独立的研究项可并行，前后依赖的任务应串行；多角度审阅可让多个专家分别给证据，再由主 Agent 汇总。需要机器消费的结果应定义结构化 Schema，并让子 Agent 返回精简、可核对的字段。

```text
明确子任务与验收格式 → 路由到职责匹配的子 Agent → 隔离执行
→ 返回摘要/证据/缺口 → 主 Agent 交叉检查并整合
```

**我的工程判断：**子 Agent 数量增加会带来更多模型调用、等待和失败分支。简单、短小、强依赖共享上下文的任务直接由主 Agent 完成，通常更清楚。

## 四、学习心得

本章让我理解了主 Agent 不应该把所有搜索和中间推理都亲自完成。通过 task 委派，子 Agent 在独立上下文中处理复杂子任务，主 Agent 只接收摘要、证据和未解决问题，这就是 Context Quarantine。定义子 Agent 时，name 和 description 决定路由，system_prompt 决定职责边界，tools 和 permissions 则决定它实际能做什么。子 Agent 的价值不只是增加一个模型，更重要的是隔离上下文、减少主线负担并形成清晰分工。

## 五、对本次课程内容的反馈

建议课程增加一个“没有子 Agent”和“使用两个专业子 Agent”的对照实验，展示主 Agent 上下文长度、工具轨迹和最终摘要的差异。还可以补充工具继承与显式替换的失败案例，让学习者更直观地理解子 Agent 配置不是简单的参数复制。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch05-subagents/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/research
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

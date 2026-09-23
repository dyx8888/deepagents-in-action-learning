# Task10 学习笔记：文件系统权限——用声明式规则控制 Agent 的读写边界

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 11 章

## 一、课程与实验链接

- 课程正文：[文件系统权限——用声明式规则控制 Agent 的读写边界](https://datawhalechina.github.io/deepagents-in-action/chapters/ch11-filesystem-permissions/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1jdgz6eEB9/)
- 实验模板：[AgentSeek 模板：`deepagents/content-builder`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/content-builder)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task10-filesystem-permissions.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task10-filesystem-permissions.md)

## 二、本章内容归纳

学习 FilesystemPermission 的 read/write 分组、allow/deny/interrupt、first-match-wins、白名单和策略包装器。

**本章学习重点：**虚拟路径、默认允许、规则顺序、delete 全有或全无、CompositeBackend 和 execute 旁路。

## 三、关键知识点拆解

### 先区分操作类型与路径

`FilesystemPermission` 把读操作（如 `ls`、`read_file`、`glob`、`grep`）和写操作（如 `write_file`、`edit_file`、`delete`）分组，再将规则应用到虚拟路径。模式可以是 `allow`、`deny` 或 `interrupt`。规则保护的是 Deep Agents 内置文件工具，不会自动拦截自定义工具、MCP 工具或沙箱 `execute`。

### 首条匹配生效，因此规则顺序就是策略

求值采用 first-match-wins。敏感路径的拒绝规则应排在宽泛放行之前；如果要做白名单，最后还需要一个兜底 deny，因为没有匹配规则时默认允许。只声明一条允许工作区的规则，不足以限制其它路径。

### 测试拒绝与放行两侧

除了验证允许路径可读写，还要验证未匹配路径、规则顺序交换、受保护路径的读/写/删除、子 Agent 继承或替换规则，以及 `interrupt` 的批准、修改与拒绝。目录删除需特别检查，因为它可能影响保护目录中的后代。

```text
操作 → 规范化虚拟路径 → 按顺序找第一条匹配规则
→ allow / deny / interrupt → 执行或返回结构化拒绝
```

**我的工程判断：**稳定的路径基线用声明式权限；依赖用户身份、内容或频率的动态策略放到 Policy Hook；Shell、MCP 和外部写入入口另设权限和审批。

## 四、学习心得

本章让我认识到权限判断必须发生在 Backend 执行前。read 覆盖 ls、read_file、glob、grep，write 覆盖 write_file、edit_file 和 delete；规则按照 first-match-wins 求值，没有匹配时默认允许。因此只写一条 allow 并不是真正白名单，必须用最后的全局 deny 兜底。权限只约束内置文件工具，自定义工具、MCP 和 execute 需要各自的安全控制。

## 五、对本次课程内容的反馈

建议课程把规则顺序错误、工作区外默认放行和删除受保护目录做成自动化测试。若能提供一个可视化规则匹配器，显示 operation、path、命中的第一条规则和最终结果，初学者会更容易掌握权限边界。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch11-filesystem-permissions/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/content-builder
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

# Task9 学习笔记：沙箱执行——让 Agent 安全地运行代码

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 10 章

## 一、课程与实验链接

- 课程正文：[沙箱执行——让 Agent 安全地运行代码](https://datawhalechina.github.io/deepagents-in-action/chapters/ch10-sandboxes/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1xFNh6GEns/)
- 实验模板：[AgentSeek 模板：`deepagents/sandbox`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/sandbox)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task9-sandboxes.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task9-sandboxes.md)

## 二、本章内容归纳

学习 Sandbox Backend、execute、文件双平面、输入播种、产物提取、生命周期和资源/网络边界。

**本章学习重点：**宿主机与沙箱区别、文件传输、凭证隔离、快照与清理、Deep Agents Code 和托管沙箱。

## 三、关键知识点拆解

### Backend 与执行环境承担不同职责

普通文件 Backend 提供虚拟文件系统读写；支持沙箱的 Backend 还提供 `execute`，让 Agent 在隔离环境运行代码或命令。宿主机目录和沙箱工作区是两个文件平面：输入通常先复制/挂载进去，产物再经过验证后取回，文件能被 Agent 读到不代表代码已在沙箱运行。

### 把安全边界做成多项配置

隔离强度取决于挂载范围、网络策略、凭证注入、CPU/内存/时间上限、进程能力和沙箱生命周期。应默认不给不必要的宿主凭证和网络访问，并在超时、异常、取消时回收执行资源。LocalShellBackend 与远程或容器化沙箱的信任边界不同。

### 验证产物而不是只看命令返回

命令退出码为 0 只说明进程报告成功；交付前还要检查目标文件存在、格式可读、内容符合要求，并明确哪个版本从沙箱取回。复用快照可减少准备时间，但要检查快照中的依赖、数据和残留信息。

```text
准备输入 → 建立隔离运行环境 → 执行并设限
→ 检查日志与退出状态 → 提取/校验产物 → 清理环境
```

**我的工程判断：**Interpreter、文件权限和沙箱并非相互替代：解释器管受限代码编排，路径权限管内置文件工具，沙箱限制代码/命令的运行环境。

## 四、学习心得

本章让我明白沙箱是执行环境，而不是简单的权限开关。普通 Backend 主要读写文件，沙箱 Backend 还提供 execute，让 Agent 能运行测试、分析数据和生成产物。真正的安全边界取决于挂载目录、网络、凭证、CPU、内存和生命周期配置。宿主机文件与沙箱文件是两个平面，运行前要播种输入，运行后还要验证并提取产物，不能把命令成功当成交付成功。

## 五、对本次课程内容的反馈

建议课程用同一段代码分别在 LocalShellBackend 和沙箱中运行，展示文件、环境变量和网络可见范围的差异。对产物提取、沙箱销毁、快照复用和失败清理增加验收清单，会帮助学习者建立完整的安全闭环。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch10-sandboxes/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/sandbox
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

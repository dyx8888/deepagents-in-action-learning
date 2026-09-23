# Task6 学习笔记：Skills——可复用的 Agent 能力包

> 学习状态：已完成
> 课程：Datawhale `deepagents-in-action`；学习群：二群
> 对应章节：第 7 章

## 一、课程与实验链接

- 课程正文：[Skills——可复用的 Agent 能力包](https://datawhalechina.github.io/deepagents-in-action/chapters/ch07-skills/)
- 视频参考：
- [视频参考 1](https://www.bilibili.com/video/BV1XsEi6qEA6/)
- [视频参考 2](https://www.bilibili.com/video/BV1gDjV6eEXA/)
- 实验模板：[AgentSeek 模板：`deepagents/content-builder`](https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/content-builder)
- 课程源码：[datawhalechina/deepagents-in-action](https://github.com/datawhalechina/deepagents-in-action)
- 本篇公开笔记：[task6-skills.md](https://github.com/dyx8888/deepagents-in-action-learning/blob/main/notes/task6-skills.md)

## 二、本章内容归纳

学习 Agent Skills 规范、SKILL.md、渐进式加载、多源优先级、脚本资源、子 Agent 继承和权限控制。

**本章学习重点：**Tool 与 Skill 的区别、description 触发条件、references/scripts/assets 和 Progressive Disclosure。

## 三、关键知识点拆解

### Skill 是可发现、可复用的一套工作方法

一个 Skill 通常由带 YAML frontmatter 的 `SKILL.md` 及可选的 `references/`、`scripts/`、`assets/` 组成。`name` 标识能力，`description` 描述何时调用；正文写清步骤、输入、输出和边界。描述过宽会导致误触发，描述过窄则会让 Agent 找不到它。

### 渐进式加载减少上下文负担

Agent 先发现可用 Skill 的名称和描述，判断相关后再读取完整说明，需要时才加载参考资料或运行脚本。这种 Progressive Disclosure 把“技能目录”“操作说明”“详细资料”分层。Skill 本身是知识与流程包；真正执行搜索、读文件或运行脚本的仍是工具、Backend 或 Interpreter。

### 多源与子 Agent 需要明确优先级

项目共享、个人和组织级 Skill 可以从不同位置加载；同名冲突应按框架规定的来源优先级处理。子 Agent 是否能看到某项 Skill 取决于加载配置与权限，不应因主 Agent 可用就推断所有子 Agent 都可用。脚本和引用资料也要遵守同一权限边界。

```text
匹配 description → 读取 SKILL.md → 按需取 references/assets
→ 调用获准工具 → 按 Skill 规定核对输出
```

**我的工程判断：**适合跨任务重复使用、步骤稳定且需要随时更新的知识；短小的一次性动作做成 Tool 更直接，用户偏好或会话状态则属于 Memory。

## 四、学习心得

本章让我认识到 Tool 只是一个原子动作，而 Skill 是把领域知识、执行步骤、脚本、参考资料和模板组合起来的可复用能力包。SKILL.md 的 name 和 description 决定 Agent 能否正确发现它，正文应该写成可执行流程，详细资料则按需放在 references 中。渐进式加载可以避免把所有知识一次性塞进上下文；共享 Skill、个人 Skill 和子 Agent Skill 还需要明确优先级与权限边界。

## 五、对本次课程内容的反馈

建议课程提供一个从零创建 Skill 的小练习，例如“官方文档检索 Skill”，同时展示 description 写得模糊和具体时的触发差异。若能增加同名 Skill 覆盖、只读 Skill 和脚本沙箱的可视化案例，学习者会更容易理解复用与安全之间的关系。

## 六、资料来源

- Datawhale《Deep Agents 实战》课程页面：https://datawhalechina.github.io/deepagents-in-action/chapters/ch07-skills/
- 课程实验模板：https://github.com/agentseek-ai/agentseek-templates/tree/main/templates/deepagents/content-builder
- Deep Agents 官方文档：https://docs.langchain.com/oss/python/deepagents/overview

本文记录本章学习理解与课程反馈；课程内容和引用资料来源均已标注。

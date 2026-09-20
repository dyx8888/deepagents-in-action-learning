"""Task3: verify that TodoListMiddleware exposes and updates write_todos."""

from __future__ import annotations

import importlib.metadata
import json
import os

from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_openai import ChatOpenAI


def required_env(name: str) -> str:
    """Return a required environment variable without printing its value."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


model = ChatOpenAI(
    model=required_env("MODEL_NAME"),
    api_key=required_env("MODEL_API_KEY"),
    base_url=required_env("MODEL_BASE_URL").rstrip("/"),
    temperature=0,
    timeout=60,
    max_retries=0,
)

agent = create_deep_agent(
    model=model,
    middleware=[TodoListMiddleware()],
    system_prompt=(
        "这是任务规划教学实验。必须调用 write_todos 恰好两次：第一次创建恰好三个 pending 待办；"
        "第二次把同样三项一次性全部更新为 completed。不要在两次之间逐项更新，"
        "也不要调用其他工具。"
        "最后用一句话说明计划状态。"
    ),
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "请演示规划一个 Python 小项目发布任务，三项分别是检查代码、"
                    "运行测试、整理发布说明；这里只演示计划状态，不执行真实文件或网络操作。"
                ),
            }
        ]
    }
)

tool_calls: list[str] = []
for message in result["messages"]:
    for call in getattr(message, "tool_calls", []) or []:
        tool_calls.append(call.get("name", "<unknown>"))

todos = result.get("todos", [])
summary = {
    "deepagents_version": importlib.metadata.version("deepagents"),
    "langchain_version": importlib.metadata.version("langchain"),
    "model_config": "PRESENT (values hidden)",
    "tool_calls": tool_calls,
    "todo_count": len(todos),
    "todos": todos,
    "final_answer": result["messages"][-1].content,
}
print(json.dumps(summary, ensure_ascii=False, indent=2))

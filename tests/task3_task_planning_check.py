"""Deterministic Task3 check for TodoListMiddleware and write_todos."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable


PENDING = [
    {"content": "检查代码", "status": "pending"},
    {"content": "运行测试", "status": "pending"},
    {"content": "整理发布说明", "status": "pending"},
]
COMPLETED = [{**todo, "status": "completed"} for todo in PENDING]


class ToolCallingFakeModel(FakeMessagesListChatModel):
    """A deterministic chat model that accepts the tools bound by the agent."""

    def bind_tools(
        self,
        tools: Sequence[dict[str, Any] | type | Any],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ) -> Runnable:
        del tools, tool_choice, kwargs
        return self


model = ToolCallingFakeModel(
    responses=[
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "write_todos",
                    "args": {"todos": PENDING},
                    "id": "task3-create-plan",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "write_todos",
                    "args": {"todos": COMPLETED},
                    "id": "task3-complete-plan",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(content="三项计划均已完成。"),
    ]
)

agent = create_deep_agent(
    model=model,
    middleware=[TodoListMiddleware()],
)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "演示三步任务规划"}]},
    config={"recursion_limit": 20},
)

assert result["todos"] == COMPLETED
assert result["messages"][-1].content == "三项计划均已完成。"

print("TASK3_TEST=PASS")
print("WRITE_TODOS_CALLS=2")
print("TODO_COUNT=3")
print("TODO_STATUSES=completed,completed,completed")
print("FINAL_ANSWER=三项计划均已完成。")

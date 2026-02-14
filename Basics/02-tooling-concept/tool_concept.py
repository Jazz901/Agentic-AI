from __future__ import annotations

from collections import Counter
import operator

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Summarize transformers"},
    {"role": "assistant", "content": "Transformers use attention..."},
    {"role": "user", "content": "Give an example"},
]


def get_text_by_role(messages: list[dict], role: str) -> list[str]:
    return [m["content"] for m in messages if m["role" == role]]


def get_last_by_role(messages: list[dict], role: str) -> list[str]:
    return next((m["content"] for m in reversed(messages) if m["role"] == role), None)

def count_roles (messages: list[dict]) -> Counter:
     return Counter(m["role"] for m in messages)

def as_readable_text(messages: list[dict]) -> str:
    return "\n".join(f'{m["role"].upper()}: {m["content"]}' for m in messages)


def search(query: str) -> str:
    return f"[SEARCH] Results for: {query}"


SAFE_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

def calculate(a: float, op:str, b: float) -> str: 
    if op not in SAFE_OPERATORS: 
        return f"[ERROR] Unsupported operator: {op}"
    try:
        result = SAFE_OPERATORS[op](a, b)
        return  f"[CALC] {a} {op} {b} = {result}"
    except Exception as e:
        return f"[ERROR] Calculation failed: {e}"


TOOLS = {
    "search": search,
    "calculate": calculate,
}


def run_tool(tool_call: dict) -> str: 
    name = tool_call.get("name")
    args = tool_call.get("arguments", {})

    if name not in TOOLS: 
        return f"[ERROR] Unknown tool: {name}"
    
    tool_fn = TOOLS[name]

    try:
        return tool_fn(**args)

    except TypeError as e: 
      return f"[ERROR] Invalid arguments for '{name}': {e}"
    except Exception as e:
        return f"[ERROR] Tool '{name}' failed: {e}"

def agent_step(tool_calls: list[dict]) -> list[str]:
    results = []
    for call in tool_calls:
        print(f"\nCALLING TOOL: {call.get('name')}")
        results.append(run_tool(call))
    return results

    
if __name__ == "__main__":
    tool_calls = [
            {"name": "search", "arguments": {"query": "Agentic AI"}},
            {"name": "calculate", "arguments": {"a": 10, "op": "/", "b": 2}},
            {"name": "calculate", "arguments": {"a": 1, "op": "^", "b": 3}}, 
            {"name": "weather", "arguments": {"city": "Berlin"}},                 
    ]

    outputs = agent_step(tool_calls)

    print("\nRESULTS:")
    for out in outputs:
        print(out)



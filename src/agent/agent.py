
import json

from src.agent.tool_executor import execute_tool
from src.tools.tool_schemas import SUPPORTED_GENRES_TOOL


MAX_ITERATIONS = 5

AVAILABLE_SCHEMAS = [
    SUPPORTED_GENRES_TOOL
]


def run_agent(client, messages):

    for iteration in range(MAX_ITERATIONS):

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=AVAILABLE_SCHEMAS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If no tools are requested, return the final response
        if not message.tool_calls:

            messages.append({
                "role": "assistant",
                "content": message.content
            })

            return message.content, messages

        # Preserve the assistant's tool-call message
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # Execute requested tools
        for tool_call in message.tool_calls:

            try:
                tool_result = execute_tool(tool_call)

            except Exception as error:
                tool_result = json.dumps({
                    "error": str(error)
                })

            # Send tool result back to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

    raise RuntimeError("Agent exceeded maximum iterations.")

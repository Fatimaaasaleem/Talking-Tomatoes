import json

from src.tools.movie_discovery import list_supported_genres


# Registry of available Python tools
AVAILABLE_TOOLS = {
    "list_supported_genres": list_supported_genres,
}


def execute_tool(tool_call):
    function_name = tool_call.function.name

    # Find the requested function
    function = AVAILABLE_TOOLS.get(function_name)

    if function is None:
        raise ValueError(f"Unknown tool: {function_name}")

    # Parse JSON arguments
    try:
        arguments = json.loads(tool_call.function.arguments)

        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a JSON object.")

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON arguments received from the LLM.")

    # Execute the Python function
    result = function(**arguments)

    # Return result as JSON
    return json.dumps(result)
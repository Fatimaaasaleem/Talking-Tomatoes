import json

from src.tools.movie_discovery import (
    list_supported_genres,
    search_movie,
    search_tv,
    discover_movies,
    discover_tv,
    get_movie_details,
    get_tv_details,
    get_similar_movies,
    get_similar_tv
)


# Registry of available Python tools
AVAILABLE_TOOLS = {
    "list_supported_genres": list_supported_genres,
    "search_movie": search_movie,
    "search_tv": search_tv,
    "discover_movies": discover_movies,
    "discover_tv": discover_tv,
    "get_movie_details": get_movie_details,
    "get_tv_details": get_tv_details,
    "get_similar_movies": get_similar_movies,
    "get_similar_tv": get_similar_tv,
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
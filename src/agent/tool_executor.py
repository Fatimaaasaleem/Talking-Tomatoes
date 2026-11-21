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

from src.tools.database_tools import (
    get_user_preferences,
    get_user_library,
    get_user_viewing_history,
    update_user_preferences,
    add_user_genre_preference,
    remove_user_genre_preference,
    add_user_library_entry,
    update_user_library_status,
    update_user_favourite,
    remove_user_library_entry,
    update_user_viewing_progress,
    record_user_viewing_history
)

from src.agent.confirmation import (
    create_pending_action,
    get_pending_action,
    clear_pending_action
)


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

    "get_user_preferences": get_user_preferences,
    "get_user_library": get_user_library,
    "get_user_viewing_history": get_user_viewing_history,

    "update_user_preferences": update_user_preferences,
    "add_user_genre_preference": add_user_genre_preference,
    "remove_user_genre_preference": remove_user_genre_preference,
    "add_user_library_entry": add_user_library_entry,
    "update_user_library_status": update_user_library_status,
    "update_user_favourite": update_user_favourite,
    "remove_user_library_entry": remove_user_library_entry,
    "update_user_viewing_progress": update_user_viewing_progress,
    "record_user_viewing_history": record_user_viewing_history,
}


DATABASE_TOOLS = {
    "get_user_preferences",
    "get_user_library",
    "get_user_viewing_history",
    "update_user_preferences",
    "add_user_genre_preference",
    "remove_user_genre_preference",
    "add_user_library_entry",
    "update_user_library_status",
    "update_user_favourite",
    "remove_user_library_entry",
    "update_user_viewing_progress",
    "record_user_viewing_history",
}


WRITE_TOOLS = {
    "update_user_preferences",
    "add_user_genre_preference",
    "remove_user_genre_preference",
    "add_user_library_entry",
    "update_user_library_status",
    "update_user_favourite",
    "remove_user_library_entry",
    "update_user_viewing_progress",
    "record_user_viewing_history",
}


def execute_tool(tool_call, user_id=None):
    """Execute read tools or create a pending database action."""

    function_name = tool_call.function.name
    function = AVAILABLE_TOOLS.get(function_name)

    if function is None:
        raise ValueError(f"Unknown tool: {function_name}")

    try:
        arguments = json.loads(tool_call.function.arguments)

        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a JSON object.")

    except json.JSONDecodeError as error:
        raise ValueError("Invalid JSON arguments received from the LLM.") from error

    # The application, not the LLM, determines the user.
    if function_name in DATABASE_TOOLS:
        if user_id is None:
            raise ValueError("User ID is required for database tools.")

    # Intercept every write request.
    if function_name in WRITE_TOOLS:

        action_id = create_pending_action(
            user_id=user_id,
            tool_name=function_name,
            arguments=arguments
        )

        return json.dumps({
            "pending_confirmation": True,
            "action_id": action_id,
            "tool_name": function_name,
            "arguments": arguments,
            "message": "This action requires explicit user confirmation. Do not execute it again. Explain the proposed action and ask the user to confirm."
        })

    # Execute read operations immediately.
    if function_name in DATABASE_TOOLS:
        arguments["user_id"] = user_id

    result = function(**arguments)

    return json.dumps(result)


def confirm_pending_action(user_id, action_id):
    """Execute a pending action after application-level confirmation."""

    action = get_pending_action(user_id)

    if action is None:
        return {
            "success": False,
            "message": "No valid pending action exists."
        }

    if action["action_id"] != action_id:
        return {
            "success": False,
            "message": "Confirmation does not match the pending action."
        }

    function = AVAILABLE_TOOLS.get(action["tool_name"])

    if function is None or action["tool_name"] not in WRITE_TOOLS:
        return {
            "success": False,
            "message": "Invalid pending action."
        }

    # Consume the pending action before execution to prevent replay.
    clear_pending_action(user_id)

    arguments = action["arguments"].copy()
    arguments["user_id"] = user_id

    try:
        result = function(**arguments)

        return {
            "success": True,
            "result": result
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


def cancel_pending_action(user_id):
    """Cancel a user's pending action."""

    action = get_pending_action(user_id)

    if action is None:
        return False

    clear_pending_action(user_id)
    return True
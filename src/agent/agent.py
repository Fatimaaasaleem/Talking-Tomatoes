import json

from src.agent.tool_executor import (
    execute_tool,
    WRITE_TOOLS,
    confirm_pending_action,
    cancel_pending_action,
)

from src.agent.confirmation import get_pending_action

from src.tools.tool_schemas import (
    SUPPORTED_GENRES_TOOL,
    SEARCH_MOVIE_TOOL,
    SEARCH_TV_TOOL,
    DISCOVER_MOVIES_TOOL,
    DISCOVER_TV_TOOL,
    GET_MOVIE_DETAILS_TOOL,
    GET_TV_DETAILS_TOOL,
    GET_SIMILAR_MOVIES_TOOL,
    GET_SIMILAR_TV_TOOL,

    # Database read schemas
    GET_USER_PREFERENCES_TOOL,
    GET_USER_LIBRARY_TOOL,
    GET_USER_VIEWING_HISTORY_TOOL,
    GET_USER_RECOMMENDATION_FEEDBACK_TOOL,
    GET_PERSONALIZED_RECOMMENDATIONS_TOOL,

    # Database write schemas
    UPDATE_USER_PREFERENCES_TOOL,
    ADD_USER_GENRE_PREFERENCE_TOOL,
    REMOVE_USER_GENRE_PREFERENCE_TOOL,
    ADD_USER_LIBRARY_ENTRY_TOOL,
    UPDATE_USER_LIBRARY_STATUS_TOOL,
    UPDATE_USER_FAVOURITE_TOOL,
    REMOVE_USER_LIBRARY_ENTRY_TOOL,
    UPDATE_USER_VIEWING_PROGRESS_TOOL,
    RECORD_USER_VIEWING_HISTORY_TOOL,
    RECORD_RECOMMENDATION_FEEDBACK_TOOL,
    REMOVE_USER_RECOMMENDATION_FEEDBACK_TOOL,
)


MAX_ITERATIONS = 5


# ==========================================
# AVAILABLE TOOL SCHEMAS
# ==========================================

AVAILABLE_SCHEMAS = [
    # TMDB tools
    SUPPORTED_GENRES_TOOL,
    SEARCH_MOVIE_TOOL,
    SEARCH_TV_TOOL,
    DISCOVER_MOVIES_TOOL,
    DISCOVER_TV_TOOL,
    GET_MOVIE_DETAILS_TOOL,
    GET_TV_DETAILS_TOOL,
    GET_SIMILAR_MOVIES_TOOL,
    GET_SIMILAR_TV_TOOL,

    # Database read schemas
    GET_USER_PREFERENCES_TOOL,
    GET_USER_LIBRARY_TOOL,
    GET_USER_VIEWING_HISTORY_TOOL,
    GET_USER_RECOMMENDATION_FEEDBACK_TOOL,
    GET_PERSONALIZED_RECOMMENDATIONS_TOOL,

    # Database write schemas
    UPDATE_USER_PREFERENCES_TOOL,
    ADD_USER_GENRE_PREFERENCE_TOOL,
    REMOVE_USER_GENRE_PREFERENCE_TOOL,
    ADD_USER_LIBRARY_ENTRY_TOOL,
    UPDATE_USER_LIBRARY_STATUS_TOOL,
    UPDATE_USER_FAVOURITE_TOOL,
    REMOVE_USER_LIBRARY_ENTRY_TOOL,
    UPDATE_USER_VIEWING_PROGRESS_TOOL,
    RECORD_USER_VIEWING_HISTORY_TOOL,
    RECORD_RECOMMENDATION_FEEDBACK_TOOL,
    REMOVE_USER_RECOMMENDATION_FEEDBACK_TOOL,
]


# ==========================================
# CONFIRMATION HANDLING
# ==========================================

def handle_pending_confirmation(messages, user_id):
    """Handle yes/no replies before sending anything to the LLM."""

    if user_id is None or not messages:
        return None

    pending_action = get_pending_action(user_id)

    if pending_action is None:
        return None

    last_message = messages[-1]

    if last_message.get("role") != "user":
        return None

    user_reply = (last_message.get("content") or "").strip().lower()

    if user_reply not in ("yes", "y", "confirm", "no", "n", "cancel"):
        return None

    if user_reply in ("no", "n", "cancel"):
        cancel_pending_action(user_id)

        response_text = "No problem. I've cancelled the requested change."

    else:
        result = confirm_pending_action(
            user_id=user_id,
            action_id=pending_action["action_id"]
        )

        if result["success"]:
            response_text = (
                "Done! Your requested change has been saved successfully."
            )
        else:
            response_text = (
                "I couldn't complete that change: "
                f"{result.get('message', 'Unknown error')}"
            )

    messages.append({
        "role": "assistant",
        "content": response_text
    })

    return response_text, messages


# ==========================================
# AGENT EXECUTION
# ==========================================

def run_agent(client, messages, user_id=None):
    """Run the Talking Tomatoes tool-calling agent."""

    # Handle confirmations before calling the LLM.
    confirmation_response = handle_pending_confirmation(
        messages,
        user_id
    )

    if confirmation_response is not None:
        return confirmation_response

    for iteration in range(MAX_ITERATIONS):

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=AVAILABLE_SCHEMAS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": message.content
            })

            return message.content, messages

        tool_calls = message.tool_calls

        write_calls = [
            tool_call
            for tool_call in tool_calls
            if tool_call.function.name in WRITE_TOOLS
        ]

        # Reject batches containing both read and write operations.
        if write_calls and len(tool_calls) > 1:

            messages.append(
                message.model_dump(exclude_none=True)
            )

            for tool_call in tool_calls:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps({
                        "error": (
                            "A database write must be the only "
                            "tool call in a turn. Please request "
                            "one change at a time."
                        )
                    })
                })

            response_text = (
                "I can handle one database change at a time. "
                "Please tell me which change you'd like first."
            )

            messages.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text, messages

        messages.append(
            message.model_dump(exclude_none=True)
        )

        pending_confirmation = False

        for tool_call in tool_calls:

            try:
                tool_result = execute_tool(
                    tool_call,
                    user_id=user_id
                )

            except Exception as error:
                tool_result = json.dumps({
                    "error": str(error)
                })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

            try:
                result_data = json.loads(tool_result)

            except (json.JSONDecodeError, TypeError):
                result_data = None

            if (
                isinstance(result_data, dict)
                and result_data.get("pending_confirmation")
            ):
                pending_confirmation = True

        if pending_confirmation:

            response_text = (
                "I'm ready to perform the requested change. "
                "Please review the proposed action and reply "
                "'yes' to confirm or 'no' to cancel."
            )

            messages.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text, messages

    raise RuntimeError(
        "Agent exceeded maximum iterations."
    )
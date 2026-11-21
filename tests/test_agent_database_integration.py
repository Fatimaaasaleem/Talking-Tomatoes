import json

import pytest

from types import SimpleNamespace
from unittest.mock import Mock

from src.database import connection
from src.database.schema import create_tables
from src.database.operations import create_user

from src.agent.agent import run_agent
from src.agent.tool_executor import (
    confirm_pending_action,
    execute_tool
)


@pytest.fixture
def test_users(tmp_path, monkeypatch):
    """Create an isolated temporary database with two users."""

    database_path = tmp_path / "test_database.db"

    monkeypatch.setattr(
        connection,
        "DATABASE_PATH",
        database_path
    )

    monkeypatch.setattr(
        connection,
        "DATABASE_DIR",
        tmp_path
    )

    create_tables()

    user_one = create_user("user_one")
    user_two = create_user("user_two")

    return user_one, user_two


def create_tool_call(name, arguments, call_id="call_123"):
    return SimpleNamespace(
        id=call_id,
        function=SimpleNamespace(
            name=name,
            arguments=json.dumps(arguments)
        )
    )


def create_assistant_tool_message(tool_call):
    return SimpleNamespace(
        tool_calls=[tool_call],
        content=None,
        model_dump=lambda exclude_none=True: {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
            ]
        }
    )


def create_final_message(content):
    return SimpleNamespace(
        tool_calls=None,
        content=content
    )


def test_agent_database_write_and_read_workflow(test_users):
    """Test adding a title through confirmation and retrieving it."""

    user_one, user_two = test_users

    # Step 1: Simulate the LLM requesting a database write.

    write_call = create_tool_call(
        "add_user_library_entry",
        {
            "tmdb_id": 550,
            "media_type": "movie",
            "status": "watchlist"
        }
    )

    client = Mock()

    client.chat.completions.create.return_value.choices = [
        Mock(
            message=create_assistant_tool_message(write_call)
        )
    ]

    messages = [
        {
            "role": "user",
            "content": "Add Fight Club to my watchlist."
        }
    ]

    response, updated_messages = run_agent(
        client,
        messages,
        user_id=user_one
    )

    assert "confirm" in response.lower()

    # Step 2: Verify that the action is pending.

    tool_result = next(
        message
        for message in updated_messages
        if message["role"] == "tool"
    )

    pending_data = json.loads(tool_result["content"])

    assert pending_data["pending_confirmation"] is True

    # Step 3: Confirm the pending database operation.

    confirmation_result = confirm_pending_action(
        user_one,
        pending_data["action_id"]
    )

    assert confirmation_result["success"] is True

    # Step 4: Retrieve the library through the agent.

    read_call = create_tool_call(
        "get_user_library",
        {}
    )

    read_client = Mock()

    read_client.chat.completions.create.side_effect = [
        Mock(
            choices=[
                Mock(
                    message=create_assistant_tool_message(read_call)
                )
            ]
        ),
        Mock(
            choices=[
                Mock(
                    message=create_final_message(
                        "Fight Club is in your watchlist."
                    )
                )
            ]
        )
    ]

    read_messages = [
        {
            "role": "user",
            "content": "Show me my watchlist."
        }
    ]

    final_response, updated_messages = run_agent(
        read_client,
        read_messages,
        user_id=user_one
    )

    assert "Fight Club" in final_response

    retrieved_result = next(
        message
        for message in updated_messages
        if message["role"] == "tool"
    )

    library = json.loads(retrieved_result["content"])

    assert len(library) == 1
    assert library[0]["tmdb_id"] == 550
    assert library[0]["media_type"] == "movie"
    assert library[0]["status"] == "watchlist"

    # Step 5: Verify that another user cannot access this entry.

    other_user_library = json.loads(
        execute_tool(
            create_tool_call(
                "get_user_library",
                {}
            ),
            user_id=user_two
        )
    )

    assert other_user_library == []


def test_agent_does_not_execute_write_without_confirmation(test_users):
    """Verify that a write request does not immediately modify the database."""

    user_one, _ = test_users

    write_call = create_tool_call(
        "add_user_library_entry",
        {
            "tmdb_id": 550,
            "media_type": "movie",
            "status": "watchlist"
        }
    )

    client = Mock()

    client.chat.completions.create.return_value.choices = [
        Mock(
            message=create_assistant_tool_message(write_call)
        )
    ]

    messages = [
        {
            "role": "user",
            "content": "Add Fight Club to my watchlist."
        }
    ]

    response, updated_messages = run_agent(
        client,
        messages,
        user_id=user_one
    )

    assert "confirm" in response.lower()

    # The database must remain unchanged until confirmation.

    from src.database.operations import get_library

    library = get_library(user_one)

    assert library == []
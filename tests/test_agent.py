import json
import pytest

from unittest.mock import Mock
from types import SimpleNamespace

from src.agent.agent import run_agent


def test_agent_returns_normal_response():
    client = Mock()

    message = Mock()
    message.tool_calls = None
    message.content = "Hello! I am Talking Tomatoes."

    client.chat.completions.create.return_value.choices = [
        Mock(message=message)
    ]

    messages = [{"role": "user", "content": "Hello"}]

    response, updated_messages = run_agent(client, messages)

    assert response == "Hello! I am Talking Tomatoes."
    assert updated_messages[-1]["role"] == "assistant"


def test_agent_stops_after_max_iterations():
    client = Mock()

    tool_call = SimpleNamespace(
        id="call_123",
        function=SimpleNamespace(
            name="unknown_tool",
            arguments="{}"
        )
    )

    message = Mock()
    message.tool_calls = [tool_call]
    message.model_dump.return_value = {
        "role": "assistant",
        "tool_calls": [{"id": "call_123"}]
    }

    client.chat.completions.create.return_value.choices = [
        Mock(message=message)
    ]

    messages = [{"role": "user", "content": "Find me a movie"}]

    with pytest.raises(RuntimeError, match="maximum iterations"):
        run_agent(client, messages)

    assert client.chat.completions.create.call_count == 5


def test_agent_completes_tool_call_cycle():
    client = Mock()

    tool_call = SimpleNamespace(
        id="call_123",
        function=SimpleNamespace(
            name="list_supported_genres",
            arguments="{}"
        )
    )

    tool_message = Mock()
    tool_message.tool_calls = [tool_call]
    tool_message.model_dump.return_value = {
        "role": "assistant",
        "tool_calls": [{"id": "call_123"}]
    }

    final_message = Mock()
    final_message.tool_calls = None
    final_message.content = "Our supported genres are Action, Comedy and Drama."

    client.chat.completions.create.side_effect = [
        Mock(choices=[Mock(message=tool_message)]),
        Mock(choices=[Mock(message=final_message)])
    ]

    messages = [{"role": "user", "content": "What genres do you support?"}]

    response, updated_messages = run_agent(client, messages)

    assert response == final_message.content

    tool_results = [
        message for message in updated_messages
        if message["role"] == "tool"
    ]

    assert len(tool_results) == 1
    assert tool_results[0]["tool_call_id"] == "call_123"

    assert json.loads(tool_results[0]["content"]) == [
        "Action",
        "Comedy",
        "Drama",
        "Horror",
        "Romance",
        "Sci-Fi",
        "Thriller"
    ]

    assert client.chat.completions.create.call_count == 2


def test_agent_handles_tool_execution_error():
    client = Mock()

    tool_call = SimpleNamespace(
        id="call_error",
        function=SimpleNamespace(
            name="unknown_tool",
            arguments="{}"
        )
    )

    tool_message = Mock()
    tool_message.tool_calls = [tool_call]
    tool_message.model_dump.return_value = {
        "role": "assistant",
        "tool_calls": [{"id": "call_error"}]
    }

    final_message = Mock()
    final_message.tool_calls = None
    final_message.content = "Sorry, I couldn't retrieve that information."

    client.chat.completions.create.side_effect = [
        Mock(choices=[Mock(message=tool_message)]),
        Mock(choices=[Mock(message=final_message)])
    ]

    messages = [{"role": "user", "content": "Find me a movie"}]

    response, updated_messages = run_agent(client, messages)

    assert response == final_message.content

    tool_results = [
        message for message in updated_messages
        if message["role"] == "tool"
    ]

    assert len(tool_results) == 1
    assert tool_results[0]["tool_call_id"] == "call_error"

    error_result = json.loads(tool_results[0]["content"])

    assert "error" in error_result
    assert "Unknown tool" in error_result["error"]

    assert client.chat.completions.create.call_count == 2
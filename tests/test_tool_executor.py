import json
import pytest
from types import SimpleNamespace

from src.agent.tool_executor import (
    execute_tool,
    confirm_pending_action,
    cancel_pending_action,
    AVAILABLE_TOOLS
)


def create_tool_call(name, arguments):
    return SimpleNamespace(
        function=SimpleNamespace(
            name=name,
            arguments=arguments
        )
    )


def test_execute_tool_successfully():
    tool_call = create_tool_call(
        "list_supported_genres",
        "{}"
    )

    result = execute_tool(tool_call)

    assert json.loads(result) == [
        "Action",
        "Comedy",
        "Drama",
        "Horror",
        "Romance",
        "Sci-Fi",
        "Thriller"
    ]


def test_execute_tool_unknown_function():
    tool_call = create_tool_call(
        "unknown_tool",
        "{}"
    )

    with pytest.raises(ValueError, match="Unknown tool"):
        execute_tool(tool_call)


def test_execute_tool_invalid_json():
    tool_call = create_tool_call(
        "list_supported_genres",
        "{invalid json}"
    )

    with pytest.raises(ValueError, match="Invalid JSON"):
        execute_tool(tool_call)
        
        
def test_write_tool_requires_confirmation(monkeypatch):
    
    executed = []

    monkeypatch.setitem(
        __import__("src.agent.tool_executor", fromlist=["AVAILABLE_TOOLS"]).AVAILABLE_TOOLS,
        "update_user_favourite",
        lambda **kwargs: executed.append(kwargs)
    )

    tool_call = create_tool_call(
        "update_user_favourite",
        json.dumps({
            "tmdb_id": 123,
            "media_type": "movie",
            "is_favourite": True
        })
    )

    result = json.loads(
        execute_tool(tool_call, user_id=101)
    )

    assert result["pending_confirmation"] is True
    assert result["tool_name"] == "update_user_favourite"
    assert executed == []


def test_valid_confirmation_executes_action(monkeypatch):
    from src.agent import tool_executor

    executed = []

    monkeypatch.setitem(
        tool_executor.AVAILABLE_TOOLS,
        "update_user_favourite",
        lambda **kwargs: executed.append(kwargs) or True
    )

    tool_call = create_tool_call(
        "update_user_favourite",
        json.dumps({
            "tmdb_id": 123,
            "media_type": "movie",
            "is_favourite": True
        })
    )

    pending = json.loads(
        execute_tool(tool_call, user_id=102)
    )

    result = tool_executor.confirm_pending_action(
        102,
        pending["action_id"]
    )

    assert result["success"] is True
    assert len(executed) == 1
    assert executed[0]["user_id"] == 102


def test_incorrect_confirmation_id_is_rejected(monkeypatch):
    from src.agent import tool_executor

    tool_call = create_tool_call(
        "update_user_favourite",
        json.dumps({
            "tmdb_id": 123,
            "media_type": "movie",
            "is_favourite": True
        })
    )

    pending = json.loads(
        execute_tool(tool_call, user_id=103)
    )

    result = tool_executor.confirm_pending_action(
        103,
        "incorrect-id"
    )

    assert result["success"] is False
    assert "does not match" in result["message"]

    # The original pending action should remain available.
    assert tool_executor.confirm_pending_action(
        103,
        pending["action_id"]
    )["success"] is True


def test_cancel_pending_action(monkeypatch):
    from src.agent import tool_executor

    executed = []

    monkeypatch.setitem(
        tool_executor.AVAILABLE_TOOLS,
        "update_user_favourite",
        lambda **kwargs: executed.append(kwargs)
    )

    tool_call = create_tool_call(
        "update_user_favourite",
        json.dumps({
            "tmdb_id": 123,
            "media_type": "movie",
            "is_favourite": True
        })
    )

    pending = json.loads(
        execute_tool(tool_call, user_id=104)
    )

    cancelled = tool_executor.cancel_pending_action(104)

    assert cancelled is True

    result = tool_executor.confirm_pending_action(
        104,
        pending["action_id"]
    )

    assert result["success"] is False
    assert executed == []


def test_expired_confirmation_is_rejected(monkeypatch):
    from src.agent import tool_executor, confirmation

    current_time = [100]

    monkeypatch.setattr(
        confirmation.time,
        "time",
        lambda: current_time[0]
    )

    tool_call = create_tool_call(
        "update_user_favourite",
        json.dumps({
            "tmdb_id": 123,
            "media_type": "movie",
            "is_favourite": True
        })
    )

    pending = json.loads(
        execute_tool(tool_call, user_id=105)
    )

    current_time[0] = 221

    result = tool_executor.confirm_pending_action(
        105,
        pending["action_id"]
    )

    assert result["success"] is False
    assert "No valid pending action" in result["message"]


def test_confirmed_action_cannot_be_replayed(monkeypatch):
    from src.agent import tool_executor

    executed = []

    monkeypatch.setitem(
        tool_executor.AVAILABLE_TOOLS,
        "update_user_favourite",
        lambda **kwargs: executed.append(kwargs) or True
    )

    tool_call = create_tool_call(
        "update_user_favourite",
        json.dumps({
            "tmdb_id": 123,
            "media_type": "movie",
            "is_favourite": True
        })
    )

    pending = json.loads(
        execute_tool(tool_call, user_id=106)
    )

    first_result = tool_executor.confirm_pending_action(
        106,
        pending["action_id"]
    )

    second_result = tool_executor.confirm_pending_action(
        106,
        pending["action_id"]
    )

    assert first_result["success"] is True
    assert second_result["success"] is False
    assert len(executed) == 1        
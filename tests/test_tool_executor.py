import json
import pytest
from types import SimpleNamespace

from src.agent.tool_executor import execute_tool


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
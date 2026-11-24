import json

from frontend.companion.local_service import extract_media_results


def test_extract_movie_results():
    messages = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "search_movie"},
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call_1",
            "content": json.dumps([
                {
                    "id": 123,
                    "title": "Interstellar",
                    "poster_path": "/poster.jpg",
                    "rating": 8.7,
                }
            ]),
        },
    ]

    results = extract_media_results(messages)

    assert len(results) == 1
    assert results[0]["title"] == "Interstellar"
    assert results[0]["media_type"] == "movie"
    assert results[0]["poster_path"] == "/poster.jpg"


def test_extract_tv_results():
    messages = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_2",
                    "function": {"name": "search_tv"},
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call_2",
            "content": json.dumps([
                {
                    "id": 456,
                    "name": "Dark",
                    "poster_path": "/dark.jpg",
                }
            ]),
        },
    ]

    results = extract_media_results(messages)

    assert len(results) == 1
    assert results[0]["name"] == "Dark"
    assert results[0]["media_type"] == "tv"


def test_ignore_unrelated_tools():
    messages = [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_3",
                    "function": {"name": "get_user_preferences"},
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call_3",
            "content": json.dumps({"language": "English"}),
        },
    ]

    assert extract_media_results(messages) == []
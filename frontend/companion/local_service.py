"""Local adapter connecting the frontend to the existing backend."""

import copy
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from src.agent.agent import run_agent
from src.agent.prompts import SYSTEM_PROMPT
from src.database.operations import get_user

from .service import (
    CompanionError,
    CompanionReply,
    CompanionService,
)


MEDIA_TOOLS = {
    "search_movie": "movie",
    "discover_movies": "movie",
    "get_similar_movies": "movie",
    "search_tv": "tv",
    "discover_tv": "tv",
    "get_similar_tv": "tv",
}


def extract_media_results(messages: list[dict]) -> list[dict]:
    """Extract media results from the latest relevant tool-call batch."""

    for index in range(len(messages) - 1, -1, -1):
        message = messages[index]

        if message.get("role") != "assistant":
            continue

        tool_calls = message.get("tool_calls", [])
        relevant_calls = {}

        for call in tool_calls:
            function = call.get("function", {})
            function_name = function.get("name")

            if function_name in MEDIA_TOOLS:
                relevant_calls[call["id"]] = MEDIA_TOOLS[function_name]

            elif function_name == "get_personalized_recommendations":
                try:
                    arguments = json.loads(function.get("arguments", "{}"))
                except (json.JSONDecodeError, TypeError):
                    arguments = {}

                media_type = arguments.get("media_type", "movie")

                if media_type in ("movie", "tv"):
                    relevant_calls[call["id"]] = media_type

        if not relevant_calls:
            continue

        media_results = []

        for result_message in messages[index + 1:]:

            tool_call_id = result_message.get("tool_call_id")

            if (
                result_message.get("role") != "tool"
                or tool_call_id not in relevant_calls
            ):
                continue

            try:
                result_data = json.loads(
                    result_message.get("content", "")
                )
            except (json.JSONDecodeError, TypeError):
                continue

            if not isinstance(result_data, list):
                continue

            media_type = relevant_calls[tool_call_id]

            for item in result_data:

                if not isinstance(item, dict):
                    continue

                media_results.append({
                    **item,
                    "media_type": media_type,
                })

        return media_results

    return []


class LocalCompanionService(CompanionService):
    """Development adapter that calls the backend directly."""

    def __init__(self, user_id: int):
        self.user_id = user_id

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise CompanionError(
                "The application is not configured correctly. "
                "Please contact the administrator."
            )

        try:
            self.client = Groq(api_key=api_key)
            self.user = get_user(user_id)

        except Exception as error:
            raise CompanionError(
                "Could not connect to the companion service. "
                "Please try again later."
            ) from error

        if not self.user:
            raise CompanionError(
                "The development user was not found in the database."
            )

    def get_username(self) -> str:
        return self.user["username"]

    def new_conversation(self) -> list[dict]:
        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def send_message(self, messages: list[dict]) -> CompanionReply:
        updated_messages = copy.deepcopy(messages)
        request_start = len(updated_messages)

        try:
            reply, updated_messages = run_agent(
                client=self.client,
                messages=updated_messages,
                user_id=self.user_id,
            )

            new_messages = updated_messages[request_start:]

            return CompanionReply(
                text=reply,
                messages=updated_messages,
                media_results=extract_media_results(new_messages),
            )

        except APITimeoutError as error:
            raise CompanionError(
                "The request timed out. Please try again."
            ) from error

        except APIConnectionError as error:
            raise CompanionError(
                "Could not connect to the AI service. Please try again."
            ) from error

        except AuthenticationError as error:
            raise CompanionError(
                "The AI service authentication failed. "
                "Please contact the administrator."
            ) from error

        except RateLimitError as error:
            raise CompanionError(
                "The AI service is busy. Please wait a moment and try again."
            ) from error

        except APIStatusError as error:
            print(
                f"Groq API Error: {error}",
                flush=True,
            )
            raise CompanionError(
                "The AI service returned an error. Please try again later."
            ) from error

        except Exception as error:
            raise CompanionError(
                "Something went wrong while processing your request."
            ) from error
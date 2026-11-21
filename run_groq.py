import os

from dotenv import load_dotenv

from groq import (
    Groq,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
    APITimeoutError
)

from src.agent.agent import run_agent
from src.agent.tool_executor import (
    confirm_pending_action,
    cancel_pending_action
)
from src.agent.confirmation import get_pending_action
from src.database.operations import get_user


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )


client = Groq(
    api_key=api_key,
    timeout=30.0,
    max_retries=1
)


# Temporary development user.
USER_ID = 2

user = get_user(USER_ID)

if user is None:
    raise ValueError(
        f"Development user with ID {USER_ID} does not exist."
    )


SYSTEM_PROMPT = """
You are Talking Tomatoes, a friendly AI entertainment companion
specialising in movies and TV shows.

GENERAL RULES:
- Keep responses conversational and concise.
- Use available tools when you need real entertainment data.
- Never invent movie or TV show information.
- Never invent user preferences or viewing history.
- Do not repeat a tool call if you already have its result.
- Do not call unrelated tools.

MOVIE AND TV TOOLS:
- Use the appropriate TMDB tools to search, discover and retrieve
  movie and TV information.
- Never invent TMDB IDs or title information.

USER PREFERENCES:
- Use get_user_preferences when relevant.
- Consider liked and disliked genres.
- Respect the user's minimum rating preference.

PERSONAL LIBRARY:
- Use get_user_library to retrieve library entries.
- Distinguish favourites from library statuses.

VIEWING HISTORY:
- Use get_user_viewing_history when relevant.
- Never fabricate viewing history or ratings.

DATABASE WRITE OPERATIONS:
- Write tools can add, update or remove user data.
- When a write tool returns pending_confirmation, explain the
  proposed operation clearly.
- Ask the user to confirm before proceeding.
- Never claim an operation succeeded before confirmation.
- Never claim that a pending operation has been completed.
- Do not repeat a write tool call when it returns pending_confirmation.

PERSONALISED RECOMMENDATIONS:
- Retrieve saved preferences when relevant.
- Use TMDB discovery tools to retrieve actual candidate titles.
- Consider liked genres, disliked genres and minimum rating.
- Explain why recommendations match the user's preferences.

FINAL RESPONSES:
- Present actual information returned by tools.
- Clearly distinguish retrieved facts from suggestions.
- Keep responses conversational and concise.
"""


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def handle_pending_confirmation(user_input):
    """Handle explicit yes/no responses to pending actions."""

    action = get_pending_action(USER_ID)

    if action is None:
        return False

    answer = user_input.strip().lower()

    affirmative = {
        "yes", "yes please", "confirm", "confirmed",
        "go ahead", "do it", "proceed"
    }

    negative = {
        "no", "no thanks", "cancel", "don't",
        "dont", "stop", "never mind", "nevermind"
    }

    if answer in affirmative:

        result = confirm_pending_action(
            user_id=USER_ID,
            action_id=action["action_id"]
        )

        messages.append({
            "role": "user",
            "content": user_input
        })

        if result["success"]:
            response = (
                "Done! The requested change has been saved."
            )
        else:
            response = (
                "I couldn't complete that change: "
                + result["message"]
            )

        messages.append({
            "role": "assistant",
            "content": response
        })

        print("\nTalking Tomatoes:", response)
        return True

    if answer in negative:

        cancel_pending_action(USER_ID)

        messages.append({
            "role": "user",
            "content": user_input
        })

        response = "No problem! I've cancelled that action."

        messages.append({
            "role": "assistant",
            "content": response
        })

        print("\nTalking Tomatoes:", response)
        return True

    print(
        "\nTalking Tomatoes: Please answer yes or no "
        "to confirm or cancel the pending action."
    )

    return True


print(f"Talking Tomatoes is ready, {user['username']}!")
print("Type 'exit' to quit.")


while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nTalking Tomatoes: See you next time!")
        break

    if not user_input:
        continue

    # Resolve pending confirmations before calling the LLM.
    if handle_pending_confirmation(user_input):
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        response, messages = run_agent(
            client,
            messages,
            user_id=USER_ID
        )

        print("\nTalking Tomatoes:", response)

    except APITimeoutError:
        print(
            "\nTalking Tomatoes: The request took too long. "
            "Please try again."
        )

    except APIConnectionError:
        print(
            "\nTalking Tomatoes: Unable to connect. "
            "Check your internet connection."
        )

    except AuthenticationError:
        print(
            "\nTalking Tomatoes: API authentication failed. "
            "Check your API key."
        )

    except RateLimitError:
        print(
            "\nTalking Tomatoes: API rate limit reached. "
            "Please try again later."
        )

    except APIStatusError as error:
        print("\nAPI Status Code:", error.status_code)
        print("API Error Details:", error.response.text)

    except Exception as error:
        print("\nAn unexpected error occurred:", error)
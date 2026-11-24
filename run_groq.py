import os

from dotenv import load_dotenv
from src.agent.agent import run_agent
from src.agent.prompts import SYSTEM_PROMPT
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
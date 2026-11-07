import os

from dotenv import load_dotenv
from groq import (
    Groq,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError
)

from src.agent.agent import run_agent


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
You are Talking Tomatoes, a friendly entertainment companion
who recommends movies and TV shows.

Keep your responses conversational and concise.
Use available tools when you need information from them.
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

print("Talking Tomatoes is ready! Type 'exit' to quit.")

while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Talking Tomatoes: See you next time!")
        break

    if not user_input:
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response, messages = run_agent(client, messages)
        print("\nTalking Tomatoes:", response)

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

    except APIStatusError as e:
        print(f"\nTalking Tomatoes: API error ({e.status_code}).")

    except Exception as e:
        print("\nAn unexpected error occurred:", e)
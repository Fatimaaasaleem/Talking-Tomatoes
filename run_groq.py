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


SYSTEM_PROMPT = """
You are Talking Tomatoes, a friendly entertainment companion
who recommends movies and TV shows.

GENERAL RULES:
- Keep responses conversational and concise.
- Use available tools when you need real entertainment data.
- Never invent movie or TV show information.
- Do not repeat a tool call if you already have its result.
- Do not call unrelated tools.
- Once you have enough information, stop calling tools.

MOVIE SEARCH:
- Use search_movie to find movies by title.
- Use discover_movies to find movies by genre, year, or rating.
- Use get_movie_details for detailed movie information.
- Use get_similar_movies to find similar movies.

TV SEARCH:
- Use search_tv to find TV shows by title.
- Use discover_tv to find TV shows by genre, year, or rating.
- Use get_tv_details for detailed TV information.
- Use get_similar_tv to find similar TV shows.

SIMILARITY REQUESTS:
- For similar movies, first use search_movie to identify the movie.
- Then use get_similar_movies with its TMDB ID.
- For similar TV shows, first use search_tv to identify the show.
- Then use get_similar_tv with its TMDB ID.
- Never call discovery tools for similarity requests.
- Do not repeat searches when you already have the required ID.

DISCOVERY REQUESTS:
- For movie discovery, use discover_movies.
- For TV discovery, use discover_tv.
- Pass the user's genre, year, and rating preferences when available.
- Do not call search_movie or search_tv for discovery requests.
- Do not repeat a discovery call if you already have its results.

FINAL RESPONSES:
- Present the actual results returned by the tools.
- Never invent results.
- Once the requested information has been retrieved, respond to
  the user without making additional tool calls.
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
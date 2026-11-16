import os
import requests

from dotenv import load_dotenv


load_dotenv()


class TMDBClient:

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):

        token = os.getenv("TMDB_BEARER_TOKEN")

        if not token:
            raise ValueError("TMDB_BEARER_TOKEN is missing.")

        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        })

    def get(self, endpoint, params=None):

        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"TMDB API request failed: {error}"
            ) from error
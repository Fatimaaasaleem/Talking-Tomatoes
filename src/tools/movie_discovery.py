from src.services.tmdb_client import TMDBClient


def list_supported_genres() -> list[str]:
    return [
        "Action",
        "Comedy",
        "Drama",
        "Horror",
        "Romance",
        "Sci-Fi",
        "Thriller"
    ]


def search_movie(query: str, limit: int = 5) -> list[dict]:

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query must be a non-empty string.")

    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    tmdb = TMDBClient()

    response = tmdb.get(
        "search/movie",
        params={
            "query": query.strip(),
            "include_adult": False,
            "page": 1
        }
    )

    movies = []

    for movie in response.get("results", [])[:limit]:
        movies.append({
            "id": movie["id"],
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "poster_path": movie.get("poster_path"),
            "genre_ids": movie.get("genre_ids", [])
        })

    return movies


def search_tv(query: str, limit: int = 5) -> list[dict]:

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query must be a non-empty string.")

    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    tmdb = TMDBClient()

    response = tmdb.get(
        "search/tv",
        params={
            "query": query.strip(),
            "page": 1
        }
    )

    shows = []

    for show in response.get("results", [])[:limit]:
        shows.append({
            "id": show["id"],
            "name": show.get("name"),
            "first_air_date": show.get("first_air_date"),
            "overview": show.get("overview"),
            "rating": show.get("vote_average"),
            "poster_path": show.get("poster_path"),
            "genre_ids": show.get("genre_ids", [])
        })

    return shows


def discover_movies(
    genre: str | None = None,
    year: int | None = None,
    min_rating: float | None = None,
    limit: int = 5
) -> list[dict]:

    if genre is not None and (
        not isinstance(genre, str) or not genre.strip()
    ):
        raise ValueError("Genre must be a non-empty string.")

    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not 1 <= limit <= 20
    ):
        raise ValueError("Limit must be between 1 and 20.")

    if year is not None and (
        not isinstance(year, int)
        or isinstance(year, bool)
        or year <= 0
    ):
        raise ValueError("Year must be a positive integer.")

    if min_rating is not None and (
        not isinstance(min_rating, (int, float))
        or isinstance(min_rating, bool)
        or not 0 <= min_rating <= 10
    ):
        raise ValueError("Minimum rating must be between 0 and 10.")

    genre_ids = {
        "action": 28,
        "comedy": 35,
        "drama": 18,
        "horror": 27,
        "romance": 10749,
        "sci-fi": 878,
        "thriller": 53
    }

    params = {
        "sort_by": "popularity.desc",
        "page": 1
    }

    if genre is not None:
        genre_key = genre.strip().lower()

        if genre_key not in genre_ids:
            raise ValueError(f"Unsupported genre: {genre}")

        params["with_genres"] = genre_ids[genre_key]

    if year is not None:
        params["primary_release_year"] = year

    if min_rating is not None:
        params["vote_average.gte"] = min_rating

    tmdb = TMDBClient()

    response = tmdb.get(
        "discover/movie",
        params=params
    )

    movies = []

    for movie in response.get("results", [])[:limit]:
        movies.append({
            "id": movie["id"],
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "poster_path": movie.get("poster_path"),
            "genre_ids": movie.get("genre_ids", [])
        })

    return movies

def get_tv_details(tv_id: int) -> dict:

    if (
        not isinstance(tv_id, int)
        or isinstance(tv_id, bool)
        or tv_id <= 0
    ):
        raise ValueError("TV ID must be a positive integer.")

    tmdb = TMDBClient()

    show = tmdb.get(f"tv/{tv_id}")

    return {
        "id": show.get("id"),
        "name": show.get("name"),
        "original_name": show.get("original_name"),
        "first_air_date": show.get("first_air_date"),
        "last_air_date": show.get("last_air_date"),
        "overview": show.get("overview"),
        "rating": show.get("vote_average"),
        "poster_path": show.get("poster_path"),
        "number_of_seasons": show.get("number_of_seasons"),
        "number_of_episodes": show.get("number_of_episodes"),
        "episode_run_time": show.get("episode_run_time", []),
        "genres": [
            genre["name"]
            for genre in show.get("genres", [])
        ],
        "tagline": show.get("tagline"),
        "status": show.get("status")
    }
def get_movie_details(movie_id: int) -> dict:

    if (
        not isinstance(movie_id, int)
        or isinstance(movie_id, bool)
        or movie_id <= 0
    ):
        raise ValueError("Movie ID must be a positive integer.")

    tmdb = TMDBClient()

    movie = tmdb.get(f"movie/{movie_id}")

    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "original_title": movie.get("original_title"),
        "release_date": movie.get("release_date"),
        "overview": movie.get("overview"),
        "rating": movie.get("vote_average"),
        "poster_path": movie.get("poster_path"),
        "runtime": movie.get("runtime"),
        "genres": [
            genre["name"]
            for genre in movie.get("genres", [])
        ],
        "tagline": movie.get("tagline"),
        "status": movie.get("status")
    }
def get_similar_movies(movie_id: int, limit: int = 5) -> list[dict]:

    if (
        not isinstance(movie_id, int)
        or isinstance(movie_id, bool)
        or movie_id <= 0
    ):
        raise ValueError("Movie ID must be a positive integer.")

    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not 1 <= limit <= 20
    ):
        raise ValueError("Limit must be between 1 and 20.")

    tmdb = TMDBClient()

    response = tmdb.get(
        f"movie/{movie_id}/similar",
        params={"page": 1}
    )

    movies = []

    for movie in response.get("results", [])[:limit]:
        movies.append({
            "id": movie["id"],
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "poster_path": movie.get("poster_path"),
            "genre_ids": movie.get("genre_ids", [])
        })

    return movies

def get_similar_tv(tv_id, limit=5):
    if not isinstance(tv_id, int) or isinstance(tv_id, bool) or tv_id <= 0:
        raise ValueError("tv_id must be a positive integer.")

    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer between 1 and 20.")

    client = TMDBClient()

    data = client.get(
        f"tv/{tv_id}/similar",
        params={"page": 1}
    )

    return [
        {
            "id": show["id"],
            "name": show["name"],
            "first_air_date": show.get("first_air_date"),
            "overview": show.get("overview"),
            "rating": show.get("vote_average"),
            "poster_path": show.get("poster_path"),
            "genre_ids": show.get("genre_ids", [])
        }
        for show in data.get("results", [])[:limit]
    ]
    
    
def discover_tv(genre=None, year=None, min_rating=None, limit=5):
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer between 1 and 20.")

    genre_map = {
        "action": 10759,
        "comedy": 35,
        "drama": 18,
        "sci-fi": 10765
    }

    params = {
        "sort_by": "popularity.desc",
        "page": 1
    }

    if genre is not None:
        if not isinstance(genre, str) or genre.lower() not in genre_map:
            raise ValueError(
                "Unsupported TV genre. Choose Action, Comedy, Drama, or Sci-Fi."
            )
        params["with_genres"] = genre_map[genre.lower()]

    if year is not None:
        if not isinstance(year, int) or isinstance(year, bool) or year < 1900:
            raise ValueError("year must be a valid integer.")
        params["first_air_date_year"] = year

    if min_rating is not None:
        if not isinstance(min_rating, (int, float)) or isinstance(min_rating, bool) or not 0 <= min_rating <= 10:
            raise ValueError("min_rating must be between 0 and 10.")
        params["vote_average.gte"] = min_rating

    client = TMDBClient()
    data = client.get("discover/tv", params=params)

    return [
        {
            "id": show["id"],
            "name": show["name"],
            "first_air_date": show.get("first_air_date"),
            "overview": show.get("overview"),
            "rating": show.get("vote_average"),
            "poster_path": show.get("poster_path"),
            "genre_ids": show.get("genre_ids", [])
        }
        for show in data.get("results", [])[:limit]
    ]
    
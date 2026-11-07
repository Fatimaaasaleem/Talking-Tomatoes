def discover_movies(
    genre: str | None = None,
    year: int | None = None,
    min_rating: float | None = None,
    limit: int = 5
) -> list[dict]:
    #validate genre
    if genre is not None and (not isinstance(genre, str) or not genre.strip()):
        raise ValueError("Genre must be a non-empty string.")

    # Validate limit
    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    # Validate year
    if year is not None and (not isinstance(year, int) or isinstance(year, bool) or year <= 0):
        raise ValueError("Year must be a positive integer.")

    # Validate rating
    if min_rating is not None and (
        not isinstance(min_rating, (int, float))
        or isinstance(min_rating, bool)
        or not 0 <= min_rating <= 10
    ):
        raise ValueError("Minimum rating must be between 0 and 10.")

    # Movie discovery logic will go here
    pass



def list_supported_genres() -> list[str]:
    # This function would return a list of supported genres
    # For demonstration purposes, we will return a static list
    return ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"]
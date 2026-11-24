from src.tools.movie_discovery import (
    discover_movies,
    discover_tv
)

from src.tools.database_tools import (
    get_user_preferences,
    get_user_library,
    get_user_recommendation_feedback
)


def get_personalized_recommendations(
    user_id: int,
    media_type: str = "movie",
    limit: int = 5
) -> list[dict]:
    """Generate recommendations based on a user's preferences."""

    if media_type not in ("movie", "tv"):
        raise ValueError("Media type must be 'movie' or 'tv'.")

    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not 1 <= limit <= 20
    ):
        raise ValueError("Limit must be between 1 and 20.")

    user_preferences = get_user_preferences(user_id)

    preferences = user_preferences.get("preferences") or {}
    genres = user_preferences.get("genres") or {}

    liked_genres = genres.get("liked", [])
    disliked_genres = genres.get("disliked", [])

    min_rating = preferences.get("min_rating", 0)

    if min_rating is None:
        min_rating = 0

    if (
        not isinstance(min_rating, (int, float))
        or isinstance(min_rating, bool)
        or not 0 <= min_rating <= 10
    ):
        raise ValueError("Stored minimum rating must be between 0 and 10.")

    # Retrieve titles already saved by the user.
    library = get_user_library(
        user_id=user_id,
        media_type=media_type
    )

    excluded_ids = {
        entry["tmdb_id"]
        for entry in library
    }

    # Retrieve titles the user has explicitly rejected.
    feedback = get_user_recommendation_feedback(user_id)

    for entry in feedback:
        if (
            entry["media_type"] == media_type
            and entry["feedback"] in ("disliked", "not_interested")
        ):
            excluded_ids.add(entry["tmdb_id"])

    # Generate candidates.
    discover_function = (
        discover_movies if media_type == "movie"
        else discover_tv
    )

    candidates = {}

    # Discover popular titles as a general candidate pool.
    results = discover_function(
        min_rating=min_rating,
        limit=20
    )

    for item in results:
        candidates[item["id"]] = item

    # Discover additional titles from liked genres.
    for genre in liked_genres:
        try:
            results = discover_function(
                genre=genre,
                min_rating=min_rating,
                limit=20
            )

            for item in results:
                candidates[item["id"]] = item

        except ValueError:
            # Skip genres unsupported by the selected media type.
            continue

    # TMDB genre IDs by media type.
    genre_ids = {
        "action": {"movie": 28, "tv": 10759},
        "comedy": {"movie": 35, "tv": 35},
        "drama": {"movie": 18, "tv": 18},
        "horror": {"movie": 27},
        "romance": {"movie": 10749},
        "sci-fi": {"movie": 878, "tv": 10765},
        "thriller": {"movie": 53}
    }

    liked_ids = {
        genre_ids[genre.lower()][media_type]
        for genre in liked_genres
        if genre.lower() in genre_ids
        and media_type in genre_ids[genre.lower()]
    }

    disliked_ids = {
        genre_ids[genre.lower()][media_type]
        for genre in disliked_genres
        if genre.lower() in genre_ids
        and media_type in genre_ids[genre.lower()]
    }

    recommendations = []

    for item in candidates.values():

        if item["id"] in excluded_ids:
            continue

        item_genres = set(item.get("genre_ids", []))

        if item_genres.intersection(disliked_ids):
            continue

        liked_matches = item_genres.intersection(liked_ids)

        # Genre matches are the primary ranking signal.
        genre_score = len(liked_matches) * 10

        # TMDB rating provides a secondary ranking signal.
        rating_score = item.get("rating") or 0

        item["recommendation_score"] = (
            genre_score + rating_score
        )

        recommendations.append(item)

    recommendations.sort(
        key=lambda item: item["recommendation_score"],
        reverse=True
    )

    return recommendations[:limit]
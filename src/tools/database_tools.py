from src.database.operations import (
    get_preferences,
    get_genre_preferences,
    get_library,
    get_viewing_history,
    save_preferences,
    add_genre_preference,
    remove_genre_preference,
    add_to_library,
    update_library_status,
    set_library_favourite,
    remove_from_library,
    update_viewing_progress,
    add_viewing_history,
    get_recommendation_feedback,
save_recommendation_feedback,
remove_recommendation_feedback,
)


# ==========================================
# READ TOOLS
# ==========================================

def get_user_preferences(user_id):
    """Retrieve a user's general and genre preferences."""

    return {
        "preferences": get_preferences(user_id),
        "genres": get_genre_preferences(user_id)
    }


def get_user_library(
    user_id,
    status=None,
    media_type=None,
    is_favourite=None
):
    """Retrieve a user's personal entertainment library."""

    return get_library(
        user_id=user_id,
        status=status,
        media_type=media_type,
        is_favourite=is_favourite
    )


def get_user_viewing_history(user_id, media_type=None, limit=20):
    """Retrieve a user's viewing history."""

    return get_viewing_history(
        user_id=user_id,
        media_type=media_type,
        limit=limit
    )


# ==========================================
# WRITE TOOLS
# ==========================================

def update_user_preferences(user_id, language="English", min_rating=0):
    """Update a user's general preferences."""

    save_preferences(
        user_id=user_id,
        language=language,
        min_rating=min_rating
    )

    return {"success": True, "message": "Preferences updated."}


def add_user_genre_preference(user_id, genre, preference_type):
    """Add a liked or disliked genre."""

    result = add_genre_preference(
        user_id=user_id,
        genre=genre,
        preference_type=preference_type
    )

    return {"success": result}


def remove_user_genre_preference(user_id, genre, preference_type):
    """Remove a liked or disliked genre."""

    result = remove_genre_preference(
        user_id=user_id,
        genre=genre,
        preference_type=preference_type
    )

    return {"success": result}


def add_user_library_entry(
    user_id,
    tmdb_id,
    media_type,
    status="watchlist",
    current_season=None,
    current_episode=None
):
    """Add a movie or TV show to the user's library."""

    add_to_library(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type,
        status=status,
        current_season=current_season,
        current_episode=current_episode
    )

    return {"success": True, "message": "Title added to library."}


def update_user_library_status(user_id, tmdb_id, media_type, status):
    """Update a title's library status."""

    result = update_library_status(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type,
        status=status
    )

    return {"success": result}


def update_user_favourite(user_id, tmdb_id, media_type, is_favourite):
    """Mark a title as favourite or remove its favourite status."""

    result = set_library_favourite(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type,
        is_favourite=is_favourite
    )

    return {"success": result}


def remove_user_library_entry(user_id, tmdb_id, media_type):
    """Remove a title from the user's library."""

    result = remove_from_library(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type
    )

    return {"success": result}


def update_user_viewing_progress(
    user_id,
    tmdb_id,
    current_season,
    current_episode
):
    """Update a TV show's current viewing progress."""

    result = update_viewing_progress(
        user_id=user_id,
        tmdb_id=tmdb_id,
        current_season=current_season,
        current_episode=current_episode
    )

    return {"success": result}


def record_user_viewing_history(
    user_id,
    tmdb_id,
    media_type,
    rating=None
):
    """Record a watched movie or TV show."""

    history_id = add_viewing_history(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type,
        rating=rating
    )

    return {
        "success": True,
        "history_id": history_id
    }
    
# ==========================================
# RECOMMENDATION FEEDBACK TOOLS
# ==========================================

def get_user_recommendation_feedback(user_id, feedback_type=None):
    """Retrieve a user's recommendation feedback."""

    return get_recommendation_feedback(
        user_id=user_id,
        feedback_type=feedback_type
    )


def record_recommendation_feedback(
    user_id,
    tmdb_id,
    media_type,
    feedback
):
    """Record or update a user's feedback on a title."""

    result = save_recommendation_feedback(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type,
        feedback=feedback
    )

    return {"success": result}


def remove_user_recommendation_feedback(user_id, tmdb_id, media_type):
    """Remove a user's feedback for a title."""

    result = remove_recommendation_feedback(
        user_id=user_id,
        tmdb_id=tmdb_id,
        media_type=media_type
    )

    return {"success": result}    
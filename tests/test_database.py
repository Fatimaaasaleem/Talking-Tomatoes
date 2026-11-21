import pytest

import src.database.connection as db_connection

from src.database.schema import create_tables
from src.database.operations import (
    create_user,
    get_user,
    save_preferences,
    get_preferences,
    add_genre_preference,
    get_genre_preferences,
    remove_genre_preference,
    add_to_library,
    get_library,
    update_library_status,
    remove_from_library,
    update_viewing_progress,
    add_viewing_history,
    get_viewing_history,
    set_library_favourite,
)


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """
    Give each test its own temporary SQLite database.
    """
    monkeypatch.setattr(
        db_connection,
        "DATABASE_PATH",
        tmp_path / "test_database.db"
    )

    create_tables()


def test_create_and_get_user(test_db):
    user_id = create_user("test_user")

    user = get_user(user_id)

    assert user is not None
    assert user["username"] == "test_user"


def test_save_and_get_preferences(test_db):
    user_id = create_user("preference_user")

    save_preferences(user_id, "English", 7.5)

    preferences = get_preferences(user_id)

    assert preferences["language"] == "English"
    assert preferences["min_rating"] == 7.5


def test_genre_preferences(test_db):
    user_id = create_user("genre_user")

    assert add_genre_preference(user_id, "Drama", "liked")
    assert add_genre_preference(user_id, "Horror", "disliked")

    preferences = get_genre_preferences(user_id)

    assert "Drama" in preferences["liked"]
    assert "Horror" in preferences["disliked"]

    assert remove_genre_preference(user_id, "Drama", "liked")


def test_add_and_get_library(test_db):
    user_id = create_user("library_user")

    add_to_library(
        user_id,
        550,
        "movie",
        "watchlist"
    )

    library = get_library(user_id)

    assert len(library) == 1
    assert library[0]["tmdb_id"] == 550
    assert library[0]["status"] == "watchlist"


def test_update_library_status(test_db):
    user_id = create_user("status_user")

    add_to_library(user_id, 550, "movie", "watchlist")

    result = update_library_status(
        user_id,
        550,
        "movie",
        "completed"
    )

    assert result is True

    library = get_library(user_id)

    assert library[0]["status"] == "completed"


def test_remove_from_library(test_db):
    user_id = create_user("remove_user")

    add_to_library(user_id, 550, "movie", "watchlist")

    result = remove_from_library(user_id, 550, "movie")

    assert result is True
    assert get_library(user_id) == []


def test_update_viewing_progress(test_db):
    user_id = create_user("progress_user")

    add_to_library(
        user_id,
        1396,
        "tv",
        "watching",
        1,
        1
    )

    result = update_viewing_progress(
        user_id,
        1396,
        2,
        5
    )

    assert result is True

    library = get_library(user_id, media_type="tv")

    assert library[0]["current_season"] == 2
    assert library[0]["current_episode"] == 5


def test_add_and_get_viewing_history(test_db):
    user_id = create_user("history_user")

    add_viewing_history(
        user_id,
        157336,
        "movie",
        9.5
    )

    history = get_viewing_history(user_id)

    assert len(history) == 1
    assert history[0]["tmdb_id"] == 157336
    assert history[0]["rating"] == 9.5


def test_viewing_history_media_filter(test_db):
    user_id = create_user("filter_user")

    add_viewing_history(user_id, 157336, "movie", 9.5)
    add_viewing_history(user_id, 1396, "tv", 8.5)

    movie_history = get_viewing_history(
        user_id,
        media_type="movie"
    )

    assert len(movie_history) == 1
    assert movie_history[0]["media_type"] == "movie"
    
    
    

def test_favourite_is_independent_of_status(test_db):
    user_id = create_user("favourite_user")

    add_to_library(user_id, 1396, "tv", "watching")

    assert set_library_favourite(
        user_id, 1396, "tv", True
    )

    library = get_library(user_id)

    assert library[0]["status"] == "watching"
    assert library[0]["is_favourite"] is True


def test_remove_favourite_preserves_status(test_db):
    user_id = create_user("unfavourite_user")

    add_to_library(user_id, 1396, "tv", "watching")
    set_library_favourite(user_id, 1396, "tv", True)

    assert set_library_favourite(
        user_id, 1396, "tv", False
    )

    library = get_library(user_id)

    assert library[0]["status"] == "watching"
    assert library[0]["is_favourite"] is False


def test_filter_favourites(test_db):
    user_id = create_user("filter_favourites_user")

    add_to_library(user_id, 550, "movie", "completed")
    add_to_library(user_id, 1396, "tv", "watching")

    set_library_favourite(user_id, 1396, "tv", True)

    favourites = get_library(user_id, is_favourite=True)

    assert len(favourites) == 1
    assert favourites[0]["tmdb_id"] == 1396


def test_adding_existing_tv_show_preserves_progress(test_db):
    user_id = create_user("progress_preservation_user")

    add_to_library(
        user_id, 1396, "tv", "watching", 2, 5
    )

    add_to_library(
        user_id, 1396, "tv", "watching"
    )

    library = get_library(user_id, media_type="tv")

    assert library[0]["current_season"] == 2
    assert library[0]["current_episode"] == 5
    
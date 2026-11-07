from src.tools.movie_discovery import list_supported_genres


def test_list_supported_genres_returns_list():
    genres = list_supported_genres()

    assert isinstance(genres, list)


def test_list_supported_genres_contains_expected_genres():
    genres = list_supported_genres()

    expected_genres = [
        "Action",
        "Comedy",
        "Drama",
        "Horror",
        "Romance",
        "Sci-Fi",
        "Thriller"
    ]

    assert genres == expected_genres
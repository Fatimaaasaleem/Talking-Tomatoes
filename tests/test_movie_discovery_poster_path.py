from src.tools.movie_discovery import (
    discover_tv,
    search_movie,
    search_tv,
    discover_movies,
    get_movie_details,
    get_tv_details,
    get_similar_movies,
    get_similar_tv
)


def patch_tmdb(monkeypatch, payload):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            return payload

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )


def movie_payload():
    return {
        "results": [
            {
                "id": 1,
                "title": "Poster Movie",
                "poster_path": "/movie.jpg"
            }
        ]
    }


def tv_payload():
    return {
        "results": [
            {
                "id": 2,
                "name": "Poster Show",
                "poster_path": "/show.jpg"
            }
        ]
    }


def test_search_movie_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, movie_payload())

    assert search_movie("test")[0]["poster_path"] == "/movie.jpg"


def test_search_tv_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, tv_payload())

    assert search_tv("test")[0]["poster_path"] == "/show.jpg"


def test_discover_movies_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, movie_payload())

    assert discover_movies()[0]["poster_path"] == "/movie.jpg"


def test_discover_tv_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, tv_payload())

    assert discover_tv()[0]["poster_path"] == "/show.jpg"


def test_get_similar_movies_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, movie_payload())

    assert get_similar_movies(1)[0]["poster_path"] == "/movie.jpg"


def test_get_similar_tv_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, tv_payload())

    assert get_similar_tv(2)[0]["poster_path"] == "/show.jpg"


def test_get_movie_details_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, {
        "id": 1,
        "title": "Poster Movie",
        "poster_path": "/movie.jpg"
    })

    assert get_movie_details(1)["poster_path"] == "/movie.jpg"


def test_get_tv_details_includes_poster_path(monkeypatch):
    patch_tmdb(monkeypatch, {
        "id": 2,
        "name": "Poster Show",
        "poster_path": "/show.jpg"
    })

    assert get_tv_details(2)["poster_path"] == "/show.jpg"


def test_list_results_poster_path_is_none_when_missing(monkeypatch):
    patch_tmdb(monkeypatch, {
        "results": [{"id": 1, "title": "No Poster"}]
    })

    assert search_movie("test")[0]["poster_path"] is None


def test_details_poster_path_is_none_when_tmdb_returns_null(monkeypatch):
    patch_tmdb(monkeypatch, {
        "id": 1,
        "title": "No Poster",
        "poster_path": None
    })

    assert get_movie_details(1)["poster_path"] is None
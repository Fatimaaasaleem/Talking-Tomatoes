from src.tools.movie_discovery import (
    discover_tv,
    list_supported_genres,
    search_movie,
    search_tv,
    discover_movies,
    get_movie_details,
    get_tv_details,
    get_similar_movies,
    get_similar_tv
)

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
    
    
def test_search_movie_returns_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "search/movie"
            assert params["query"] == "Interstellar"

            return {
                "results": [
                    {
                        "id": 157336,
                        "title": "Interstellar",
                        "release_date": "2014-11-05",
                        "overview": "A team travels through a wormhole.",
                        "vote_average": 8.5,
                        "genre_ids": [12, 18, 878]
                    }
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = search_movie("Interstellar")

    assert len(results) == 1
    assert results[0]["title"] == "Interstellar"
    assert results[0]["id"] == 157336


def test_search_movie_rejects_empty_query():

    import pytest

    with pytest.raises(ValueError):
        search_movie("")


def test_search_movie_rejects_invalid_limit():

    import pytest

    with pytest.raises(ValueError):
        search_movie("Interstellar", limit=0)


def test_search_movie_respects_limit(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            return {
                "results": [
                    {"id": 1, "title": "Movie 1"},
                    {"id": 2, "title": "Movie 2"},
                    {"id": 3, "title": "Movie 3"}
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = search_movie("test", limit=2)

    assert len(results) == 2    
    
def test_search_tv_returns_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "search/tv"
            assert params["query"] == "Breaking Bad"

            return {
                "results": [
                    {
                        "id": 1396,
                        "name": "Breaking Bad",
                        "first_air_date": "2008-01-20",
                        "overview": "A chemistry teacher turns to crime.",
                        "vote_average": 8.9,
                        "genre_ids": [18, 80]
                    }
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = search_tv("Breaking Bad")

    assert len(results) == 1
    assert results[0]["name"] == "Breaking Bad"
    assert results[0]["id"] == 1396


def test_search_tv_rejects_empty_query():

    import pytest

    with pytest.raises(ValueError):
        search_tv("")


def test_search_tv_rejects_invalid_limit():

    import pytest

    with pytest.raises(ValueError):
        search_tv("Breaking Bad", limit=0)


def test_search_tv_respects_limit(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            return {
                "results": [
                    {"id": 1, "name": "Show 1"},
                    {"id": 2, "name": "Show 2"},
                    {"id": 3, "name": "Show 3"}
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = search_tv("test", limit=2)

    assert len(results) == 2   
    
    
def test_discover_movies_returns_filtered_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "discover/movie"
            assert params["with_genres"] == 27
            assert params["primary_release_year"] == 2020
            assert params["vote_average.gte"] == 7
            assert params["sort_by"] == "popularity.desc"

            return {
                "results": [
                    {
                        "id": 1,
                        "title": "Test Horror Movie",
                        "release_date": "2020-05-10",
                        "overview": "A horror movie.",
                        "vote_average": 7.5,
                        "genre_ids": [27]
                    }
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = discover_movies(
        genre="Horror",
        year=2020,
        min_rating=7,
        limit=5
    )

    assert len(results) == 1
    assert results[0]["title"] == "Test Horror Movie"


def test_discover_movies_rejects_unsupported_genre():

    import pytest

    with pytest.raises(ValueError):
        discover_movies(genre="Fantasy")


def test_discover_movies_rejects_invalid_year():

    import pytest

    with pytest.raises(ValueError):
        discover_movies(year=-2020)


def test_discover_movies_rejects_invalid_rating():

    import pytest

    with pytest.raises(ValueError):
        discover_movies(min_rating=11)


def test_discover_movies_rejects_invalid_limit():

    import pytest

    with pytest.raises(ValueError):
        discover_movies(limit=0)


def test_discover_movies_respects_limit(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            return {
                "results": [
                    {"id": 1, "title": "Movie 1"},
                    {"id": 2, "title": "Movie 2"},
                    {"id": 3, "title": "Movie 3"}
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = discover_movies(limit=2)

    assert len(results) == 2     
    
def test_get_movie_details_returns_details(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "movie/157336"

            return {
                "id": 157336,
                "title": "Interstellar",
                "original_title": "Interstellar",
                "release_date": "2014-11-05",
                "overview": "A team travels through a wormhole.",
                "vote_average": 8.5,
                "runtime": 169,
                "genres": [
                    {"name": "Adventure"},
                    {"name": "Drama"},
                    {"name": "Science Fiction"}
                ],
                "tagline": "Mankind was born on Earth.",
                "status": "Released"
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    movie = get_movie_details(157336)

    assert movie["title"] == "Interstellar"
    assert movie["runtime"] == 169
    assert movie["rating"] == 8.5
    assert "Drama" in movie["genres"]


def test_get_movie_details_rejects_invalid_id():

    import pytest

    with pytest.raises(ValueError):
        get_movie_details(0)    
        
def test_get_tv_details_returns_details(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "tv/1396"

            return {
                "id": 1396,
                "name": "Breaking Bad",
                "original_name": "Breaking Bad",
                "first_air_date": "2008-01-20",
                "last_air_date": "2013-09-29",
                "overview": "A chemistry teacher turns to crime.",
                "vote_average": 8.9,
                "number_of_seasons": 5,
                "number_of_episodes": 62,
                "episode_run_time": [45],
                "genres": [
                    {"name": "Drama"},
                    {"name": "Crime"}
                ],
                "tagline": "All hail the king.",
                "status": "Ended"
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    show = get_tv_details(1396)

    assert show["name"] == "Breaking Bad"
    assert show["number_of_seasons"] == 5
    assert show["number_of_episodes"] == 62
    assert "Drama" in show["genres"]


def test_get_tv_details_rejects_invalid_id():

    import pytest

    with pytest.raises(ValueError):
        get_tv_details(0)
        
        
def test_get_similar_movies_returns_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "movie/157336/similar"
            assert params == {"page": 1}

            return {
                "results": [
                    {
                        "id": 1,
                        "title": "Similar Movie",
                        "release_date": "2020-01-01",
                        "overview": "A science fiction movie.",
                        "vote_average": 8.0,
                        "genre_ids": [878]
                    }
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = get_similar_movies(157336)

    assert len(results) == 1
    assert results[0]["title"] == "Similar Movie"
    assert results[0]["id"] == 1  
    
def test_get_similar_tv_returns_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "tv/1396/similar"
            assert params == {"page": 1}

            return {
                "results": [
                    {
                        "id": 2,
                        "name": "Similar Show",
                        "first_air_date": "2020-01-01",
                        "overview": "A drama series.",
                        "vote_average": 8.5,
                        "genre_ids": [18]
                    }
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = get_similar_tv(1396)

    assert len(results) == 1
    assert results[0]["name"] == "Similar Show"
    assert results[0]["id"] == 2


def test_get_similar_tv_invalid_id():
    import pytest

    with pytest.raises(ValueError):
        get_similar_tv(-1)


def test_get_similar_tv_invalid_limit():
    import pytest

    with pytest.raises(ValueError):
        get_similar_tv(1396, limit=25)


def test_get_similar_tv_empty_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            return {"results": []}

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    assert get_similar_tv(1396) == []      
def test_discover_tv_returns_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            assert endpoint == "discover/tv"
            assert params["with_genres"] == 18
            assert params["first_air_date_year"] == 2020
            assert params["vote_average.gte"] == 7.5

            return {
                "results": [
                    {
                        "id": 1,
                        "name": "Test Show",
                        "first_air_date": "2020-01-01",
                        "overview": "A drama series.",
                        "vote_average": 8.0,
                        "genre_ids": [18]
                    }
                ]
            }

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    results = discover_tv(
        genre="Drama",
        year=2020,
        min_rating=7.5
    )

    assert len(results) == 1
    assert results[0]["name"] == "Test Show"


def test_discover_tv_invalid_genre():
    import pytest

    with pytest.raises(ValueError):
        discover_tv(genre="Horror")


def test_discover_tv_invalid_year():
    import pytest

    with pytest.raises(ValueError):
        discover_tv(year=1800)


def test_discover_tv_invalid_rating():
    import pytest

    with pytest.raises(ValueError):
        discover_tv(min_rating=11)


def test_discover_tv_invalid_limit():
    import pytest

    with pytest.raises(ValueError):
        discover_tv(limit=25)


def test_discover_tv_empty_results(monkeypatch):

    class FakeTMDBClient:

        def __init__(self):
            pass

        def get(self, endpoint, params=None):
            return {"results": []}

    monkeypatch.setattr(
        "src.tools.movie_discovery.TMDBClient",
        FakeTMDBClient
    )

    assert discover_tv() == []    
from src.tools import recommendations


def test_liked_genre_gets_higher_priority(monkeypatch):

    monkeypatch.setattr(
        recommendations,
        "get_user_preferences",
        lambda user_id: {
            "preferences": {"min_rating": 0},
            "genres": {"liked": ["Action"], "disliked": []}
        }
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_library",
        lambda **kwargs: []
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_recommendation_feedback",
        lambda user_id: []
    )

    def mock_discover_movies(genre=None, min_rating=None, limit=20):

        if genre == "Action":
            return [{
                "id": 1,
                "title": "Action Movie",
                "rating": 6.0,
                "genre_ids": [28]
            }]

        return [{
            "id": 2,
            "title": "Comedy Movie",
            "rating": 9.0,
            "genre_ids": [35]
        }]

    monkeypatch.setattr(
        recommendations,
        "discover_movies",
        mock_discover_movies
    )

    results = recommendations.get_personalized_recommendations(
        user_id=1,
        media_type="movie",
        limit=2
    )

    assert results[0]["title"] == "Action Movie"
    
def test_disliked_genre_is_excluded(monkeypatch):

    monkeypatch.setattr(
        recommendations,
        "get_user_preferences",
        lambda user_id: {
            "preferences": {"min_rating": 0},
            "genres": {"liked": [], "disliked": ["Horror"]}
        }
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_library",
        lambda **kwargs: []
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_recommendation_feedback",
        lambda user_id: []
    )

    monkeypatch.setattr(
        recommendations,
        "discover_movies",
        lambda **kwargs: [
            {
                "id": 1,
                "title": "Horror Movie",
                "rating": 9.0,
                "genre_ids": [27]
            },
            {
                "id": 2,
                "title": "Drama Movie",
                "rating": 7.0,
                "genre_ids": [18]
            }
        ]
    )

    results = recommendations.get_personalized_recommendations(
        user_id=1,
        media_type="movie",
        limit=5
    )

    assert all(item["id"] != 1 for item in results)
    assert any(item["id"] == 2 for item in results)  
    
def test_disliked_genre_is_excluded(monkeypatch):

    monkeypatch.setattr(
        recommendations,
        "get_user_preferences",
        lambda user_id: {
            "preferences": {"min_rating": 0},
            "genres": {"liked": [], "disliked": ["Horror"]}
        }
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_library",
        lambda **kwargs: []
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_recommendation_feedback",
        lambda user_id: []
    )

    monkeypatch.setattr(
        recommendations,
        "discover_movies",
        lambda **kwargs: [
            {
                "id": 1,
                "title": "Horror Movie",
                "rating": 9.0,
                "genre_ids": [27]
            },
            {
                "id": 2,
                "title": "Drama Movie",
                "rating": 7.0,
                "genre_ids": [18]
            }
        ]
    )

    results = recommendations.get_personalized_recommendations(
        user_id=1,
        media_type="movie",
        limit=5
    )

    assert all(item["id"] != 1 for item in results)
    assert any(item["id"] == 2 for item in results)  
    
def test_library_titles_are_excluded(monkeypatch):

    monkeypatch.setattr(
        recommendations,
        "get_user_preferences",
        lambda user_id: {
            "preferences": {"min_rating": 0},
            "genres": {"liked": [], "disliked": []}
        }
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_library",
        lambda **kwargs: [
            {"tmdb_id": 1}
        ]
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_recommendation_feedback",
        lambda user_id: []
    )

    monkeypatch.setattr(
        recommendations,
        "discover_movies",
        lambda **kwargs: [
            {
                "id": 1,
                "title": "Already Saved",
                "rating": 8.0,
                "genre_ids": [28]
            },
            {
                "id": 2,
                "title": "New Discovery",
                "rating": 7.0,
                "genre_ids": [18]
            }
        ]
    )

    results = recommendations.get_personalized_recommendations(
        user_id=1,
        media_type="movie",
        limit=5
    )

    assert all(item["id"] != 1 for item in results)
    assert any(item["id"] == 2 for item in results)  
    
def test_negative_feedback_titles_are_excluded(monkeypatch):

    monkeypatch.setattr(
        recommendations,
        "get_user_preferences",
        lambda user_id: {
            "preferences": {"min_rating": 0},
            "genres": {"liked": [], "disliked": []}
        }
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_library",
        lambda **kwargs: []
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_recommendation_feedback",
        lambda user_id: [
            {
                "tmdb_id": 1,
                "media_type": "movie",
                "feedback": "not_interested"
            }
        ]
    )

    monkeypatch.setattr(
        recommendations,
        "discover_movies",
        lambda **kwargs: [
            {
                "id": 1,
                "title": "Rejected Movie",
                "rating": 8.0,
                "genre_ids": [28]
            },
            {
                "id": 2,
                "title": "Other Movie",
                "rating": 7.0,
                "genre_ids": [18]
            }
        ]
    )

    results = recommendations.get_personalized_recommendations(
        user_id=1,
        media_type="movie",
        limit=5
    )

    assert all(item["id"] != 1 for item in results)
    assert any(item["id"] == 2 for item in results)    
    
def test_tv_recommendations(monkeypatch):

    monkeypatch.setattr(
        recommendations,
        "get_user_preferences",
        lambda user_id: {
            "preferences": {"min_rating": 0},
            "genres": {"liked": ["Drama"], "disliked": []}
        }
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_library",
        lambda **kwargs: []
    )

    monkeypatch.setattr(
        recommendations,
        "get_user_recommendation_feedback",
        lambda user_id: []
    )

    monkeypatch.setattr(
        recommendations,
        "discover_tv",
        lambda **kwargs: [
            {
                "id": 10,
                "name": "Drama Series",
                "rating": 8.0,
                "genre_ids": [18]
            }
        ]
    )

    results = recommendations.get_personalized_recommendations(
        user_id=1,
        media_type="tv",
        limit=5
    )

    assert len(results) == 1
    assert results[0]["name"] == "Drama Series"          
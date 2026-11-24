SUPPORTED_GENRES_TOOL = {
    "type": "function",
    "function": {
        "name": "list_supported_genres",
        "description": "Returns the list of movie genres supported by Talking Tomatoes.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
SEARCH_MOVIE_TOOL = {
    "type": "function",
    "function": {
        "name": "search_movie",
        "description": "Searches TMDB for movies matching a title or keyword and returns matching movie information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The movie title or keyword to search for."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of movie results to return. Defaults to 5."
                }
            },
            "required": ["query"]
        }
    }
}
SEARCH_TV_TOOL = {
    "type": "function",
    "function": {
        "name": "search_tv",
        "description": "Searches TMDB for TV shows matching a title or keyword and returns matching TV show information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The TV show title or keyword to search for."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of TV show results to return. Defaults to 5."
                }
            },
            "required": ["query"]
        }
    }
}
DISCOVER_MOVIES_TOOL = {
    "type": "function",
    "function": {
        "name": "discover_movies",
        "description": "Discovers movies using optional genre, release year, and minimum rating filters.",
        "parameters": {
            "type": "object",
            "properties": {
                "genre": {
                    "type": "string",
                    "description": "Movie genre: Action, Comedy, Drama, Horror, Romance, Sci-Fi, or Thriller."
                },
                "year": {
                    "type": "integer",
                    "description": "Movie release year."
                },
                "min_rating": {
                    "type": "number",
                    "description": "Minimum TMDB rating between 0 and 10."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results, between 1 and 20. Defaults to 5."
                }
            },
            "required": []
        }
    }
}
GET_MOVIE_DETAILS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_movie_details",
        "description": "Retrieves detailed information about a movie using its TMDB ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "movie_id": {
                    "type": "integer",
                    "description": "The TMDB ID of the movie."
                }
            },
            "required": ["movie_id"]
        }
    }
}
GET_TV_DETAILS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_tv_details",
        "description": "Retrieves detailed information about a TV show using its TMDB ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "tv_id": {
                    "type": "integer",
                    "description": "The TMDB ID of the TV show."
                }
            },
            "required": ["tv_id"]
        }
    }
}
GET_SIMILAR_MOVIES_TOOL = {
    "type": "function",
    "function": {
        "name": "get_similar_movies",
        "description": "Finds movies similar to a movie using its TMDB ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "movie_id": {
                    "type": "integer",
                    "description": "TMDB ID of the movie."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results, between 1 and 20. Defaults to 5."
                }
            },
            "required": ["movie_id"]
        }
    }
}
GET_SIMILAR_TV_TOOL = {
    "type": "function",
    "function": {
        "name": "get_similar_tv",
        "description": "Finds TV shows similar to a TV show using its TMDB ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "tv_id": {
                    "type": "integer",
                    "description": "TMDB ID of the TV show."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results, between 1 and 20. Defaults to 5."
                }
            },
            "required": ["tv_id"]
        }
    }
}

DISCOVER_TV_TOOL = {
    "type": "function",
    "function": {
        "name": "discover_tv",
        "description": "Discovers TV shows using genre, release year, and minimum rating filters.",
        "parameters": {
            "type": "object",
            "properties": {
                "genre": {
                    "type": "string",
                    "description": "TV genre: Action, Comedy, Drama, or Sci-Fi."
                },
                "year": {
                    "type": "integer",
                    "description": "First air date year."
                },
                "min_rating": {
                    "type": "number",
                    "description": "Minimum TMDB rating between 0 and 10."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results, between 1 and 20."
                }
            },
            "required": []
        }
    }
}
GET_USER_PREFERENCES_TOOL = {
    "type": "function",
    "function": {
        "name": "get_user_preferences",
        "description": "Retrieves the current user's language, minimum rating, liked genres, and disliked genres.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


GET_USER_LIBRARY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_user_library",
        "description": "Retrieves titles from the current user's personal library. Can filter by status, media type, or favourite status.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": [
                        "watchlist",
                        "watching",
                        "completed",
                        "dropped"
                    ],
                    "description": "Optional library status filter."
                },
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"],
                    "description": "Optional media type filter."
                },
                "is_favourite": {
                    "type": "boolean",
                    "description": "Filter by favourite status."
                }
            },
            "required": []
        }
    }
}


GET_USER_VIEWING_HISTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_user_viewing_history",
        "description": "Retrieves the current user's viewing history, including watched titles and ratings.",
        "parameters": {
            "type": "object",
            "properties": {
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"],
                    "description": "Optional media type filter."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of history records to retrieve. Defaults to 20."
                }
            },
            "required": []
        }
    }
}
GET_USER_RECOMMENDATION_FEEDBACK_TOOL = {
    "type": "function",
    "function": {
        "name": "get_user_recommendation_feedback",
        "description": "Retrieves the current user's feedback on recommended movies and TV shows.",
        "parameters": {
            "type": "object",
            "properties": {
                "feedback_type": {
                    "type": "string",
                    "enum": ["liked", "disliked", "not_interested"],
                    "description": "Optional feedback category filter."
                }
            },
            "required": []
        }
    }
}
# ==========================================
# DATABASE WRITE TOOLS
# ==========================================

UPDATE_USER_PREFERENCES_TOOL = {
    "type": "function",
    "function": {
        "name": "update_user_preferences",
        "description": "Updates the current user's language and minimum rating preference.",
        "parameters": {
            "type": "object",
            "properties": {
                "language": {"type": "string"},
                "min_rating": {"type": "number"}
            },
            "required": []
        }
    }
}

ADD_USER_GENRE_PREFERENCE_TOOL = {
    "type": "function",
    "function": {
        "name": "add_user_genre_preference",
        "description": "Adds a genre to the user's liked or disliked genres.",
        "parameters": {
            "type": "object",
            "properties": {
                "genre": {"type": "string"},
                "preference_type": {
                    "type": "string",
                    "enum": ["liked", "disliked"]
                }
            },
            "required": ["genre", "preference_type"]
        }
    }
}

REMOVE_USER_GENRE_PREFERENCE_TOOL = {
    "type": "function",
    "function": {
        "name": "remove_user_genre_preference",
        "description": "Removes a genre from the user's liked or disliked genres.",
        "parameters": {
            "type": "object",
            "properties": {
                "genre": {"type": "string"},
                "preference_type": {
                    "type": "string",
                    "enum": ["liked", "disliked"]
                }
            },
            "required": ["genre", "preference_type"]
        }
    }
}

ADD_USER_LIBRARY_ENTRY_TOOL = {
    "type": "function",
    "function": {
        "name": "add_user_library_entry",
        "description": "Adds a movie or TV show to the user's library.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                },
                "status": {
                    "type": "string",
                    "enum": ["watchlist", "watching", "completed", "dropped"]
                },
                "current_season": {"type": "integer"},
                "current_episode": {"type": "integer"}
            },
            "required": ["tmdb_id", "media_type"]
        }
    }
}

UPDATE_USER_LIBRARY_STATUS_TOOL = {
    "type": "function",
    "function": {
        "name": "update_user_library_status",
        "description": "Changes the status of a title in the user's library.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                },
                "status": {
                    "type": "string",
                    "enum": ["watchlist", "watching", "completed", "dropped"]
                }
            },
            "required": ["tmdb_id", "media_type", "status"]
        }
    }
}

UPDATE_USER_FAVOURITE_TOOL = {
    "type": "function",
    "function": {
        "name": "update_user_favourite",
        "description": "Marks a title as a favourite or removes its favourite status.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                },
                "is_favourite": {"type": "boolean"}
            },
            "required": ["tmdb_id", "media_type", "is_favourite"]
        }
    }
}

REMOVE_USER_LIBRARY_ENTRY_TOOL = {
    "type": "function",
    "function": {
        "name": "remove_user_library_entry",
        "description": "Removes a movie or TV show from the user's library.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                }
            },
            "required": ["tmdb_id", "media_type"]
        }
    }
}

UPDATE_USER_VIEWING_PROGRESS_TOOL = {
    "type": "function",
    "function": {
        "name": "update_user_viewing_progress",
        "description": "Updates the user's current season and episode for a TV show.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "current_season": {"type": "integer"},
                "current_episode": {"type": "integer"}
            },
            "required": [
                "tmdb_id",
                "current_season",
                "current_episode"
            ]
        }
    }
}

RECORD_USER_VIEWING_HISTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "record_user_viewing_history",
        "description": "Records a movie or TV show in the user's viewing history, optionally with a rating.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                },
                "rating": {
                    "type": "number",
                    "description": "Optional rating."
                }
            },
            "required": ["tmdb_id", "media_type"]
        }
    }
}
RECORD_RECOMMENDATION_FEEDBACK_TOOL = {
    "type": "function",
    "function": {
        "name": "record_recommendation_feedback",
        "description": "Records or updates the current user's feedback on a movie or TV show.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                },
                "feedback": {
                    "type": "string",
                    "enum": ["liked", "disliked", "not_interested"]
                }
            },
            "required": ["tmdb_id", "media_type", "feedback"]
        }
    }
}


REMOVE_USER_RECOMMENDATION_FEEDBACK_TOOL = {
    "type": "function",
    "function": {
        "name": "remove_user_recommendation_feedback",
        "description": "Removes the current user's feedback for a movie or TV show.",
        "parameters": {
            "type": "object",
            "properties": {
                "tmdb_id": {"type": "integer"},
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"]
                }
            },
            "required": ["tmdb_id", "media_type"]
        }
    }
}
# ==========================================
# PERSONALIZED RECOMMENDATIONS
# ==========================================

GET_PERSONALIZED_RECOMMENDATIONS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_personalized_recommendations",
        "description": (
            "Generates personalized movie or TV recommendations "
            "based on the current user's liked and disliked genres, "
            "minimum rating preference, personal library, and "
            "previous recommendation feedback. Excludes titles "
            "already in the user's library and titles they have "
            "disliked or marked as not interested."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "media_type": {
                    "type": "string",
                    "enum": ["movie", "tv"],
                    "description": "Whether to recommend movies or TV shows. Defaults to movie."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of recommendations to return, between 1 and 20. Defaults to 5."
                }
            },
            "required": []
        }
    }
}
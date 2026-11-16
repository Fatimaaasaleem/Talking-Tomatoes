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
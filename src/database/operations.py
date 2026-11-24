from src.database.connection import get_connection


# ==========================================
# USER OPERATIONS
# ==========================================

def create_user(username):
    """Create a new user and return their ID."""

    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username must be a non-empty string.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (username) VALUES (?)",
            (username.strip(),)
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def get_user(user_id):
    """Retrieve a user using their ID."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, username, created_at FROM users WHERE id = ?",
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        return {
            "id": user[0],
            "username": user[1],
            "created_at": user[2]
        }

    finally:
        connection.close()


# ==========================================
# GENERAL PREFERENCE OPERATIONS
# ==========================================

def save_preferences(user_id, language="English", min_rating=0):
    """Save or update a user's general preferences."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(language, str) or not language.strip():
        raise ValueError("Language must be a non-empty string.")

    if (
        not isinstance(min_rating, (int, float))
        or isinstance(min_rating, bool)
        or not 0 <= min_rating <= 10
    ):
        raise ValueError("Minimum rating must be between 0 and 10.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO preferences (user_id, language, min_rating)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET
                language = excluded.language,
                min_rating = excluded.min_rating
        """, (user_id, language.strip(), min_rating))

        connection.commit()

    finally:
        connection.close()


def get_preferences(user_id):
    """Retrieve a user's saved general preferences."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT language, min_rating
            FROM preferences
            WHERE user_id = ?
        """, (user_id,))

        preferences = cursor.fetchone()

        if preferences is None:
            return None

        return {
            "language": preferences[0],
            "min_rating": preferences[1]
        }

    finally:
        connection.close()


# ==========================================
# GENRE PREFERENCE OPERATIONS
# ==========================================

def add_genre_preference(user_id, genre, preference_type):
    """Add a liked or disliked genre for a user."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(genre, str) or not genre.strip():
        raise ValueError("Genre must be a non-empty string.")

    if preference_type not in ("liked", "disliked"):
        raise ValueError("Preference type must be 'liked' or 'disliked'.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO preference_genres
            (user_id, genre, preference_type)
            VALUES (?, ?, ?)
        """, (user_id, genre.strip().title(), preference_type))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def get_genre_preferences(user_id):
    """Retrieve all liked and disliked genres for a user."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT genre, preference_type
            FROM preference_genres
            WHERE user_id = ?
            ORDER BY genre
        """, (user_id,))

        results = cursor.fetchall()

        preferences = {
            "liked": [],
            "disliked": []
        }

        for genre, preference_type in results:
            preferences[preference_type].append(genre)

        return preferences

    finally:
        connection.close()


def remove_genre_preference(user_id, genre, preference_type):
    """Remove a specific genre preference."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(genre, str) or not genre.strip():
        raise ValueError("Genre must be a non-empty string.")

    if preference_type not in ("liked", "disliked"):
        raise ValueError("Preference type must be 'liked' or 'disliked'.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM preference_genres
            WHERE user_id = ?
            AND genre = ?
            AND preference_type = ?
        """, (user_id, genre.strip().title(), preference_type))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()





# ==========================================
# LIBRARY OPERATIONS
# ==========================================

VALID_MEDIA_TYPES = ("movie", "tv")

VALID_LIBRARY_STATUSES = (
    "watchlist",
    "watching",
    "completed",
    "dropped"
)


def add_to_library(
    user_id,
    tmdb_id,
    media_type,
    status="watchlist",
    current_season=None,
    current_episode=None
):
    """Add a title to a user's library or update its status."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if status not in VALID_LIBRARY_STATUSES:
        raise ValueError("Invalid library status.")

    if media_type == "movie" and (
        current_season is not None or current_episode is not None
    ):
        raise ValueError("Viewing progress is only supported for TV shows.")

    if current_season is not None and (
        not isinstance(current_season, int)
        or isinstance(current_season, bool)
        or current_season < 1
    ):
        raise ValueError("current_season must be a positive integer.")

    if current_episode is not None and (
        not isinstance(current_episode, int)
        or isinstance(current_episode, bool)
        or current_episode < 1
    ):
        raise ValueError("current_episode must be a positive integer.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO library (
                user_id,
                tmdb_id,
                media_type,
                status,
                current_season,
                current_episode
            )
            VALUES (?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id, tmdb_id, media_type)
            DO UPDATE SET
                status = excluded.status,
                current_season = COALESCE(
                    excluded.current_season,
                    library.current_season
                ),
                current_episode = COALESCE(
                    excluded.current_episode,
                    library.current_episode
                )
        """, (
            user_id,
            tmdb_id,
            media_type,
            status,
            current_season,
            current_episode
        ))

        connection.commit()
        return True

    finally:
        connection.close()


def get_library(
    user_id,
    status=None,
    media_type=None,
    is_favourite=None
):
    """Retrieve a user's library with optional filters."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if status is not None and status not in VALID_LIBRARY_STATUSES:
        raise ValueError("Invalid library status.")

    if media_type is not None and media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if is_favourite is not None and not isinstance(is_favourite, bool):
        raise ValueError("is_favourite must be True or False.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                tmdb_id,
                media_type,
                status,
                is_favourite,
                current_season,
                current_episode,
                added_at
            FROM library
            WHERE user_id = ?
        """

        parameters = [user_id]

        if status is not None:
            query += " AND status = ?"
            parameters.append(status)

        if media_type is not None:
            query += " AND media_type = ?"
            parameters.append(media_type)

        if is_favourite is not None:
            query += " AND is_favourite = ?"
            parameters.append(int(is_favourite))

        query += " ORDER BY added_at DESC"

        cursor.execute(query, parameters)
        results = cursor.fetchall()

        return [
            {
                "tmdb_id": row[0],
                "media_type": row[1],
                "status": row[2],
                "is_favourite": bool(row[3]),
                "current_season": row[4],
                "current_episode": row[5],
                "added_at": row[6]
            }
            for row in results
        ]

    finally:
        connection.close()


def update_library_status(user_id, tmdb_id, media_type, status):
    """Update the status of an existing library entry."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if status not in VALID_LIBRARY_STATUSES:
        raise ValueError("Invalid library status.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE library
            SET status = ?
            WHERE user_id = ?
            AND tmdb_id = ?
            AND media_type = ?
        """, (status, user_id, tmdb_id, media_type))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


def set_library_favourite(user_id, tmdb_id, media_type, is_favourite):
    """Mark an existing library title as favourite or remove that designation."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if not isinstance(is_favourite, bool):
        raise ValueError("is_favourite must be True or False.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE library
            SET is_favourite = ?
            WHERE user_id = ?
            AND tmdb_id = ?
            AND media_type = ?
        """, (
            int(is_favourite),
            user_id,
            tmdb_id,
            media_type
        ))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


def remove_from_library(user_id, tmdb_id, media_type):
    """Remove a movie or TV show from a user's library."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM library
            WHERE user_id = ?
            AND tmdb_id = ?
            AND media_type = ?
        """, (user_id, tmdb_id, media_type))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()

        
# ==========================================
# VIEWING PROGRESS OPERATIONS
# ==========================================

def update_viewing_progress(
    user_id,
    tmdb_id,
    current_season,
    current_episode
):
    """
    Update the viewing progress of a TV show
    already present in the user's library.
    """

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if not isinstance(current_season, int) or isinstance(current_season, bool) or current_season < 1:
        raise ValueError("current_season must be a positive integer.")

    if not isinstance(current_episode, int) or isinstance(current_episode, bool) or current_episode < 1:
        raise ValueError("current_episode must be a positive integer.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE library
            SET current_season = ?,
                current_episode = ?
            WHERE user_id = ?
            AND tmdb_id = ?
            AND media_type = 'tv'
        """, (
            current_season,
            current_episode,
            user_id,
            tmdb_id
        ))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ==========================================
# VIEWING HISTORY OPERATIONS
# ==========================================

def add_viewing_history(
    user_id,
    tmdb_id,
    media_type,
    rating=None
):
    """
    Record a watched movie or TV show.
    """

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in ("movie", "tv"):
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if rating is not None:
        if (
            not isinstance(rating, (int, float))
            or isinstance(rating, bool)
            or not 0 <= rating <= 10
        ):
            raise ValueError("Rating must be between 0 and 10.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO viewing_history (
                user_id,
                tmdb_id,
                media_type,
                rating
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            tmdb_id,
            media_type,
            rating
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_viewing_history(user_id, media_type=None, limit=20):
    """
    Retrieve a user's viewing history.
    Optionally filter by media type.
    """

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if media_type is not None and media_type not in ("movie", "tv"):
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                tmdb_id,
                media_type,
                watched_at,
                rating
            FROM viewing_history
            WHERE user_id = ?
        """

        parameters = [user_id]

        if media_type is not None:
            query += " AND media_type = ?"
            parameters.append(media_type)

        query += " ORDER BY watched_at DESC LIMIT ?"
        parameters.append(limit)

        cursor.execute(query, parameters)

        results = cursor.fetchall()

        return [
            {
                "tmdb_id": row[0],
                "media_type": row[1],
                "watched_at": row[2],
                "rating": row[3]
            }
            for row in results
        ]

    finally:
        connection.close()  
        
        
        
# ==========================================
# RECOMMENDATION FEEDBACK OPERATIONS
# ==========================================

VALID_RECOMMENDATION_FEEDBACK = (
    "liked",
    "disliked",
    "not_interested"
)


def save_recommendation_feedback(
    user_id,
    tmdb_id,
    media_type,
    feedback
):
    """Save or update a user's feedback on a recommendation."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    if feedback not in VALID_RECOMMENDATION_FEEDBACK:
        raise ValueError("Invalid recommendation feedback.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO recommendation_feedback (
                user_id,
                tmdb_id,
                media_type,
                feedback
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(user_id, tmdb_id, media_type)
            DO UPDATE SET
                feedback = excluded.feedback,
                created_at = CURRENT_TIMESTAMP
        """, (
            user_id,
            tmdb_id,
            media_type,
            feedback
        ))

        connection.commit()

        return True

    finally:
        connection.close()              
        
        
def get_recommendation_feedback(user_id, feedback_type=None):
    """Retrieve a user's recommendation feedback."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if (
        feedback_type is not None
        and feedback_type not in VALID_RECOMMENDATION_FEEDBACK
    ):
        raise ValueError("Invalid feedback type.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                tmdb_id,
                media_type,
                feedback,
                created_at
            FROM recommendation_feedback
            WHERE user_id = ?
        """

        parameters = [user_id]

        if feedback_type is not None:
            query += " AND feedback = ?"
            parameters.append(feedback_type)

        query += " ORDER BY created_at DESC"

        cursor.execute(query, parameters)

        results = cursor.fetchall()

        return [
            {
                "tmdb_id": row[0],
                "media_type": row[1],
                "feedback": row[2],
                "created_at": row[3]
            }
            for row in results
        ]

    finally:
        connection.close()     
        
def remove_recommendation_feedback(user_id, tmdb_id, media_type):
    """Remove a user's feedback for a specific title."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("user_id must be a positive integer.")

    if not isinstance(tmdb_id, int) or isinstance(tmdb_id, bool) or tmdb_id <= 0:
        raise ValueError("tmdb_id must be a positive integer.")

    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError("media_type must be 'movie' or 'tv'.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM recommendation_feedback
            WHERE user_id = ?
            AND tmdb_id = ?
            AND media_type = ?
        """, (user_id, tmdb_id, media_type))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()           
        
        
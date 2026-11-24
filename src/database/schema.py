
from src.database.connection import get_connection


def create_tables():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # 1. Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                language TEXT DEFAULT 'English',
                min_rating REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,
                CHECK (min_rating >= 0 AND min_rating <= 10)
            )
        """)

        # 3. Preference genres table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preference_genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                genre TEXT NOT NULL,
                preference_type TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,
                CHECK (preference_type IN ('liked', 'disliked')),
                UNIQUE (user_id, genre, preference_type)
            )
        """)

        # 4. Library table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tmdb_id INTEGER NOT NULL,
                media_type TEXT NOT NULL,
                status TEXT NOT NULL,
                is_favourite INTEGER NOT NULL DEFAULT 0,
                current_season INTEGER,
                current_episode INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,
                CHECK (media_type IN ('movie', 'tv')),
                CHECK (
                    status IN (
                        'watchlist',
                        'watching',
                        'completed',
                        'dropped'
                    )
                ),
                CHECK (is_favourite IN (0, 1)),
                CHECK (
                    current_season IS NULL OR current_season >= 1
                ),
                CHECK (
                    current_episode IS NULL OR current_episode >= 1
                ),
                UNIQUE (user_id, tmdb_id, media_type)
            )
        """)

        # 5. Viewing history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viewing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tmdb_id INTEGER NOT NULL,
                media_type TEXT NOT NULL,
                watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rating REAL,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,
                CHECK (media_type IN ('movie', 'tv')),
                CHECK (rating IS NULL OR (rating >= 0 AND rating <= 10))
            )
        """)
                # 6. Recommendation feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tmdb_id INTEGER NOT NULL,
                media_type TEXT NOT NULL,
                feedback TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,

                CHECK (media_type IN ('movie', 'tv')),

                CHECK (
                    feedback IN (
                        'liked',
                        'disliked',
                        'not_interested'
                    )
                ),

                UNIQUE (user_id, tmdb_id, media_type)
            )
        """)

        # Migrate existing library tables.
        columns = {
            row[1]
            for row in cursor.execute(
                "PRAGMA table_info(library)"
            ).fetchall()
        }

        if "is_favourite" not in columns:

            cursor.execute("""
                CREATE TABLE library_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    tmdb_id INTEGER NOT NULL,
                    media_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    is_favourite INTEGER NOT NULL DEFAULT 0,
                    current_season INTEGER,
                    current_episode INTEGER,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE,
                    CHECK (media_type IN ('movie', 'tv')),
                    CHECK (
                        status IN (
                            'watchlist',
                            'watching',
                            'completed',
                            'dropped'
                        )
                    ),
                    CHECK (is_favourite IN (0, 1)),
                    CHECK (
                        current_season IS NULL OR current_season >= 1
                    ),
                    CHECK (
                        current_episode IS NULL OR current_episode >= 1
                    ),
                    UNIQUE (user_id, tmdb_id, media_type)
                )
            """)

            cursor.execute("""
                INSERT INTO library_new (
                    id,
                    user_id,
                    tmdb_id,
                    media_type,
                    status,
                    is_favourite,
                    current_season,
                    current_episode,
                    added_at
                )
                SELECT
                    id,
                    user_id,
                    tmdb_id,
                    media_type,
                    CASE
                        WHEN status = 'favourite' THEN 'watchlist'
                        ELSE status
                    END,
                    CASE
                        WHEN status = 'favourite' THEN 1
                        ELSE 0
                    END,
                    current_season,
                    current_episode,
                    added_at
                FROM library
            """)

            cursor.execute("DROP TABLE library")

            cursor.execute("""
                ALTER TABLE library_new
                RENAME TO library
            """)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

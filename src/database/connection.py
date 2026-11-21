import sqlite3
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database directory and file
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "talking_tomatoes.db"


def get_connection():

    # Create database directory if it doesn't exist
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Establish database connection
    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
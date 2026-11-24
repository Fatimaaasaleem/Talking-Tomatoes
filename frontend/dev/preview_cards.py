"""Standalone preview of the card component. NOT part of the app.

Every card below is synthetic test data for checking layout and edge cases.
The real app never imports this file.

Run from the project root:
    python -m streamlit run frontend/dev/preview_cards.py
"""

import sys
from pathlib import Path

# Make `ui.cards` importable (this script lives in frontend/dev/).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from ui.cards import MediaCard, render_cards

st.set_page_config(page_title="Card preview", page_icon="🍅", layout="wide")

st.title("Card preview")
st.caption("Synthetic data for layout testing only.")

# Paste a real `poster_path` from one of your TMDB results (for example
# "/abc123.jpg") to see a real poster in the cards that use it.
SAMPLE_POSTER_PATH = ""

LONG_OVERVIEW = (
    "This is a deliberately long description used to check truncation. " * 8
)

st.subheader("1. Typical cards (movie and series)")
render_cards([
    MediaCard("movie", "Sample Movie", "2024-05-01", 8.8,
              "A short, ordinary description of a sample movie.",
              SAMPLE_POSTER_PATH or None, 1),
    MediaCard("tv", "Sample Series", "2023-09-15", 8.5,
              "A short, ordinary description of a sample series.",
              SAMPLE_POSTER_PATH or None, 2),
    MediaCard("movie", "Another Movie", "2021-01-10", 7.2,
              "Another short description.", SAMPLE_POSTER_PATH or None, 3),
])

st.subheader("2. Everything missing")
render_cards([MediaCard()])

st.subheader("3. Poster that fails to load (placeholder should show)")
render_cards([
    MediaCard("movie", "Broken Poster Movie", "2020-02-02", 6.9,
              "The poster path does not exist.",
              "/this-poster-does-not-exist.jpg", 4),
    MediaCard("tv", "Rejected Poster URL", "2020", 7.0,
              "Non-http(s) poster values are ignored.",
              "javascript:alert(1)", 5),
])

st.subheader("4. Long overview and long title")
render_cards([
    MediaCard("movie", "A Very Long Title That Keeps Going And Going To Test Wrapping",
              "2019-06-06", 7.7, LONG_OVERVIEW, None, 6),
])

st.subheader("5. Special characters")
render_cards([
    MediaCard("movie", '<b>Bold</b> & "Quotes" $5 $10', "2018-03-03", 5.5,
              "<script>alert('x')</script> costs $5 & $10 *not italic* _nor this_",
              None, 7),
])

st.subheader("6. Dates and ratings in unusual forms")
render_cards([
    MediaCard("movie", "Year as int", 2022, 8.0, None, None, 8),
    MediaCard("tv", "Empty date, zero rating", "", 0, "TMDB uses 0 for unrated.", None, 9),
    MediaCard(None, "Unknown type", "not-a-date", "7.46", "No badge expected.", None, 10),
])

st.subheader("7. Actions hook (buttons do nothing here)")
render_cards(
    [MediaCard("movie", "Action Demo", "2024", 8.1, "Buttons appear under cards.", None, 11),
     MediaCard("tv", "Action Demo 2", "2024", 8.2, "Keys use the card index.", None, 12)],
    per_row=2,
    actions=lambda card, index: st.button("Sample action", key=f"preview-action-{index}"),
)
"""Reusable movie / TV cards for Streamlit.

This module is deliberately independent of the backend: it imports only
Streamlit and the standard library, and it renders whatever MediaCard
objects it is given. Turning backend results into MediaCard objects is the
job of the adapter layer, not this file.

    cards = [MediaCard(media_type="movie", title="...", poster="/abc.jpg")]
    render_cards(cards, per_row=3)

An optional `actions` callback is called under each card so buttons (add to
watchlist, feedback, ...) can be added later without changing this module:

    render_cards(cards, actions=lambda card, index: st.button("...", key=f"a{index}"))
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Union

import streamlit as st

# TMDB's public image host. Backend poster values are usually relative paths
# such as "/abc123.jpg"; full http(s) URLs are also accepted and used as-is.
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w342"

OVERVIEW_LIMIT = 180


@dataclass(frozen=True)
class MediaCard:
    """Display data for one movie or TV show. Every field may be missing."""

    media_type: Optional[str] = None        # "movie" | "tv" | None
    title: Optional[str] = None
    release_date: Union[str, int, None] = None   # "2024-05-01", "2024" or 2024
    rating: Union[float, int, str, None] = None  # TMDB audience rating, 0-10
    overview: Optional[str] = None
    poster: Optional[str] = None            # "/abc.jpg" or full http(s) URL
    tmdb_id: Optional[int] = None           # for stable widget keys by callers


CardActions = Callable[[MediaCard, int], None]


# ---------------------------------------------------------------------------
# Pure helpers (no Streamlit calls) so they are easy to test.
# ---------------------------------------------------------------------------

def clean_text(value) -> Optional[str]:
    """Collapse whitespace; return None for anything empty or non-text."""
    if not isinstance(value, str):
        return None
    text = " ".join(value.split())
    return text or None


def poster_url(poster) -> Optional[str]:
    """Return a safe image URL, or None if there is no usable poster."""
    text = clean_text(poster)
    if text is None:
        return None
    lowered = text.lower()
    if lowered.startswith(("https://", "http://")):
        return text
    if text.startswith("/"):
        return TMDB_IMAGE_BASE + text
    return None


def format_year(value) -> Optional[str]:
    """Extract a four-digit year from '2024-05-01', '2024' or 2024."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return str(value) if 1000 <= value <= 9999 else None
    text = clean_text(value)
    if text is None:
        return None
    match = re.match(r"^(\d{4})(?:\D|$)", text)
    return match.group(1) if match else None


def format_rating(value) -> Optional[str]:
    """One-decimal rating, or None. TMDB uses 0 for 'not rated yet'."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number or not 0 < number <= 10:
        return None
    return f"{number:.1f}"


def truncate(text: str, limit: int = OVERVIEW_LIMIT) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.-")
    return (cut or text[:limit]) + "…"


def normalise_media_type(value) -> Optional[str]:
    if isinstance(value, str) and value.strip().lower() in ("movie", "tv"):
        return value.strip().lower()
    return None


def _esc(text: str) -> str:
    # "$" is escaped so Streamlit's markdown never treats it as math.
    return html.escape(text, quote=True).replace("$", "&#36;")


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

STYLES = """<style>
.tt-poster{position:relative;aspect-ratio:2/3;border-radius:14px;overflow:hidden;border:1px solid rgba(128,128,128,.35);background:linear-gradient(160deg,#2c2c31,#16161a);}
.tt-ph{position:absolute;inset:0;display:grid;place-items:center;font-size:2.4rem;opacity:.45;}
.tt-poster img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.tt-badge{position:absolute;top:10px;left:10px;padding:.15rem .5rem;border-radius:6px;font-size:.62rem;font-weight:700;letter-spacing:.08em;color:#fff;background:rgba(20,20,22,.82);}
.tt-badge.tv{background:rgba(240,82,63,.92);}
.tt-rate{position:absolute;bottom:10px;left:10px;padding:.15rem .5rem;border-radius:6px;font-size:.75rem;font-weight:600;color:#fff;background:rgba(20,20,22,.82);}
.tt-rate i{color:#f5b73b;font-style:normal;}
.tt-rate.none{font-weight:500;color:#c9c5c2;}
.tt-title{font-weight:600;font-size:.95rem;margin-top:.6rem;line-height:1.25;color:inherit;}
.tt-year{font-size:.75rem;opacity:.65;margin-top:.1rem;}
.tt-over{font-size:.8rem;opacity:.85;margin-top:.4rem;line-height:1.4;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;}
.tt-over.none{font-style:italic;opacity:.55;}
</style>"""


def build_card_html(card: MediaCard) -> str:
    """Return the HTML for one card as a single line (no blank lines).

    A placeholder always sits underneath the poster image. If the image is
    missing or fails to load, the placeholder shows through.
    """
    title = clean_text(card.title) or "Untitled"
    media_type = normalise_media_type(card.media_type)
    year = format_year(card.release_date)
    rating = format_rating(card.rating)
    overview = clean_text(card.overview)
    image = poster_url(card.poster)

    parts = [
        '<div class="tt-card">',
        f'<div class="tt-poster" role="img" aria-label="'
        f'{_esc("Poster for " + title if image else "No poster available for " + title)}">',
        '<div class="tt-ph">🎬</div>',
    ]

    if image:
        parts.append(f'<img src="{_esc(image)}" alt="" loading="lazy">')

    if media_type == "movie":
        parts.append('<span class="tt-badge movie">MOVIE</span>')
    elif media_type == "tv":
        parts.append('<span class="tt-badge tv">SERIES</span>')

    if rating:
        parts.append(f'<span class="tt-rate"><i>★</i> {rating}</span>')
    else:
        parts.append('<span class="tt-rate none">No rating</span>')

    parts.append("</div>")
    parts.append(f'<div class="tt-title">{_esc(title)}</div>')

    if year:
        parts.append(f'<div class="tt-year">{year}</div>')

    if overview:
        parts.append(
            f'<div class="tt-over" title="{_esc(overview)}">'
            f"{_esc(truncate(overview))}</div>"
        )
    else:
        parts.append('<div class="tt-over none">No description available.</div>')

    parts.append("</div>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Streamlit rendering
# ---------------------------------------------------------------------------

def render_card(card: MediaCard, inject_css: bool = True) -> None:
    """Render a single card. Pass inject_css=False if styles are already on the page."""
    if inject_css:
        st.markdown(STYLES, unsafe_allow_html=True)
    st.markdown(build_card_html(card), unsafe_allow_html=True)


def render_cards(
    cards: Sequence[MediaCard],
    per_row: int = 3,
    actions: Optional[CardActions] = None,
) -> None:
    """Render cards in a grid of `per_row` columns.

    `actions(card, index)` is called inside each card's column, under the
    card, with the card's position in `cards` (use it for unique widget keys).
    """
    if not cards:
        return

    per_row = max(1, min(int(per_row), 6))
    st.markdown(STYLES, unsafe_allow_html=True)

    for start in range(0, len(cards), per_row):
        columns = st.columns(per_row, gap="medium")
        for offset, card in enumerate(cards[start:start + per_row]):
            index = start + offset
            with columns[offset]:
                render_card(card, inject_css=False)
                if actions is not None:
                    actions(card, index)
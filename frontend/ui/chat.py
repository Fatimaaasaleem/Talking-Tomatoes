import streamlit as st

from companion.service import CompanionError
from ui.cards import MediaCard, render_cards


def visible_messages(messages: list[dict]) -> list[tuple[int, dict]]:
    return [
        (index, message)
        for index, message in enumerate(messages)
        if message.get("role") in ("user", "assistant")
        and message.get("content")
    ]


def build_media_cards(results: list[dict]) -> list[MediaCard]:
    cards = []

    for item in results:
        cards.append(
            MediaCard(
                media_type=item.get("media_type", "movie"),
                title=item.get("title") or item.get("name") or "Untitled",
                release_date=(
                    item.get("release_date")
                    or item.get("first_air_date")
                ),
                rating=item.get("rating"),
                overview=item.get("overview"),
                poster=item.get("poster_path"),
                tmdb_id=item.get("id"),
            )
        )

    return cards


def render_history(messages: list[dict]) -> None:
    media_by_message = st.session_state.get(
        "media_results_by_message", {}
    )

    for index, message in visible_messages(messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                results = media_by_message.get(index, [])

                if results:
                    render_cards(build_media_cards(results))


def submit_message(service, prompt: str) -> None:
    current_messages = st.session_state.messages

    updated_messages = current_messages + [
        {"role": "user", "content": prompt}
    ]

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = service.send_message(updated_messages)

            st.markdown(reply.text)

            if reply.media_results:
                render_cards(build_media_cards(reply.media_results))

        st.session_state.messages = reply.messages

        assistant_index = len(reply.messages) - 1

        st.session_state.setdefault(
            "media_results_by_message", {}
        )

        st.session_state.media_results_by_message[
            assistant_index
        ] = reply.media_results

    except CompanionError as error:
        st.error(error.message)
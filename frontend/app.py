"""Talking Tomatoes: Streamlit entry point.

Run from the project root:
    python -m streamlit run frontend/app.py
"""

import streamlit as st

from config import DEV_USER_ID
from companion.service import CompanionError
from companion.local_service import LocalCompanionService
from ui.chat import render_history, submit_message


st.set_page_config(
    page_title="Talking Tomatoes",
    page_icon="🍅",
    layout="centered",
)


@st.cache_resource
def get_service():
    """Create the development companion service."""
    return LocalCompanionService(user_id=DEV_USER_ID)


try:
    service = get_service()

except CompanionError as error:
    st.error(error.message)
    st.stop()


if "messages" not in st.session_state:
    st.session_state.messages = service.new_conversation()


with st.sidebar:
    st.markdown("### 🍅 Talking Tomatoes")
    st.caption(f"Development user: {service.get_username()}")

    if st.button("New conversation", use_container_width=True):
        st.session_state.messages = service.new_conversation()
        st.session_state.media_results_by_message = {}
        st.rerun()


st.title("Talking Tomatoes")
st.caption("Tell me what you're in the mood to watch.")

render_history(st.session_state.messages)

prompt = st.chat_input("Describe what you want to watch…")

if prompt:
    submit_message(service, prompt)
from __future__ import annotations

import streamlit as st


def get_session_state() -> dict:
    if "_state" not in st.session_state:
        st.session_state["_state"] = {}
    return st.session_state["_state"]



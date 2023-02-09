import traceback

import streamlit as st

from todo.ui import todos_ui
from todo.http import fetch_todos
from auth import (
    signup,
    login
)

st.set_page_config("Todo List", "📝", "wide")
st.write("# Todo List App")
if "fetch_todos" not in st.session_state: st.session_state["fetch_todos"] = None


def is_authenticated():
    is_login = True if "access_token" in st.session_state else False
    if not is_login:
        with st.expander("Signup", expanded=True):
            signup()
        with st.expander("Login"):
            login()
    else:
        if st.sidebar.button("Logout"):
            del st.session_state["access_token"]
            del st.session_state["refresh_token"]
            st.experimental_rerun()
    return is_login


def main():
    if not is_authenticated(): return
    access_token = st.session_state["access_token"]
    if st.session_state["fetch_todos"] is None or len(st.session_state["fetch_todos"]) == 0:
        st.session_state["fetch_todos"] = fetch_todos(access_token)
    if st.sidebar.button("Re-Fetch"):
        st.session_state["fetch_todos"] = None
        st.experimental_rerun()
    todos = st.session_state["fetch_todos"]
    todos_ui(todos, access_token)


try:
    main()
except Exception as e:
    traceback.print_exc()
    st.error("Something went wrong")

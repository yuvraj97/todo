from math import ceil

import streamlit as st

from todo.http import update_todos
from todo.http import delete_todos
from todo.http import insert_todos


def todos_ui(todos, access_token):
    with st.expander("Add Note", expanded=True):
        add_todo(access_token)
    todo_update(todos, access_token)


def add_todo(access_token):
    header = st.text_input(
        "Header",
        "Enter Header Here",
        key=f"Header Add"
    )
    description = st.text_area(
        "Description",
        "Enter Description Here",
        key=f"Description Add"
    )
    if st.button("Submit"):
        insert_todos(
            access_token,
            dict(
                header=header,
                description=description
            )
        )
        st.session_state["fetch_todos"] = None
        st.experimental_rerun()


def todo_update(todos, access_token):
    n = len(todos)
    n_columns = 3
    n_rows = ceil(n/n_columns)
    counter = 0
    for row_i in range(n_rows):
        cols = st.columns(3)
        for col_i, col in enumerate(cols):
            if counter >= len(todos): return
            todo = todos[counter]
            counter += 1
            with col.expander(f"Todo {row_i * 3 + col_i + 1}", expanded=True):
                header = st.text_input(
                    "Header",
                    todo["header"],
                    key=f"Header: {row_i}, {col_i}"
                )
                description = st.text_area(
                    "Description",
                    todo["description"],
                    key=f"Description: {row_i}, {col_i}"
                )
                if st.button("Update", key=f"Update: {row_i}, {col_i}"):
                    update_todos(access_token, dict(
                        id=todo["id"],
                        header=header,
                        description=description
                    ))
                    st.session_state["fetch_todos"] = None
                    st.experimental_rerun()
                if st.button("Delete", key=f"Delete: {row_i}, {col_i}"):
                    delete_todos(access_token, dict(id=todo["id"]))
                    st.session_state["fetch_todos"] = None
                    st.experimental_rerun()

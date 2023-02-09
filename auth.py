import streamlit as st
import requests


BASE_URL = "https://o15bg4.deta.dev"


def signup():
    email = st.text_input("email")
    password = st.text_input("Password")
    role = "admin"
    if st.button("Submit"):
        signup_response = requests.post(
            f"{BASE_URL}/auth/signup",
            json={
                "email": email,
                "password": password,
                "role": role,
            }
        ).json()
        if signup_response is True:
            st.success("Created Successfully")
            return True
        else:
            st.error(signup_response["detail"])
    return False


def login():
    email = st.text_input("Email", key="Login_email")
    password = st.text_input("Password", key="Login_password")
    if st.button("Login"):
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        status_code = login_response.status_code
        login_response = login_response.json()
        if status_code == 200:
            refresh_token = login_response["refresh"]
            access_token = login_response["access"]
            st.success("Logged-In Successfully")
            st.session_state["access_token"] = access_token
            st.session_state["refresh_token"] = refresh_token
            st.session_state["email"] = email
            st.experimental_rerun()
        else:
            st.error(login_response["detail"])

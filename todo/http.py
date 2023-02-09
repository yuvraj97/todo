import requests
import json


BASE_URL = "http://127.0.0.1:8000"


def fetch_todos(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"{BASE_URL}/todo/"
    response = requests.request("GET", url, headers=headers).json()
    return response


def update_todos(access_token, payload):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"{BASE_URL}/todo/update"
    response = requests.request("PUT", url, headers=headers, json=payload).json()
    return response


def delete_todos(access_token, payload):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"{BASE_URL}/todo/"
    response = requests.request("DELETE", url, headers=headers, json=payload).json()
    return response


def insert_todos(access_token, payload):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"{BASE_URL}/todo/"
    response = requests.request("PUT", url, headers=headers, json=payload).json()
    return response

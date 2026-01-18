import os
import requests
from requests.exceptions import RequestException

SLACK_API_URL = os.getenv("SLACK_API_URL")
SLACK_ADMIN_INVITE_URL = os.getenv("SLACK_ADMIN_INVITE_URL")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")


def fetch_slack_users(token=None):
    headers = {"Authorization": f"Bearer {token or SLACK_TOKEN}"}
    try:
        response = requests.get(SLACK_API_URL, headers=headers, verify=False)
        return response.json()
    except requests.RequestException as error:
        return {"error": str(error)}


def send_slack_invite(payload, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            SLACK_ADMIN_INVITE_URL,
            headers=headers,
            json=payload,
            timeout=10,
            verify=False,
        )
        return response.json()
    except RequestException as error:
        return {"error": str(error)}

import json
import logging
import os
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
    )

SLACK_ADMIN_INVITE_URL = os.getenv("SLACK_ADMIN_INVITE_URL")
SLACK_API_URL = os.getenv("SLACK_API_URL")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_USERS_FILE = os.getenv("SLACK_USERS_FILE")


def add_slack_user(email: str, full_name: str, user_token: str):
    payload = build_slack_invite_payload(email, full_name)
    data = send_slack_invite(payload, user_token)

    if data.get("ok"):
        logging.info("User invitation sent successfully: %s", email)
    else:
        logging.error(
            "Failed to invite user %s | error=%s | response=%s",
            email,
            data.get("error"),
            data
        )


def build_slack_invite_payload(email, full_name):
    return {
        "email": email,
        "real_name": full_name,
        "resend": False
    }


def fetch_slack_users(token=None):
    headers = {"Authorization": f"Bearer {token or SLACK_TOKEN}"}
    response = requests.get(SLACK_API_URL, headers=headers, verify=False)
    return response.json()


def get_slack_users(token=None):
    data = fetch_slack_users(token)
    return parse_slack_users(data)


def parse_slack_users(data):
    users_list = []
    for user in data.get("members", []):
        if not user.get("is_bot", False):
            users_list.append({
                "id": user["id"],
                "username": user["name"],
                "full_name": user.get("real_name", ""),
                "is_bot": user.get("is_bot", False)
            })
    return users_list


def save_users_to_json(users, filename=None):
    filename = filename or SLACK_USERS_FILE
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
        logging.info(f"Saved {len(users)} users to {filename}")
    except Exception as error:
        logging.error(f"Failed to save users to JSON: {error}")


def send_slack_invite(payload, user_token):
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        SLACK_ADMIN_INVITE_URL,
        headers=headers,
        json=payload,
        timeout=10,
        verify=False
    )
    return response.json()


if __name__ == "__main__":
    users = get_slack_users()
    save_users_to_json(users)

    add_slack_user(
        email="user@example.com",
        full_name="New User",
        user_token=SLACK_TOKEN
    )

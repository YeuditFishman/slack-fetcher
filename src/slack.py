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


def get_slack_users(token=None):
    headers = {"Authorization": f"Bearer {token or SLACK_TOKEN}"}
    response = requests.get(SLACK_API_URL, headers=headers, verify=False)
    data = response.json()
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


def add_slack_user(email: str, full_name: str, user_token: str):
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": email,
        "real_name": full_name,
        "resend": False
    }

    response = requests.post(
        SLACK_ADMIN_INVITE_URL,
        headers=headers,
        json=payload,
        timeout=10,
        verify=False
    )

    data = response.json()

    if response.status_code == 200 and data.get("ok"):
        logging.info("User invitation sent successfully: %s", email)
    else:
        logging.error(
            "Failed to invite user %s | error=%s | response=%s",
            email,
            data.get("error"),
            data
        )


if __name__ == "__main__":
    users = get_slack_users()
    save_users_to_json(users)

    add_slack_user(
        email="user@example.com",
        full_name="New User",
        user_token=SLACK_TOKEN
    )

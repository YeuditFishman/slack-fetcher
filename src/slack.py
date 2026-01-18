import logging
import os
from src.slack_api import fetch_slack_users, send_slack_invite
from src.slack_users import (
    parse_slack_users,
    save_users_to_json,
    build_slack_invite_payload,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
    )

SLACK_TOKEN = os.getenv("SLACK_TOKEN")


def get_slack_users(token=None):
    data = fetch_slack_users(token)
    return parse_slack_users(data)


def add_slack_user(email: str, full_name: str, user_token: str):
    payload = build_slack_invite_payload(email, full_name)
    response = send_slack_invite(payload, user_token)

    if response.get("ok"):
        logging.info("User invitation sent successfully: %s", email)
    else:
        logging.error(
            "Failed to invite user %s | error=%s | response=%s",
            email,
            response.get("error"),
            response,
        )


if __name__ == "__main__":
    users = get_slack_users()
    save_users_to_json(users)

    add_slack_user(
        email="user@example.com",
        full_name="New User",
        user_token=SLACK_TOKEN
    )

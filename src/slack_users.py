import json
import logging
import os

SLACK_USERS_FILE = os.getenv("SLACK_USERS_FILE")


def parse_slack_users(data):
    users = []
    for user in data.get("members", []):
        if not user.get("is_bot", False):
            users.append({
                "id": user["id"],
                "username": user["name"],
                "full_name": user.get("real_name", ""),
                "is_bot": user.get("is_bot", False),
            })
    return users


def save_users_to_json(users, filename=None):
    filename = filename or SLACK_USERS_FILE
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)
    logging.info("Saved %s users to %s", len(users), filename)


def build_slack_invite_payload(email, full_name):
    return {
        "email": email,
        "real_name": full_name,
        "resend": False,
    }

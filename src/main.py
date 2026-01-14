import json
import logging
import os
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
    )

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_API_URL = os.getenv("SLACK_API_URL")
SLACK_USERS_FILE = os.getenv("SLACK_USERS_FILE")

def get_slack_users():
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    response = requests.get(SLACK_API_URL, headers=headers, verify=False)
    data = response.json()
    users_list = []
    for user in data.get("members", []):
        users_list.append({
            "id": user["id"],
            "username": user["name"],
            "full_name": user.get("real_name", ""),
            "is_bot": user.get("is_bot", False)
        })
    return users_list

def save_users_to_json(users):
    try:
        with open(SLACK_USERS_FILE, "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
        logging.info(f"Saved {len(users)} users to {SLACK_USERS_FILE}")
    except Exception as error:
        logging.error(f"Failed to save users to JSON: {error}")

if __name__ == "__main__":
    users = get_slack_users()
    save_users_to_json(users)

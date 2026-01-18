import json
import os
from src.slack_users import (
    parse_slack_users,
    save_users_to_json,
    build_slack_invite_payload,
)
import unittest


class TestSlackUsers(unittest.TestCase):

    def test_build_slack_invite_payload(self):
        payload = build_slack_invite_payload("user@example.com", "New User")
        self.assertEqual(payload["email"], "user@example.com")
        self.assertEqual(payload["real_name"], "New User")
        self.assertFalse(payload["resend"])

    def test_parse_slack_users_filters_bots(self):
        data = {
            "members": [
                {
                    "id": "U123",
                    "name": "rikif",
                    "real_name": "Riki F",
                    "is_bot": False
                },
                {
                    "id": "U124",
                    "name": "botuser",
                    "real_name": "Bot",
                    "is_bot": True
                }
            ]
        }
        users = parse_slack_users(data)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "rikif")

    def test_save_users_to_json(self):
        users = [
            {
                "id": "U123",
                "username": "rikif",
                "full_name": "Riki F",
                "is_bot": False
            }
        ]
        filename = "test_users.json"
        save_users_to_json(users, filename)
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data, users)
        os.remove(filename)

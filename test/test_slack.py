import json
import os
from src.main import get_slack_users, save_users_to_json
import unittest
from unittest.mock import patch


class TestSlackUsers(unittest.TestCase):

    @patch('src.main.requests.get')
    @patch.dict(os.environ, {
        "SLACK_TOKEN": "fake-token",
        "SLACK_API_URL": "https://fake-url"
        })
    def test_get_slack_users(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "ok": True,
            "members": [
                {
                    "id": "U123",
                    "name": "rikif",
                    "real_name": "Riki F",
                    "is_bot": False
                },
                {
                    "id": "U124",
                    "name": "yehuditfi",
                    "real_name": "Yehudit F",
                    "is_bot": False
                }
            ]
        }

        users = get_slack_users()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        user = users[0]
        self.assertIn("id", user)
        self.assertIn("username", user)
        self.assertIn("full_name", user)
        self.assertIn("is_bot", user)

    @patch.dict(os.environ, {
        "SLACK_USERS_FILE": "test_users.json"
        })
    def test_save_users_to_json(self):
        users = [
            {
                "id": "U123",
                "username": "rikif",
                "full_name": "Riki F",
                "is_bot": False
            }
        ]
        save_users_to_json(users)
        self.assertTrue(os.path.exists("test_users.json"))
        with open("test_users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data, users)
        os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()

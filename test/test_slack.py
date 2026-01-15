import json
import os
from src.slack import (
    add_slack_user,
    get_slack_users,
    save_users_to_json,
    fetch_slack_users,
    parse_slack_users,
    build_slack_invite_payload,
    send_slack_invite
)
import unittest
from unittest.mock import patch, MagicMock


class TestSlackUsers(unittest.TestCase):

    @patch('src.slack.requests.get')
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

        data = fetch_slack_users("fake-token")
        self.assertIn("members", data)

    def test_parse_slack_users(self):
        raw_data = {
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
        users = parse_slack_users(raw_data)
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

    def test_get_slack_users_combined(self):
        with patch('src.slack.fetch_slack_users') as mock_fetch:
            mock_fetch.return_value = {
                "members": [
                    {
                        "id": "U123",
                        "name": "rikif",
                        "real_name": "Riki F",
                        "is_bot": False
                    }
                ]
            }
            users = get_slack_users("fake-token")
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0]["username"], "rikif")


class TestAddSlackUser(unittest.TestCase):

    def test_build_slack_invite_payload(self):
        payload = build_slack_invite_payload("user@example.com", "New User")
        self.assertEqual(payload["email"], "user@example.com")
        self.assertEqual(payload["real_name"], "New User")
        self.assertFalse(payload["resend"])

    @patch('src.slack.requests.post')
    def test_send_slack_invite_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        payload = {
            "email": "user@example.com",
            "real_name": "New User",
            "resend": False
            }
        data = send_slack_invite(payload, "fake-token")
        self.assertTrue(data["ok"])
        mock_post.assert_called_once()

    @patch('src.slack.requests.post')
    def test_add_slack_user_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        add_slack_user(
            email="user@example.com",
            full_name="New User",
            user_token="fake-token"
        )

        mock_post.assert_called_once()

    @patch('src.slack.requests.post')
    def test_add_slack_user_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ok": False,
            "error": "not_allowed"
            }
        mock_post.return_value = mock_response

        add_slack_user("user@example.com", "New User", "fake-token")
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()

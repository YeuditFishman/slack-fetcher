import json
import os
from src.slack import add_slack_user, get_slack_users, save_users_to_json
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

        users = get_slack_users("fake-token")
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        user = users[0]
        self.assertIn("id", user)
        self.assertIn("username", user)
        self.assertIn("full_name", user)
        self.assertIn("is_bot", user)

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


class TestAddSlackUser(unittest.TestCase):

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
        args, kwargs = mock_post.call_args
        self.assertIn("json", kwargs)
        self.assertEqual(kwargs["json"]["email"], "user@example.com")
        self.assertEqual(kwargs["json"]["real_name"], "New User")

        @patch('src.slack.requests.post')
        def test_add_slack_user_failure(self, mock_post):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "ok": False,
                "error": "not_allowed"
                }
            mock_post.return_value = mock_response

            add_slack_user(
                email="user@example.com",
                full_name="New User",
                user_token="fake-token"
            )

            mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()

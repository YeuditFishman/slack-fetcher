from src.slack import add_slack_user, get_slack_users
import unittest
from unittest.mock import patch


class TestSlackFlow(unittest.TestCase):

    @patch('src.slack.send_slack_invite')
    def test_add_slack_user(self, mock_send):
        mock_send.return_value = {"ok": True}

        add_slack_user(
            email="user@example.com",
            full_name="New User",
            user_token="fake-token"
        )

        mock_send.assert_called_once()

    @patch('src.slack.fetch_slack_users')
    def test_get_slack_users(self, mock_fetch):
        mock_fetch.return_value = {
            "ok": True,
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


if __name__ == "__main__":
    unittest.main()

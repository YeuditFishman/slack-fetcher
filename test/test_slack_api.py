from src.slack_api import fetch_slack_users, send_slack_invite
import unittest
from unittest.mock import patch, MagicMock


class TestSlackAPI(unittest.TestCase):

    @patch("src.slack_api.requests.get")
    def test_fetch_slack_users(self, mock_get):
        mock_get.return_value.json.return_value = {
            "members": [{"id": "U1", "name": "user", "is_bot": False}]
        }

        data = fetch_slack_users("fake-token")
        self.assertIn("members", data)

    @patch("src.slack_api.requests.post")
    def test_send_slack_invite_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        payload = {"email": "a@b.com", "real_name": "Test", "resend": False}
        result = send_slack_invite(payload, "fake-token")

        self.assertTrue(result["ok"])

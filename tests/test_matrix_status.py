import unittest
from unittest.mock import patch, MagicMock
from pymonomatrix.MatrixStatus import MatrixStatus, api_url

class TestMatrixStatus(unittest.TestCase):
    def setUp(self):
        # Setup basic MatrixStatus with dummy labels
        input_labels = [f"Input {i}" for i in range(1, 9)]
        output_video_labels = [f"Output Video {i}" for i in range(1, 9)]
        output_audio_labels = [f"Output Audio {i}" for i in range(1, 9)]
        self.matrix_status = MatrixStatus(input_labels, output_video_labels, output_audio_labels)

    @patch('requests.Session.post')
    def test_get_status(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.text = "mocked response text"
        mock_post.return_value = mock_response

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that self.session.post was called with the correct parameters
        req_body = {"foo": "bar"}
        mock_post.assert_called_once_with(api_url, json=req_body, timeout=10)

        # Check that self.response is correctly set to the response text
        self.assertEqual(self.matrix_status.response, "mocked response text")

    def test_decode_volume_initial_update(self):
        self.matrix_status.response_yaml = {
            "volume2": "100!50!!5000100!50!!5000"
        }
        self.matrix_status.decode_volume()
        expected_volumes = [100, 50, 5, 0, 100, 50, 5, 0]
        self.assertEqual(self.matrix_status.volume, expected_volumes)
        self.assertEqual(self.matrix_status.volume_changed, [True] * 8)

    def test_decode_volume_no_change(self):
        self.matrix_status.volume = [100, 50, 5, 0, 100, 50, 5, 0]
        self.matrix_status.response_yaml = {
            "volume2": "100!50!!5000100!50!!5000"
        }
        self.matrix_status.decode_volume()
        self.assertEqual(self.matrix_status.volume, [100, 50, 5, 0, 100, 50, 5, 0])
        self.assertEqual(self.matrix_status.volume_changed, [False] * 8)

    def test_decode_volume_partial_change(self):
        self.matrix_status.volume = [100, 50, 5, 0, 100, 50, 5, 0]
        # Change index 1 (!50 -> !55) and index 2 (!!5 -> !!8)
        self.matrix_status.response_yaml = {
            "volume2": "100!55!!8000100!50!!5000"
        }
        self.matrix_status.decode_volume()
        self.assertEqual(self.matrix_status.volume, [100, 55, 8, 0, 100, 50, 5, 0])
        expected_changed = [False, True, True, False, False, False, False, False]
        self.assertEqual(self.matrix_status.volume_changed, expected_changed)

    def test_fix_yaml_with_parentheses(self):
        # Arrange
        self.matrix_status.response = "(key: value)"

        # Act
        self.matrix_status.fix_yaml()

        # Assert
        self.assertEqual(self.matrix_status.response_yaml, {"key": "value"})

    def test_fix_yaml_without_parentheses(self):
        # Arrange
        self.matrix_status.response = "key: value"

        # Act
        self.matrix_status.fix_yaml()

        # Assert
        self.assertEqual(self.matrix_status.response_yaml, {"key": "value"})

    @patch('requests.Session.post')
    def test_get_status_request_exception(self, mock_post):
        # Arrange
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Mocked error")

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that self.session.post was called with the correct parameters
        req_body = {"foo": "bar"}
        mock_post.assert_called_once_with(api_url, json=req_body, timeout=10)

        # Check that self.response is correctly set to None
        self.assertIsNone(self.matrix_status.response)

    @patch('requests.Session.post')
    def test_get_status_connection_error(self, mock_post):
        # Arrange
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Mocked connection error")

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that self.response is correctly set to None
        self.assertIsNone(self.matrix_status.response)

    @patch('requests.Session.post')
    def test_get_status_timeout(self, mock_post):
        # Arrange
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Mocked timeout error")

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that self.response is correctly set to None
        self.assertIsNone(self.matrix_status.response)

if __name__ == '__main__':
    unittest.main()

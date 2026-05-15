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

    @patch('pymonomatrix.MatrixStatus.requests.post')
    def test_get_status(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.text = "mocked response text"
        mock_post.return_value = mock_response

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that requests.post was called with the correct parameters
        req_body = {"foo": "bar"}
        mock_post.assert_called_once_with(api_url, json=req_body, timeout=10)

        # Check that self.response is correctly set to the response text
        self.assertEqual(self.matrix_status.response, "mocked response text")

    @patch('pymonomatrix.MatrixStatus.requests.post')
    def test_get_status_request_exception(self, mock_post):
        # Arrange
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Mocked error")

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that requests.post was called with the correct parameters
        req_body = {"foo": "bar"}
        mock_post.assert_called_once_with(api_url, json=req_body, timeout=10)

        # Check that self.response is correctly set to None
        self.assertIsNone(self.matrix_status.response)

    @patch('pymonomatrix.MatrixStatus.requests.post')
    def test_get_status_connection_error(self, mock_post):
        # Arrange
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Mocked connection error")

        # Act
        self.matrix_status.get_status()

        # Assert
        # Check that self.response is correctly set to None
        self.assertIsNone(self.matrix_status.response)

    @patch('pymonomatrix.MatrixStatus.requests.post')
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

import unittest
from unittest.mock import patch, MagicMock
from pymonomatrix.SetMatrix import SetMatrix, api_url

class TestSetMatrix(unittest.TestCase):
    def setUp(self):
        # Setup basic SetMatrix with dummy labels
        input_labels = [f"Input {i}" for i in range(1, 9)]
        output_video_labels = [f"Output Video {i}" for i in range(1, 9)]
        output_audio_labels = [f"Output Audio {i}" for i in range(1, 9)]
        self.set_matrix = SetMatrix(input_labels, output_video_labels, output_audio_labels)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_post_command_success(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        req_body = "CMD=AVOLUME01:50."

        # Act
        result = self.set_matrix.post_command(req_body)

        # Assert
        self.assertTrue(result)
        mock_post.assert_called_once_with(api_url, data=req_body, timeout=10)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_post_command_failure(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        req_body = "CMD=AVOLUME01:50."

        # Act
        result = self.set_matrix.post_command(req_body)

        # Assert
        self.assertFalse(result)
        mock_post.assert_called_once_with(api_url, data=req_body, timeout=10)

if __name__ == '__main__':
    unittest.main()

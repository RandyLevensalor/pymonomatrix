import unittest
from unittest.mock import patch, MagicMock
from pymonomatrix.SetMatrix import SetMatrix, api_url

class TestSetMatrix(unittest.TestCase):
    def setUp(self):
        self.input_labels = ["Input 1", "Input 2", "Input 3", "Input 4", "Input 5", "Input 6", "Input 7", "Input 8"]
        self.output_video_labels = ["Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"]
        self.output_audio_labels = ["Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"]
        self.matrix = SetMatrix(self.input_labels, self.output_video_labels, self.output_audio_labels)

    @patch.object(SetMatrix, 'post_command')
    def test_set_video_output_success(self, mock_post_command):
        # Arrange
        mock_post_command.return_value = True

        # Act
        result = self.matrix.set_video_output("Bar", "Input 3")

        # Assert
        self.assertTrue(result)
        # Bar is index 1 -> output 2. Input 3 is index 2 -> input 3.
        # Expected CMD: CMD=OUT02:03.
        mock_post_command.assert_called_once_with("CMD=OUT02:03.")

    @patch.object(SetMatrix, 'post_command')
    def test_set_video_output_invalid_output(self, mock_post_command):
        # Act
        result = self.matrix.set_video_output("Nonexistent Room", "Input 1")

        # Assert
        self.assertFalse(result)
        mock_post_command.assert_not_called()

    @patch.object(SetMatrix, 'post_command')
    def test_set_video_output_invalid_input(self, mock_post_command):
        # Act
        result = self.matrix.set_video_output("Living Room", "Input 9")

        # Assert
        self.assertFalse(result)
        mock_post_command.assert_not_called()

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_post_command_success(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        req_body = "CMD=AVOLUME01:50."

        # Act
        result = self.matrix.post_command(req_body)

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
        result = self.matrix.post_command(req_body)

        # Assert
        self.assertFalse(result)
        mock_post.assert_called_once_with(api_url, data=req_body, timeout=10)

if __name__ == '__main__':
    unittest.main()

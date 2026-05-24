import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to sys.path to import pymonomatrix
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymonomatrix.SetMatrix import SetMatrix

class TestSetMatrix(unittest.TestCase):
    def setUp(self):
        input_labels = [f"Input {i}" for i in range(1, 9)]
        output_video_labels = [f"Output Video {i}" for i in range(1, 9)]
        output_audio_labels = [f"Output Audio {i}" for i in range(1, 9)]
        self.set_matrix = SetMatrix(input_labels, output_video_labels, output_audio_labels)
        # Mock post_command to prevent actual network calls during tests
        self.set_matrix.post_command = MagicMock(return_value=True)

        self.input_labels = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
        self.output_video_labels = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]
        self.output_audio_labels = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]
        self.set_matrix2 = SetMatrix(self.input_labels, self.output_video_labels, self.output_audio_labels)


    def test_set_volume_invalid_output(self):
        # Act
        result = self.set_matrix.set_volume("Invalid Output", 50)

        # Assert
        self.assertFalse(result)
        self.set_matrix.post_command.assert_not_called()

    def test_set_volume_invalid_volume(self):
        # Act
        result = self.set_matrix.set_volume("Output Audio 1", "INVALID")

        # Assert
        self.assertFalse(result)
        self.set_matrix.post_command.assert_not_called()

    def test_set_volume_valid_special_volume(self):
        special_volumes = ["V+", "V-", "MU", "UM"]
        for vol in special_volumes:
            with self.subTest(volume=vol):
                self.set_matrix.post_command.reset_mock()

                # Act
                result = self.set_matrix.set_volume("Output Audio 1", vol)

                # Assert
                self.assertTrue(result)
                # Output index is output_audio_labels.index("Output Audio 1") + 1 = 0 + 1 = 1
                expected_req_body = f"CMD=AVOLUME01:{vol}."
                self.set_matrix.post_command.assert_called_once_with(expected_req_body)

    def test_set_volume_valid_int_volume_under_10(self):
        # Act
        result = self.set_matrix.set_volume("Output Audio 2", 5)

        # Assert
        self.assertTrue(result)
        # Output index is 2, volume 5 is padded to "05"
        expected_req_body = "CMD=AVOLUME02:05."
        self.set_matrix.post_command.assert_called_once_with(expected_req_body)

    def test_set_volume_valid_int_volume_10_and_over(self):
        # Act
        result = self.set_matrix.set_volume("Output Audio 3", 50)

        # Assert
        self.assertTrue(result)
        # Output index is 3
        expected_req_body = "CMD=AVOLUME03:50."
        self.set_matrix.post_command.assert_called_once_with(expected_req_body)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_post_command_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = self.set_matrix2.post_command("CMD=TEST.")

        self.assertTrue(result)
        mock_post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=TEST.", timeout=10)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_post_command_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = self.set_matrix2.post_command("CMD=TEST.")

        self.assertFalse(result)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_set_volume_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Output "A1" is index 0 -> index 1
        # Volume 20 -> "20"
        result = self.set_matrix2.set_volume("A1", 20)

        self.assertTrue(result)
        mock_post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=AVOLUME01:20.", timeout=10)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_set_video_output_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Output "V1" is index 0 -> index 1
        # Input "I1" is index 0 -> index 1
        result = self.set_matrix2.set_video_output("V1", "I1")

        self.assertTrue(result)
        mock_post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=OUT01:01.", timeout=10)

    @patch('pymonomatrix.SetMatrix.requests.post')
    def test_set_audio_output_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Output "A1" is index 0 -> index 1
        # Input "I1" is index 0 -> index 1
        result = self.set_matrix2.set_audio_output("A1", "I1")

        self.assertTrue(result)
        mock_post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=AUDIO01:01.", timeout=10)

if __name__ == '__main__':
    unittest.main()

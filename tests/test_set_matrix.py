import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock requests before importing SetMatrix
mock_requests = MagicMock()
sys.modules['requests'] = mock_requests

# Add the project root to sys.path to import pymonomatrix
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymonomatrix.SetMatrix import SetMatrix

class TestSetMatrix(unittest.TestCase):
    def setUp(self):
        self.input_labels = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
        self.output_video_labels = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]
        self.output_audio_labels = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"]
        self.set_matrix = SetMatrix(self.input_labels, self.output_video_labels, self.output_audio_labels)

    def test_post_command_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        result = self.set_matrix.post_command("CMD=TEST.")

        self.assertTrue(result)
        mock_requests.post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=TEST.", timeout=10)

    def test_post_command_failure(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests.post.return_value = mock_response

        result = self.set_matrix.post_command("CMD=TEST.")

        self.assertFalse(result)

    def test_set_volume_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        # Output "A1" is index 0 -> index 1
        # Volume 20 -> "20"
        result = self.set_matrix.set_volume("A1", 20)

        self.assertTrue(result)
        mock_requests.post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=AVOLUME01:20.", timeout=10)

    def test_set_video_output_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        # Output "V1" is index 0 -> index 1
        # Input "I1" is index 0 -> index 1
        result = self.set_matrix.set_video_output("V1", "I1")

        self.assertTrue(result)
        mock_requests.post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=OUT01:01.", timeout=10)

    def test_set_audio_output_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        # Output "A1" is index 0 -> index 1
        # Input "I1" is index 0 -> index 1
        result = self.set_matrix.set_audio_output("A1", "I1")

        self.assertTrue(result)
        mock_requests.post.assert_called_with("http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi", data="CMD=AUDIO01:01.", timeout=10)

if __name__ == '__main__':
    unittest.main()

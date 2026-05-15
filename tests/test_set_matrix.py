import unittest
from unittest.mock import MagicMock
from pymonomatrix.SetMatrix import SetMatrix

class TestSetMatrix(unittest.TestCase):
    def setUp(self):
        input_labels = [f"Input {i}" for i in range(1, 9)]
        output_video_labels = [f"Output Video {i}" for i in range(1, 9)]
        output_audio_labels = [f"Output Audio {i}" for i in range(1, 9)]
        self.set_matrix = SetMatrix(input_labels, output_video_labels, output_audio_labels)
        # Mock post_command to prevent actual network calls during tests
        self.set_matrix.post_command = MagicMock(return_value=True)

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

if __name__ == '__main__':
    unittest.main()

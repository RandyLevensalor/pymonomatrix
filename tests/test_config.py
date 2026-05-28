import unittest
from unittest.mock import patch, mock_open
import yaml
import os
from pymonomatrix.config import load_config, DEFAULT_CONFIG_FILE

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.default_expected_config = {
            "input_labels": ["Input 1", "Input 2", "Input 3", "Input 4", "Input 5", "Input 6", "Input 7", "Input 8"],
            "output_video_labels": ["Output 1", "Output 2", "Output 3", "Output 4", "Output 5", "Output 6", "Output 7", "Output 8"],
            "output_audio_labels": ["Output 1", "Output 2", "Output 3", "Output 4", "Output 5", "Output 6", "Output 7", "Output 8"]
        }

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_load_config_default(self, mock_env_get, mock_path_exists):
        # Arrange
        mock_env_get.return_value = DEFAULT_CONFIG_FILE
        mock_path_exists.return_value = False

        # Act
        config = load_config()

        # Assert
        self.assertEqual(config, self.default_expected_config)
        mock_env_get.assert_called_with("PYMONOMATRIX_CONFIG", DEFAULT_CONFIG_FILE)

    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_load_config_with_env_var(self, mock_env_get, mock_path_exists):
        # Arrange
        fake_path = "/path/to/custom_config.yaml"
        mock_env_get.return_value = fake_path

        # We need os.path.exists to return True only for fake_path
        def fake_exists(path):
            if path == fake_path:
                return True
            return False
        mock_path_exists.side_effect = fake_exists

        custom_yaml = '{"input_labels": ["Custom Input 1", "Custom Input 2"]}'

        expected_config = self.default_expected_config.copy()
        expected_config.update({"input_labels": ["Custom Input 1", "Custom Input 2"]})

        with patch('builtins.open', mock_open(read_data=custom_yaml)):
            # Act
            config = load_config()

        # Assert
        self.assertEqual(config, expected_config)
        mock_env_get.assert_called_with("PYMONOMATRIX_CONFIG", DEFAULT_CONFIG_FILE)

    @patch('logging.error')
    @patch('os.path.exists')
    @patch('os.environ.get')
    def test_load_config_invalid_yaml(self, mock_env_get, mock_path_exists, mock_logging_error):
        # Arrange
        fake_path = "config.yaml"
        mock_env_get.return_value = fake_path

        def fake_exists(path):
            if path == fake_path:
                return True
            return False
        mock_path_exists.side_effect = fake_exists

        invalid_yaml = "unbalanced: [\n"

        with patch('builtins.open', mock_open(read_data=invalid_yaml)):
            # Act
            config = load_config()

        # Assert
        self.assertEqual(config, self.default_expected_config)
        mock_logging_error.assert_called_once()
        self.assertTrue("Error parsing config file" in mock_logging_error.call_args[0][0])

if __name__ == '__main__':
    unittest.main()

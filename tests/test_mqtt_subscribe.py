import unittest
from unittest.mock import MagicMock, patch
import pymonomatrix.mqttSubscribe as mqttSubscribe

class TestMqttSubscribe(unittest.TestCase):
    def setUp(self):
        # Create a mock for the client
        self.mock_client = MagicMock()

        # We need to capture the on_message callback that gets attached to the client
        # so we can call it directly with our mock messages.
        self.on_message_callback = None

        def mock_on_message(client, userdata, msg):
            pass

        def mock_subscribe(topic):
            pass

        self.mock_client.subscribe = mock_subscribe

        self.mock_set_matrix = MagicMock()

        # Set up the subscribe module
        mqttSubscribe.subscribe(self.mock_client, "pymonomatrix/set/", self.mock_set_matrix)

        # Capture the callback
        self.on_message_callback = self.mock_client.on_message

    def test_malformed_topic_no_hyphen(self):
        """Test that a topic without a hyphen doesn't raise IndexError."""
        # Create a mock message with a topic that will not split into 2 parts
        mock_msg = MagicMock()
        mock_msg.topic = "pymonomatrix/set/invalidtopic"
        mock_msg.payload = b"test_payload"

        # This should not raise an exception
        try:
            self.on_message_callback(self.mock_client, None, mock_msg)
        except IndexError:
            self.fail("IndexError raised for malformed topic!")

    def test_malformed_topic_no_prefix(self):
        """Test that a topic completely missing the prefix doesn't raise IndexError."""
        mock_msg = MagicMock()
        mock_msg.topic = "completely/different/topic"
        mock_msg.payload = b"test_payload"

        # This should not raise an exception
        try:
            self.on_message_callback(self.mock_client, None, mock_msg)
        except IndexError:
            self.fail("IndexError raised for malformed topic!")

    def test_valid_topic(self):
        """Test that a valid topic is processed correctly."""
        mock_msg = MagicMock()
        mock_msg.topic = "pymonomatrix/set/1-video_output"
        mock_msg.payload = b"test_payload"

        # Create a mock set_video_output function on the mock_set_matrix
        mock_set_video_output = MagicMock()
        setattr(self.mock_set_matrix, 'set_video_output', mock_set_video_output)

        self.on_message_callback(self.mock_client, None, mock_msg)

        # Verify the function was called with correct index and payload
        mock_set_video_output.assert_called_once_with("1", "test_payload")

    def test_valid_topic_invalid_type(self):
        """Test that a valid topic format but invalid type doesn't raise AttributeError."""
        mock_msg = MagicMock()
        mock_msg.topic = "pymonomatrix/set/1-invalidtype"
        mock_msg.payload = b"test_payload"

        # This should not raise an exception
        try:
            self.on_message_callback(self.mock_client, None, mock_msg)
        except AttributeError:
            self.fail("AttributeError raised for invalid type!")

if __name__ == '__main__':
    unittest.main()

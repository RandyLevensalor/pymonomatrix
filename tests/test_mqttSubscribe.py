import pytest
import sys
import os
sys.path.append(os.path.abspath('pymonomatrix'))

from unittest.mock import MagicMock, patch
import mqttSubscribe

class TestMqttSubscribe:
    def test_on_message_allowed_type(self):
        # Setup mock client, user data, and message
        mock_client = MagicMock()
        mock_msg = MagicMock()
        mock_msg.topic = "pymonomatrix/set/Index-volume"
        mock_msg.payload.decode.return_value = "50"

        mock_set_matrix = MagicMock()

        # Define an on_message capture variable
        on_message_func = None

        # We need to capture the nested on_message function
        def mock_subscribe(topic):
            pass

        mock_client.subscribe = mock_subscribe

        # Capture the assigned on_message handler
        def mock_on_message_setter(self, func):
            nonlocal on_message_func
            on_message_func = func

        type(mock_client).on_message = property(fset=mock_on_message_setter)

        # Call subscribe to bind our callback
        mqttSubscribe.subscribe(mock_client, "pymonomatrix/set/", mock_set_matrix)

        # Call the actual callback
        if on_message_func:
             on_message_func(mock_client, None, mock_msg)

        # Assert that the appropriate method was called on SetMatrix
        mock_set_matrix.set_volume.assert_called_once_with("Index", "50")

    def test_on_message_disallowed_type(self):
        # Setup mock client, user data, and message
        mock_client = MagicMock()
        mock_msg = MagicMock()
        mock_msg.topic = "pymonomatrix/set/Index-invalid_command"
        mock_msg.payload.decode.return_value = "exploit"

        mock_set_matrix = MagicMock()

        # Define an on_message capture variable
        on_message_func = None

        # Capture the assigned on_message handler
        def mock_on_message_setter(self, func):
            nonlocal on_message_func
            on_message_func = func

        type(mock_client).on_message = property(fset=mock_on_message_setter)

        # Call subscribe to bind our callback
        mqttSubscribe.subscribe(mock_client, "pymonomatrix/set/", mock_set_matrix)

        # Call the actual callback
        if on_message_func:
             on_message_func(mock_client, None, mock_msg)

        # Assert that NO method was called on SetMatrix
        mock_set_matrix.set_volume.assert_not_called()
        mock_set_matrix.set_video_output.assert_not_called()
        mock_set_matrix.set_audio_output.assert_not_called()
        # Ensure no unexpected attribute was accessed except the standard ones if any
        # Specifically, ensure getattr wasn't used dynamically in an exploitative way

        # We can test that the mock wasn't interacted with for "set_invalid_command"
        with pytest.raises(AssertionError):
            mock_set_matrix.set_invalid_command.assert_called()

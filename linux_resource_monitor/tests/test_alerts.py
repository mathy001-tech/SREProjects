import pytest
from unittest.mock import patch
import logging
from linux_resource_monitor.collector.alerts import send_slack_alert

# Create a test logger
test_logger = logging.getLogger("test_logger")

@patch('requests.post')
def test_send_slack_alert_success(mock_post):
    # Arrange: Mock successful HTTP response
    mock_post.return_value.status_code = 200

    # Act: Call your function with a fake webhook URL and test message
    send_slack_alert("http://fakeurl", "Test message", test_logger)

    # Assert: requests.post was called exactly once
    mock_post.assert_called_once()

@patch('requests.post')
def test_send_slack_alert_failure(mock_post, caplog):
    # Arrange: Mock a failing HTTP response
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Error"

    # Act: Capture logs and call the function
    with caplog.at_level(logging.ERROR):
        send_slack_alert("http://fakeurl", "Test message", test_logger)

    # Assert: Check that the error was logged
    assert "Slack alert failed with status 500" in caplog.text

import uuid

from unittest import mock
from messenger.models import Channel
from tests import factories


@mock.patch.object(uuid, "uuid4")
def test_generate_invite_code_succeeds(mock_uuid4):
    """
    Given: We are calling the method generate_invite_code without conflicts
    Expect: We are able to return a code
    """

    # Create the channel so we can call the generate code...
    channel_a = factories.Channel()

    # Mock uuid so we can assert it later down the line...
    mock_uuid4.return_value.hex = "abcdef1234567890"

    code = channel_a.generate_invite_code()

    # Asser that we are able to return a code...s
    assert code == "ABCDEF12"


@mock.patch.object(Channel, "_invite_code_exists", return_value=True)
@mock.patch.object(uuid, "uuid4")
def test_generate_invite_code_tries_ten_times(mock_uuid4, mock_invite_code_exists):
    """
    Given: That all generated code that was called already exists
    Expect: We stop at the 10th try and log it as critical
    """

    # Create the channel so we can call the generate code...
    channel_a = factories.Channel()

    with mock.patch("utils.logging.logger") as mock_logger:
        code = channel_a.generate_invite_code()

    # Asser that we have called the logger with the following parameters...
    mock_logger.critical.assert_called_once_with(
        msg="Channel was not able to generate an invite code",
        extra={"channel_id": channel_a.pk},
    )

    # And code returns an empty string
    assert code == ""

    # Assert that these functions are called 10 times before stopping
    assert mock_invite_code_exists.call_count == 10
    assert mock_uuid4.call_count == 10

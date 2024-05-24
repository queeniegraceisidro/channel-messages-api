from messenger.models import Channel
from tests import factories


def test_invite_code_exists_when_it_does_not_exists():
    """
    Given: We are calling the static method _invite_code_exists without conflicts
    Expect: The function returns False
    """
    assert Channel._invite_code_exists("ABCDE") is False


def test_invite_code_exists_when_it_exists():
    """
    Given: We are calling the static method _invite_code_exists with conflicts
    Expect: The function returns True
    """

    # Create the channel that will conflict to what we will pass
    factories.Channel(invite_code="ABCDE")
    assert Channel._invite_code_exists("ABCDE") is True

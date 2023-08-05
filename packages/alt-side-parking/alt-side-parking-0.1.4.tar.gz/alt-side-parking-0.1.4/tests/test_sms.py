from automock import get_mock
from alt_side_parking.sms import (
    normalize_number,
    send_reminder,
)


def test_send_reminder():
    send_reminder()
    mock = get_mock("alt_side_parking.sms.get_client")
    assert mock().api.account.messages.create.called_with(
        to="+13472344323",
        from_="12123452342",
        body="Move your car my guy",
    )


def test_normalize_number():
    number = normalize_number("+13472344323")
    assert "+13472344323" == number
    other_number = normalize_number("+1347-234-4323")
    assert number == other_number

import phonenumbers
from twilio.rest import Client

from .config import (
    MOBILE,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_NUMBER,
)


REMINDER_TEXT = "Move your car my guy"


def send_reminder() -> None:
    client = get_client()
    personal_number = normalize_number(MOBILE)
    twilio_number = normalize_number(TWILIO_NUMBER)
    client.api.account.messages.create(
        to=personal_number,
        from_=twilio_number,
        body=REMINDER_TEXT,
    )


def get_client() -> Client:
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def normalize_number(mobile_number: str) -> str:
    return phonenumbers.format_number(
        phonenumbers.parse(mobile_number, None),
        phonenumbers.PhoneNumberFormat.E164,
    )

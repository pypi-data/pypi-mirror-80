from .feed import is_suspended_today
from .sms import send_reminder

remind_me = send_reminder


def we_not_good() -> bool:
    return not is_suspended_today()

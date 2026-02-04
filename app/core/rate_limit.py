from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

RATE_LIMITS = {
    "auth_register": "3/minute",
    "auth_login": "3/minute",
    "auth_logout": "3/minute",
    "user_password": "5/minute",
    "user_username": "5/minute",
    "user_subscription": "5/minute",
    "user_delete": "5/minute",
    "newsletter_send": "10/minute",
}

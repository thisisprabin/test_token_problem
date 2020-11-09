import datetime
from django.utils import timezone
from utils.constants import (
    TOKEN_EXPIRE_LIMIT,
)
from uuid import UUID


def get_expire_token_time(created_time):
    expire_time = created_time + datetime.timedelta(seconds=TOKEN_EXPIRE_LIMIT)
    return expire_time


def datetime_to_epoch(date_time):
    if date_time:
        date_time = int(date_time.timestamp() * 1000.0)
    return date_time


def get_timezone():
    return timezone.now()


def validate_uuid4(uuid_string):
    ack = False
    try:
        val = UUID(uuid_string, version=4)
        ack = True
    except ValueError:
        ack = False
    return ack

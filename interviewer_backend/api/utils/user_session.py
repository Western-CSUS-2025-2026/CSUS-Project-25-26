import datetime

from api.settings import get_settings


settings = get_settings()


def calc_session_expire_date():
    return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=settings.SESSION_TIME_IN_DAYS)

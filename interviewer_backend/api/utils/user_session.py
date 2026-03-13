import datetime

from api.settings import get_settings


settings = get_settings()


def calc_session_expire_date(now: datetime.datetime | None = None):
    base_time = now or datetime.datetime.now(tz=datetime.timezone.utc)
    return base_time + datetime.timedelta(days=settings.SESSION_TIME_IN_DAYS)

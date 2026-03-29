import datetime
from typing import Type


class APIError(Exception):
    msg: str

    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class ObjectNotFound(APIError):
    def __init__(self, obj: type, obj_id_or_name: int | str):
        super().__init__(
            f"Object {obj.__name__} {obj_id_or_name=} not found",
        )


class AlreadyExists(APIError):
    def __init__(self, obj: type, obj_id_or_name: int | str):
        super().__init__(
            f"Object {obj.__name__}, {obj_id_or_name=} already exists",
        )


class ForbiddenAction(APIError):
    def __init__(self, type: Type):
        super().__init__(f"Forbidden action with {type.__name__}")


class TooManyEmailRequests(APIError):
    delay_time: datetime.timedelta

    def __init__(self, dtime: datetime.timedelta):
        self.delay_time = dtime
        super().__init__(
            f'Too many email requests. Delay: {dtime}',
        )


class RegistrationIncomplete(APIError):
    def __init__(self):
        super().__init__(f"User registration wasn't complete")


class AuthFailed(APIError):
    def __init__(self, error_msg: str):
        super().__init__(error_msg)


class FailToConnectTwelveLabs(APIError):
    def __init__(self, error_msg: str = "Failed to connect TwelveLabs API"):
        super().__init__(error_msg)


class IndexCreatingFail(APIError):
    def __init__(self, error_msg: str = "Failed to create an index"):
        super().__init__(error_msg)


class FailToCreateTask(APIError):
    def __init__(self, error_msg: str = "Failed to create task"):
        super().__init__(error_msg)


class FailToParseAnalysis(APIError):
    def __init__(self, error_msg: str = "Failed to to parse analysis"):
        super().__init__(error_msg)

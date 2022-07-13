from dataclasses import dataclass

from exception.error_response_exception import ErrorResponseException


@dataclass
class UsernamePasswordException(ErrorResponseException):

    def __init__(self) -> None:
        super().__init__("Wrong username or password!", 403)

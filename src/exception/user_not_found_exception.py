from dataclasses import dataclass

from exception.error_response_exception import ErrorResponseException


@dataclass
class UserNotFoundException(ErrorResponseException):

    def __init__(self) -> None:
        super().__init__(f"User not found!", 404)

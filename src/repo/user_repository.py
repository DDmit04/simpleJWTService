from exception.user_not_found_exception import UserNotFoundException
from model.user import User


class UserRepository:

    def __init__(self, user_bunk: list[User]) -> None:
        super().__init__()
        self.user_bank = user_bunk

    def get_user_by_id(self, user_id) -> User:
        for user in self.user_bank:
            if user.id == user_id:
                return user
        raise UserNotFoundException()

    def get_user_by_uuid(self, user_uuid) -> User:
        for user in self.user_bank:
            if user.uuid == user_uuid:
                return user
        raise UserNotFoundException()

    def find_by_username(self, username) -> User:
        for user in self.user_bank:
            if user.username == username:
                return user
        raise UserNotFoundException()

    def update_user_uuid(self, user_id, uuid: str):
        for user in self.user_bank:
            if user.id == user_id:
                user.uuid = uuid
                return user

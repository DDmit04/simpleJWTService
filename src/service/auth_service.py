import uuid

from exception.username_password_exception import UsernamePasswordException
from model.token_auth_data import TokenAuthData
from repo.user_repository import UserRepository
from service.jwt_service import JwtService


class AuthService:

    def __init__(self,
                 user_repository: UserRepository,
                 jwt_service: JwtService):
        super().__init__()
        self.jwt_service = jwt_service
        self.user_repository = user_repository

    def auth_user(self, username, given_password) -> TokenAuthData:
        user = self.user_repository.find_by_username(username)
        user_password = user.password
        if given_password == user_password:
            return self.__gen_tokens_for_user(user)
        raise UsernamePasswordException()

    def logout(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if user is not None:
            new_uuid = uuid.uuid4().hex
            self.user_repository.update_user_uuid(user_id, new_uuid)
            return True
        return False

    def refresh_tokens(self, user_uuid):
        user = self.user_repository.get_user_by_uuid(user_uuid)
        return self.__gen_tokens_for_user(user)

    def __gen_tokens_for_user(self, user):
        user_id = user.id
        jwt_token = self.jwt_service.gen_jwt_token(user_id)
        refresh_token = self.jwt_service.gen_refresh_token(user.uuid)
        return TokenAuthData(jwt_token, refresh_token)
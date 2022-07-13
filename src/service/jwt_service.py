import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, \
    decode_token


class JwtService:

    def __init__(self, jwt_time: datetime, refresh_time: datetime,
                 secret: str):
        super().__init__()
        self.jwt_time = datetime.timedelta(seconds=jwt_time)
        self.refresh_time = datetime.timedelta(seconds=refresh_time)
        self.secret = secret

    def gen_jwt_token(self, user_id: int):
        return create_access_token(user_id, expires_delta=self.jwt_time)

    def gen_refresh_token(self, base_uuid: str):
        return create_refresh_token(base_uuid, expires_delta=self.refresh_time)

    def get_token_subject(self, token):
        decoded_token = decode_token(token)
        return decoded_token['sub']

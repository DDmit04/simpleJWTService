import os
import uuid
from datetime import timedelta

import humanfriendly
from flask import Flask
from werkzeug.security import generate_password_hash

from model.user import User
from repo.user_repository import UserRepository
from service.auth_service import AuthService
from service.jwt_service import JwtService


class DependencyInjector:

    def __init__(self):
        super().__init__()
        self.user_bunk = None

    def get_config(self):
        base_username = os.environ.get("BASE_USER_NAME", 'user')
        base_password = os.environ.get("BASE_USER_PASSWORD", 'pswd')
        base_id = os.environ.get("BASE_USER_ID", 1)
        jwt_lifetime = humanfriendly.parse_timespan(
            os.environ.get("JWT_LIFETIME_SECONDS", '15m')
        )
        refresh_lifetime = humanfriendly.parse_timespan(
            os.environ.get("REFRESH_LIFETIME_SECONDS", '7d')
        )
        jwt_Secret = os.environ.get('JWT_SECRET', '')
        return {
            "USER_ID": base_id,
            "USERNAME": base_username,
            "PASSWORD": base_password,
            "JWT_LIFETIME_SECONDS": jwt_lifetime,
            "REFRESH_LIFETIME_SECONDS": refresh_lifetime,
            "JWT_SECRET": jwt_Secret
        }

    def get_user_bunk(self):
        if self.user_bunk is None:
            config = self.get_config()
            user_id = config['USER_ID']
            username = config['USERNAME']
            password = generate_password_hash(config['PASSWORD'])
            user_uuid = uuid.uuid4().hex
            user = User(user_id, username, password, user_uuid)
            self.user_bunk = [user]
        return self.user_bunk

    def get_user_repo(self):
        user_bunk = self.get_user_bunk()
        return UserRepository(user_bunk)

    def get_jwt_service(self) -> JwtService:
        config = self.get_config()
        jwt_time = config['JWT_LIFETIME_SECONDS']
        refresh_time = config['REFRESH_LIFETIME_SECONDS']
        secret = config['JWT_SECRET']
        return JwtService(jwt_time, refresh_time, secret)

    def get_user_auth_service(self) -> AuthService:
        jwt_service = self.get_jwt_service()
        user_repo = self.get_user_repo()
        return AuthService(user_repo, jwt_service)

    def get_app(self):
        config = self.get_config()
        app = Flask(__name__)
        app.config["JWT_SECRET_KEY"] = config['JWT_SECRET']
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = \
            timedelta(seconds=config['JWT_LIFETIME_SECONDS'])
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = \
            timedelta(seconds=config['REFRESH_LIFETIME_SECONDS'])
        return app

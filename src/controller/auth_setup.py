from flask import Response
from flask_httpauth import HTTPBasicAuth

from exception.username_password_exception import UsernamePasswordException
from injector.dependency_container import di_container

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, given_password):
    user_auth_service = di_container.get_user_auth_service()
    try:
        username = user_auth_service.auth_user(username, given_password)
    except UsernamePasswordException:
        return Response(status=403)
    return username

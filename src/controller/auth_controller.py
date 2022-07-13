from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from controller.auth_setup import auth
from injector.dependency_container import di_container

auth_controller_blueprint = Blueprint('auth', __name__)


@auth_controller_blueprint.route('/login', methods=["POST"])
@auth.login_required
def login():
    auth_service = di_container.get_user_auth_service()
    tokens = auth_service.get_tokens(auth.current_user())
    return jsonify(tokens)


@auth_controller_blueprint.route('/logout', methods=["GET"])
@jwt_required()
def logout():
    auth_service = di_container.get_user_auth_service()
    user_id = get_jwt_identity()
    success = auth_service.logout(user_id)
    if success:
        return Response(status=200)
    return Response(status=403)


@auth_controller_blueprint.route('/ref', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    auth_service = di_container.get_user_auth_service()
    user_uuid = get_jwt_identity()
    tokens = auth_service.refresh_tokens(user_uuid)
    return jsonify(tokens)

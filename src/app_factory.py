from flask import jsonify, make_response, Flask
from jsonschema.exceptions import ValidationError

from controller.auth_controller import auth_controller_blueprint


def setup_app(app: Flask) -> Flask:
    app.register_blueprint(auth_controller_blueprint,
                           url_prefix='/auth')

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return make_response(jsonify(
                {'error': original_error.message}),
                400)
        return error

    return app

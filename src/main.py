from flask_jwt_extended import JWTManager

from app_factory import setup_app
from injector.dependency_container import di_container

app = di_container.get_app()
jwt = JWTManager(app)
app = setup_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

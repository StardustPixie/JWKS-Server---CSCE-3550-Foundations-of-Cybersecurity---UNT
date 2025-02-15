from flask import Flask
def create_app():
    app = Flask(__name__)

    from .key_utils import generate_key_pair  
    generate_key_pair()

    from app.routes import jwks_blueprint, auth_blueprint
    app.register_blueprint(jwks_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
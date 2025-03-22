from flask import Flask
import time
import key_utils
import database
from routes import jwks_blueprint, auth_blueprint

def create_app():
    app = Flask(__name__)

    #DB is initilizaed and ensures that the keys table exists
    database.init_db()

    if not database.get_all_valid_keys():
        key_utils.generate_and_store_key(expiry=int(time.time()) + 3600)
        key_utils.generate_and_store_key(expiry=int(time.time()) - 3600)

    #Here is where the route handlers are registered
    app.register_blueprint(jwks_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

from flask import Blueprint, jsonify, request
from app.key_utils import keys, generate_key_pair
from app.jwt_utils import create_jwt
import time
import base64
from cryptography.hazmat.primitives import serialization

jwks_blueprint = Blueprint('jwks', __name__)
auth_blueprint = Blueprint('auth', __name__)

@jwks_blueprint.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    jwks_keys = []
    for kid, key_info in keys.items():
        if key_info['expiry'] > time.time():
            public_key = key_info['public_key']
            public_numbers = public_key.public_numbers()

            n_bytes = public_numbers.n.to_bytes(256, byteorder='big')
            e_bytes = public_numbers.e.to_bytes(3, byteorder='big')
            
            n_b64 = base64.urlsafe_b64encode(n_bytes).decode('utf-8').rstrip('=')
            e_b64 = base64.urlsafe_b64encode(e_bytes).decode('utf-8').rstrip('=')
            
            jwks_keys.append({
                'kid': kid,
                'kty': 'RSA',
                'alg': 'RS256',
                'use': 'sig',
                'n': n_b64,
                'e': e_b64
            })
    return jsonify({'keys': jwks_keys}), 200

@auth_blueprint.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', '').lower() == 'true'
    kid, private_key, _, expiry = generate_key_pair()
    if expired:
        expiry = int(time.time()) - 3600  
        keys[kid]['expiry'] = expiry

    payload = {
        'sub': '1234567890',
        'name': 'John Doe',
        'iat': int(time.time()),
        'exp': expiry
    }
    token = create_jwt(payload, private_key, kid)
    return jsonify({'token': token}), 200
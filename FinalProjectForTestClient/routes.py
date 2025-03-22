from flask import Blueprint, jsonify, request
import time
import base64
from cryptography.hazmat.primitives import serialization
import database
from jwt_utils import create_jwt
from key_utils import generate_and_store_key


jwks_blueprint = Blueprint('jwks', __name__)
auth_blueprint = Blueprint('auth', __name__)

@jwks_blueprint.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    jwks_keys = []
    rows = database.get_all_valid_keys()  
    for row in rows:
        kid_str = str(row['kid'])
        private_key = serialization.load_pem_private_key(row['key'], password=None)
        public_key = private_key.public_key()
        public_numbers = public_key.public_numbers()

        n_bytes = public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, byteorder='big')
        e_bytes = public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, byteorder='big')

        #This line shows public key parameters being decoded (n,e) into base64 for the JWKS server
        n_b64 = base64.urlsafe_b64encode(n_bytes).decode('utf-8').rstrip('=')
        e_b64 = base64.urlsafe_b64encode(e_bytes).decode('utf-8').rstrip('=')
        
        jwks_keys.append({
            'kid': kid_str,  
            'kty': 'RSA',
            'alg': 'RS256',
            'use': 'sig',
            'n': n_b64,
            'e': e_b64
        })
    return jsonify({'keys': jwks_keys}), 200

@auth_blueprint.route('/auth', methods=['POST'])
def auth():
    #This line checks if the client is requesting a JWT with an expired key
    expired = request.args.get('expired', '').lower() == 'true'
    row = database.get_key(expired=expired)
    
    if row is None:
        if expired:
            exp = int(time.time()) - 3600  
        else:
            exp = int(time.time()) + 3600 
        kid, private_key, exp = generate_and_store_key(expiry=exp)
    else:
        kid = str(row['kid'])  
        exp = row['exp']
        key_data = row['key']
        if not isinstance(key_data, bytes):
            key_data = bytes(key_data)
        private_key = serialization.load_pem_private_key(key_data, password=None)

    payload = {
        'sub': '1234567890',
        'name': 'John Doe',
        'iat': int(time.time()),
        'exp': exp
    }
    token = create_jwt(payload, private_key, kid)
    return jsonify({'token': token}), 200

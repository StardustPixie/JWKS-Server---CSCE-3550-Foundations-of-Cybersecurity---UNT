from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import time
import uuid

keys = {}

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    kid = str(uuid.uuid4())
    expiry = int(time.time()) + 3600 
    keys[kid] = {
        'private_key': private_key,
        'public_key': public_key,
        'expiry': expiry
    }
    return kid, private_key, public_key, expiry
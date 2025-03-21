from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import time
from database import insert_key

def generate_and_store_key(expiry=None):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    if expiry is None:
        expiry = int(time.time()) + 3600
    kid = insert_key(private_key, expiry)
    return kid, private_key, expiry

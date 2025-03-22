from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import time
from database import insert_key

def generate_and_store_key(expiry=None):
    """
    Generates a new RSA key pair and stores the private key within the DB
    """
    #Here is where the 2048 bit RSA key pair is generated
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    if expiry is None:
        expiry = int(time.time()) + 3600
    #Key is now stored in the SQLite DB and retrieve the assigned ID/kid
    kid = insert_key(private_key, expiry)
    return kid, private_key, expiry

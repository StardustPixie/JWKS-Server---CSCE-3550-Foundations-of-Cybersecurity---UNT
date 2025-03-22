import jwt

def create_jwt(payload, private_key, kid):
    """
    Creates a JSON Web Token signed with the provided RSA private key
    """
    token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': str(kid)})
    return token

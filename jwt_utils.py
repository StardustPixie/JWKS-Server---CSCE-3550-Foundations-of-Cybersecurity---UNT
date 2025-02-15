import jwt

def create_jwt(payload, private_key, kid):
    token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': kid})
    return token
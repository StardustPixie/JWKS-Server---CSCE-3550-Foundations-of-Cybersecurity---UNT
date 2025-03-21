# JWKS Server (JSON Web Key Set)
A lightweight RESTful server for generating and serving JSON Web Keys (JWKS) to verify JWTs, with built-in mock authentication and key expiration support.


## Features
- RSA key pair generation with unique `kid` and expiry.
- `/.well-known/jwks.json` endpoint returns valid public keys.
- `/auth` issues signed JWTs (including expired ones via query).
- SQLite database used for persistent key storage.


# Environment Setup
python -m venv venv
venv\Scripts\activate   # Windows


# Install Dependencies
pip install -r requirements.txt


# Run Server
--Navigate to project directory
python run.py


# Tests
coverage run -m unittest discover -s . -p "test_*.py"
coverage report -m


# Example Output
test_auth_endpoint         ... ok
test_expired_auth_endpoint ... ok
test_jwks_endpoint         ... ok

Ran 3 tests in 0.1s
OK



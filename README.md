# JWKS-Server---CSCE-3550-Foundations-of-Cybersecurity---UNT

# JWKS Server for JWT Key Management

A RESTful server that generates and serves JSON Web Key Sets (JWKS) for verifying JWTs, with support for key expiry and mock authentication.

## Features
- Generates RSA key pairs with unique Key IDs (`kid`) and expiry times.
- `/jwks` endpoint to retrieve valid public keys.
- `/auth` endpoint to issue JWTs (optionally signed with expired keys).


## Setup & Run

1. **Clone the Repository (bash)**
   -git clone https://github.com/your-username/your-repo.git
   -cd your-repo

2. **Create a Virtual Environment**
-python -m venv venv
-source venv/bin/activate  # macOS/Linux
-venv\Scripts\activate     # Windows

3. **Install Dependencies**
-pip install -r requirements.txt

4. **Run the Server**
-python run.py

5. **Get Valid Public Keys**
-curl -X GET http://localhost:8080/jwks

6. **Get a Valid JWT**
-curl -X POST http://localhost:8080/auth

7. **Get Expired JWT**
-curl -X POST http://localhost:8080/auth?expired=true

8. **Testing**
-pip install coverage
-pip install requests
-pip freeze > requirements.txt

   8a. **Open a new terminal after python run.py**
    -python -m unittest discover -s tests -p "test_*.py" -v
    -pip install coverage
    -coverage run -m unittest discover -s tests -p "test_*.py"
    -coverage report -m 

**Output**
test_auth_endpoint (test_server.TestJWKSServer) ... ok
test_expired_auth_endpoint (test_server.TestJWKSServer) ... ok
test_jwks_endpoint (test_server.TestJWKSServer) ... ok
 -----------------------

Ran 3 tests in 0.1s
OK

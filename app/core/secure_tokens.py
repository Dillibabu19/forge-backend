import hashlib
import secrets

def generate_secure_token(length=64):
    return secrets.token_urlsafe(length)

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


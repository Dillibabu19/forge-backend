from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def _normalize_password(password: str) -> bytes:
    """
    Normalize password for bcrypt:
    - UTF-8 encode
    - If >72 bytes, pre-hash with SHA-256
    """
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        password_bytes = hashlib.sha256(password_bytes).digest()

    return password_bytes

def hash_password(password: str) -> str:
    normalized = _normalize_password(password)
    return pwd_context.hash(normalized)

def verify_password(password: str, hashed_password: str) -> bool:
    normalized = _normalize_password(password)
    return pwd_context.verify(normalized, hashed_password)


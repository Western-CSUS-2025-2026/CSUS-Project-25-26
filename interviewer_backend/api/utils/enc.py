import hashlib


def hash_password(password: str, salt: str) -> str:
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str, salt: str) -> bool:
    return hash_password(password, salt) == hashed_password

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Single source of truth for password length limits — imported by schemas.
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

ph = PasswordHasher()

def hash_password(plain_password: str) -> str:
    return ph.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


def validate_password_strength(value: str) -> str:
    """Password policy: composition rules beyond raw length. Raises
    ValueError (Pydantic turns it into a 422 detail)."""
    value = value.strip()
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one number")
    return value

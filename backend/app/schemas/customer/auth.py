from typing import Annotated
import re

from pydantic import BaseModel, EmailStr, Field, field_validator, AfterValidator

from ...core.security import (
    validate_password_strength,
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
)

# Password policy defined exactly once: length limits come from constants in
# core/security/passwords.py, composition rules from validate_password_strength.
StrongPassword = Annotated[
    str,
    Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH),
    AfterValidator(validate_password_strength),
]

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")


class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(
                        ...,
                        min_length=3,
                        max_length=10,
                        description="Username (3-10 chars, letters/numbers/underscores only"
                        )
    password: StrongPassword


    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if not USERNAME_PATTERN.fullmatch(value):
            raise ValueError("Username can only contain letters, numbers and underscores")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    # Optional: the refresh token normally arrives in an HttpOnly cookie.
    # A body value is accepted as a fallback (tests, non-browser clients).
    refresh_token: str | None = Field(None, min_length=1, description="Refresh token (fallback when no cookie is present)")


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1, description="Single-use reset token from the email link")
    password: StrongPassword


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool

    model_config = {"from_attributes": True}
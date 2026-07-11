from pydantic import BaseModel, EmailStr, Field, field_validator
import re

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(
                        ...,
                        min_length=3,
                        max_length=10,
                        description="Username (3-10 chars, letters/numbers/underscores only"
                        )
    password: str = Field(
                        ...,
                        min_length=8,
                        max_length=128,
                        description="Password (min 8 chars)"
                        )
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if not USERNAME_PATTERN.fullmatch(value):
            raise ValueError("Username can only contain letters, numbers and underscores")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        value = value.strip()
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        return value
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool

    model_config = {"from_attributes": True}
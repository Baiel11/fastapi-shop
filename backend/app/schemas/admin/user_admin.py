from pydantic import BaseModel
from datetime import datetime


class AdminUserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateUserStatus(BaseModel):
    is_active: bool


class UpdateUserRole(BaseModel):
    is_admin: bool

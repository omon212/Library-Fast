from pydantic import BaseModel
from app.users.models import UserRole


class RegisterSchema(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.USER


class LoginSchema(BaseModel):
    username: str
    password: str

from pydantic import BaseModel
from app.users.models import UserRole


class RegisterSchema(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.USER


class LoginSchema(BaseModel):
    username: str
    password: str


class LoginResponseSchema(BaseModel):
    message: str
    access_token: str


class RegisterResponseSchema(BaseModel):
    message: str


class UserGetSchema(BaseModel):
    id: int
    username: str
    role: UserRole

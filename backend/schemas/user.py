from pydantic import BaseModel
from datetime import datetime


class UserRegisterForm(BaseModel):
    username: str
    email: str
    password: str


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

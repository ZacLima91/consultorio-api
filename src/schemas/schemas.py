from pydantic import BaseModel
from typing import Optional, List


class UserList(BaseModel):
    username: str
    cpf: str
    laudos: Optional[List[str]] = None
    role: bool = True

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    cpf: str
    password: str
    laudos: Optional[List[str]] = None
    role: bool = True

    class Config:
        orm_mode = True


class LoginData(BaseModel):
    cpf: str
    password: str

    class Config:
        orm_mode = True


class LoginSuccess(BaseModel):
    access_token: str
    user: UserList

    class Config:
        orm_mode = True

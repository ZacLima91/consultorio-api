from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    email: Optional[str]
    cpf: str
    password: str
    laudos: Optional[List[str]] = None
    role: bool = True

    class Config:
        orm_mode = True

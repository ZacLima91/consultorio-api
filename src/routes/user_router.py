from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.config.database import get_db
from src.schemas.schemas import UserBase
from src.infra.sqlalchemy.repository.user import RepositoryUser


router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserBase,session: Session = Depends(get_db)):
    created_user = RepositoryUser(session).create_user(user)
    return created_user

@router.get("/user", status_code=status.HTTP_200_OK, response_model=List[UserBase])
async def get_all_users(session: Session = Depends(get_db)):
    users = await RepositoryUser.get_all_user()
    return users

@router.delete("/user", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, session: Session = Depends(get_db)):
    deleted_user = await RepositoryUser.delete_user(user_id)
    return deleted_user

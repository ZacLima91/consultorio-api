from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import ValidationError
from src.infra.sqlalchemy.config.database import get_db
from src.schemas.schemas import UserBase, UserList, LoginData
from src.infra.sqlalchemy.repository.user import RepositoryUser
from src.infra.providers.hash_provider import gerate_hash, verify_hash
from src.infra.providers.token_provider import verify_access_token, create_access_token
from src.routes.auth_utils import logged_in
from src.schemas.schemas import LoginSuccess, UserBase


router = APIRouter()


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED, response_model=UserList)
async def create_user(user: UserBase, logged_user: UserList = Depends(logged_in), session: Session = Depends(get_db)):
    if not logged_user.role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso negado. Função de usuário necessária.")
    try:
        # verifica se o usuario existe
        repository_user = RepositoryUser(session)
        user_exists = repository_user.get_by_cpf(user.cpf)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já cadastrado.")

        # cria user
        user.password = gerate_hash(user.password)
        created_user = RepositoryUser(session).create_user(user)
        return created_user

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/auth/sign", status_code=status.HTTP_200_OK)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    user = RepositoryUser(session).get_by_cpf(login_data.cpf)
    pwd = verify_hash(login_data.password, user.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não encontrado.")

    if not pwd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Senha inválida.")

    # Gerar Token JWT
    token = create_access_token({'sub': user.cpf, })

    return LoginSuccess(user=user, access_token=token)


@router.get("/auth/me", status_code=status.HTTP_200_OK, response_model=UserBase)
def get_user(logged_user: UserBase = Depends(logged_in)):
    return logged_user


@router.get("/all", response_model=List[UserBase])
def get_all(session: Session = Depends(get_db)):
    repository_user = RepositoryUser(session)
    users = repository_user.get_all_user()
    return users


@router.delete("/user", status_code=status.HTTP_200_OK, response_model=UserList)
async def delete_user(user_id: int, session: Session = Depends(get_db), logged_user: UserList = Depends(logged_in)):
    if not logged_user.role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso negado. Função de usuário necessária.")
    deleted_user = await RepositoryUser.delete_user(UserBase)
    return deleted_user

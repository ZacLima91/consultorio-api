from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import token_provider
from src.infra.sqlalchemy.repository.user import RepositoryUser
from src.schemas.schemas import UserList


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def logged_in(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> UserList:
    # decodificar o token
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')

    try:
        cpf = token_provider.verify_access_token(token)
    except JWTError:
        raise exception

    if not cpf:
        raise exception

    user = RepositoryUser(session).get_by_cpf(cpf)

    if not user:
        raise exception

    return user

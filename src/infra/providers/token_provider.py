import json
from datetime import datetime, timedelta
from jose import jwt
from typing import Union

# CONFIG
SECRET_KEY = 'Isaac92167497.'
ALGORITHM = 'HS256'
EXPIRES_AT = 3000


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=EXPIRES_AT)

    to_encode.update({'expires_at': expire.isoformat()})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):
    charge = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return charge.get('sub')

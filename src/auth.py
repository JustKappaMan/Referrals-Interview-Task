from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from exceptions import *
from database import fake_db, get_user
from models import TokenData, User, UserInDB
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def _get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[jwt.ALGORITHMS.HS256])
        if (username := payload.get("sub")) is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException

    if (user := get_user(fake_db, username=token_data.username)) is None:
        raise UnregisteredUserException

    return user


def create_access_token(data: dict, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode = data.copy() | {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=jwt.ALGORITHMS.HS256)
    return encoded_jwt


def authenticate_user(db: dict, username: str, password: str) -> UserInDB:
    if (user := get_user(db, username)) is None:
        raise UnregisteredUserException
    if not _verify_password(password, user.hashed_password):
        raise InvalidPasswordException
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(_get_current_user)]) -> User:
    if current_user.disabled:
        raise InactiveUserException
    return current_user

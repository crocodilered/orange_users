from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.db.repos import DbExistenceError
from app.db.repos.users import UsersRepo
from app.deps.db import get_repo
from app.models.users import User


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl='auth')),
    repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> User:
    ex = HTTPException(status_code=401, headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get('sub', '')
        user = await repo.retrieve_active_by_username(username)
        return user
    except (DbExistenceError, JWTError):
        raise ex

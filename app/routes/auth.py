from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config import JWT_EXPIRE_MINUTES
from app.db.repos import DbExistenceError
from app.db.repos.users import UsersRepo
from app.deps.auth import get_current_user
from app.deps.db import get_repo
from app.libs.auth import verify_password, create_access_token, hash_password
from app.models.users import User
from app.schemas.auth import AccessToken
from app.schemas.users import (UserInRetrieve, UserForUpdate,
                               UserForUpdatePassword)

router = APIRouter()


@router.post('', response_model=AccessToken)
async def authenticate_user(
    intake: OAuth2PasswordRequestForm = Depends(),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> AccessToken:
    ex = HTTPException(status_code=401, headers={'WWW-Authenticate': 'Bearer'})
    try:
        user = await users_repo.retrieve_active_by_username(intake.username)
    except DbExistenceError:
        raise ex

    if verify_password(intake.password, user.hashed_password) is False:
        raise ex

    access_token = create_access_token(
        user=user,
        expires_delta=timedelta(minutes=JWT_EXPIRE_MINUTES)
    )

    return AccessToken(access_token=access_token)


@router.get('/', response_model=UserInRetrieve)
async def retrieve_current_user(
    current_user: User = Depends(get_current_user),
) -> UserInRetrieve:
    return UserInRetrieve.cast(current_user)


@router.put('', response_model=UserInRetrieve)
async def update_current_user(
    intake: UserForUpdate,
    current_user: User = Depends(get_current_user),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> UserInRetrieve:
    params = intake.dict()
    params['hashed_password'] = current_user.hashed_password
    user = await users_repo.update(User(**params))
    return UserInRetrieve.cast(user)


@router.put('/~password', response_model=UserInRetrieve)
async def update_current_user_password(
    intake: UserForUpdatePassword,
    current_user: User = Depends(get_current_user),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> UserInRetrieve:
    if not verify_password(intake.current_password,
                           current_user.hashed_password):
        raise HTTPException(status_code=401)

    user = current_user.copy()
    user.hashed_password = hash_password(intake.new_password)
    user = await users_repo.update(user)

    return UserInRetrieve.cast(user)

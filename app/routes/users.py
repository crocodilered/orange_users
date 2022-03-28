from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.db.repos import DbExistenceError, DbUniqueError
from app.db.repos.users import UsersRepo
from app.deps.auth import get_current_user
from app.deps.db import get_repo
from app.libs.auth import hash_password
from app.models.users import User
from app.schemas.users import (UserInList, UserInRetrieve, UserForCreate,
                               UserForUpdate)

router = APIRouter()


@router.get('', response_model=List[UserInList])
async def list_users(
    offset: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> List[UserInList]:
    users = await users_repo.list(offset=offset, limit=limit)
    return [UserInList.cast(x) for x in users]


@router.post('', response_model=UserInRetrieve)
async def create_user(
    intake: UserForCreate,
    current_user: User = Depends(get_current_user),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> UserInRetrieve:
    params = intake.dict(exclude={'password'})
    params['hashed_password'] = hash_password(intake.password)

    try:
        user = await users_repo.create(User(**params))
    except DbUniqueError as e:
        raise HTTPException(status_code=400, detail=e)
    else:
        return UserInRetrieve.cast(user)


@router.put('/{user_pk}', response_model=UserInRetrieve)
async def update_user(
    user_pk: int,
    intake: UserForUpdate,
    current_user: User = Depends(get_current_user),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> UserInRetrieve:
    try:
        user = await users_repo.retrieve(user_pk)
    except DbExistenceError:
        raise HTTPException(status_code=404)
    else:
        params = user.dict()
        params.update(intake.dict())
        user = await users_repo.update(User(**params))
        return UserInRetrieve.cast(user)


@router.get('/{user_pk}', response_model=UserInRetrieve)
async def retrieve_user(
    user_pk: int,
    current_user: User = Depends(get_current_user),
    users_repo: UsersRepo = Depends(get_repo(UsersRepo)),
) -> UserInRetrieve:
    try:
        user = await users_repo.retrieve(user_pk)
    except DbExistenceError:
        raise HTTPException(status_code=404)
    else:
        return UserInRetrieve.cast(user)

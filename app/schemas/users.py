from app.schemas import BaseSchema


class UserInRetrieve(BaseSchema):
    pk: int
    username: str
    title: str
    phone: str
    email: str
    is_active: bool


class UserInList(BaseSchema):
    pk: int
    username: str
    title: str
    is_active: bool


class UserForCreate(BaseSchema):
    username: str
    password: str
    title: str
    phone: str
    email: str
    is_active: bool


class UserForUpdate(BaseSchema):
    pk: int
    username: str
    title: str
    phone: str
    email: str
    is_active: bool


class UserForUpdatePassword(BaseSchema):
    current_password: str
    new_password: str

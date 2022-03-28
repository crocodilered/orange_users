from app.models import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    title: str = ''
    phone: str = ''
    email: str = ''
    is_active: bool = False

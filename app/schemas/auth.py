from app.schemas import BaseSchema


class AccessToken(BaseSchema):
    access_token: str
    token_type: str = 'Bearer'

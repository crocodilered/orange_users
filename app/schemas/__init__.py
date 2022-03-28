from pydantic import BaseModel


class BaseSchema(BaseModel):
    @classmethod
    def cast(cls, model: BaseModel) -> 'BaseSchema':
        return cls(**model.dict())

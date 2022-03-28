from abc import ABC
from enum import Enum
from typing import Any, List, Optional

from asyncpg.connection import Connection
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.models import OrangeBaseModel


class DbErrorCode(Enum):
    ENTITY_EXISTENCE = 'entity-existence'
    UNIQUE_VIOLATION = 'unique-violation'
    FK_VIOLATION = 'fk-violation'


class DbBaseError(Exception):
    code: DbErrorCode
    message: str

    def __init__(self, message: Any = '') -> None:
        self.message = message

    def dict(self):
        return {
            'code': self.code.value,
            'message': str(self.message),
        }


class DbExistenceError(DbBaseError):
    """ Запрашиваемый / сохраняемый объект не существует """
    code = DbErrorCode.ENTITY_EXISTENCE


class DbUniqueError(DbBaseError):
    """ Нарушение уникальности поля """
    code = DbErrorCode.UNIQUE_VIOLATION


class DbFkError(DbBaseError):
    """ Нарушение ссылающегося (fk) поля """
    code = DbErrorCode.FK_VIOLATION


class BaseRepo(ABC):
    QUERIES = None
    MODEL = None

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def retrieve(self, pk: int) -> 'OrangeBaseModel':
        record = await self.QUERIES.retrieve(self.conn, pk=pk)
        if not record:
            raise DbExistenceError()
        else:
            return self.MODEL(**record)

    async def update(self, model: 'OrangeBaseModel') -> 'OrangeBaseModel':
        params = model.dict()
        record = await self.QUERIES.update(self.conn, **params)
        if not record:
            raise DbExistenceError()
        else:
            return self.MODEL(**record)

    async def delete(self, pk: int) -> None:
        record = await self.QUERIES.delete(self.conn, pk=pk)
        if not record:
            raise DbExistenceError()

    async def list(
        self,
        *,
        offset: Optional[int] = 0,
        limit: Optional[int] = 0
    ) -> List['OrangeBaseModel']:
        records = await self.QUERIES.list(self.conn, offset=offset, limit=limit)
        return [self.MODEL(**x) for x in records]

    async def create(self, model: 'OrangeBaseModel') -> 'OrangeBaseModel':
        params = model.dict()
        try:
            record = await self.QUERIES.create(self.conn, **params)
        except UniqueViolationError as e:
            raise DbUniqueError(e) from e
        except ForeignKeyViolationError as e:
            raise DbFkError(e) from e
        else:
            return self.MODEL(**record)

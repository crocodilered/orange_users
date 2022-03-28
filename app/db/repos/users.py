from app.db import queries
from app.db.repos import BaseRepo, DbExistenceError
from app.models.users import User


class UsersRepo(BaseRepo):
    QUERIES = queries.users
    MODEL = User

    async def retrieve_active_by_username(self, username: str) -> User:
        record = await self.QUERIES.retrieve_active_by_username(
            self.conn,
            username=username
        )
        if not record:
            raise DbExistenceError()
        else:
            return User(**record)

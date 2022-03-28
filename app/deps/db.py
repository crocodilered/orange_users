import json
from typing import AsyncGenerator, Callable, Type

from asyncpg.connection import Connection
from asyncpg.pool import Pool
from fastapi import Depends
from starlette.requests import Request

from app.db.repos import BaseRepo


def get_pool(request: Request) -> Pool:
    return request.app.state.pool


async def get_conn(
    pool: Pool = Depends(get_pool)
) -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        await conn.set_type_codec(
            'json',
            schema='pg_catalog',
            encoder=json.dumps,
            decoder=json.loads
        )
        yield conn


def get_repo(repo_type: Type[BaseRepo]) -> Callable[[Connection], BaseRepo]:
    def func(conn: Connection = Depends(get_conn)) -> BaseRepo:
        return repo_type(conn)
    return func

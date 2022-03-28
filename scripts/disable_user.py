"""
Скрипт для деактивации пользователя
"""
import asyncio
import sys

from asyncpg.connection import Connection
from loguru import logger

from app.db import get_db_connection


def get_username() -> str:
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return ''


async def disable_user(conn: Connection, username: str) -> bool:
    row = await conn.fetchrow(
        'UPDATE users SET enabled=False WHERE username=$1 RETURNING pk',
        username
    )

    return row is not None


async def main() -> None:
    conn = await get_db_connection()

    username = get_username()

    if username == '':
        logger.error('Username cannot be empty')

    else:
        if await disable_user(conn, username):
            logger.info('User (username)=({}) disabled', username)
        else:
            logger.warning('User (username)=({}) does not exist', username)

    await conn.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

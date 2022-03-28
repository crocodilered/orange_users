"""
Скрипт для изменения пароля
"""
import asyncio
import sys
from typing import Tuple

from asyncpg.connection import Connection
from loguru import logger
from passlib.context import CryptContext

from app.db import get_db_connection


def get_password_hash(password):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.hash(password)


def get_username_and_password() -> Tuple[str, str]:
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        return '', ''


async def update_password(conn: Connection, username: str, password: str) -> bool:
    row = await conn.fetchrow(
        'UPDATE users SET password=$2 WHERE username=$1 RETURNING pk',
        username,
        get_password_hash(password)
    )
    return row is not None


async def main() -> None:
    conn = await get_db_connection()

    try:
        username, password = get_username_and_password()
        assert (username != '' and password != ''), 'Username (or password) cannot be empty'

        if await update_password(conn, username, password):
            logger.info('User\'s (username)=({}) password updated', username)
        else:
            logger.warning('User (username)=({}) does not exist', username)

    except AssertionError as e:
        logger.error(e)

    await conn.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

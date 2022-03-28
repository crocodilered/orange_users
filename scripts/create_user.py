"""
Скрипт для создания пользователя
python scripts/create_user.py {unit_pk} {username} {password}
"""
import asyncio
import sys
from typing import Tuple

from asyncpg.connection import Connection
from asyncpg.exceptions import UniqueViolationError
from loguru import logger
from passlib.context import CryptContext

from app.db import get_db_connection


def get_password_hash(password):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.hash(password)


def get_params() -> Tuple[int, str, str]:
    if len(sys.argv) == 4:
        return int(sys.argv[1]), sys.argv[2], sys.argv[3]
    else:
        return 0, '', ''


async def create_user(conn: Connection, unit_pk: str, username: str, password: str) -> None:
    await conn.execute('''
        INSERT INTO users (
            created, updated,
            unit_pk, username, password,
            phone, email,
            is_active
        ) VALUES (
            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
            $1, $2, $3,
            '', '',
            TRUE
        )
    ''', unit_pk, username, get_password_hash(password))


async def main() -> None:
    try:
        conn = await get_db_connection()

        unit_pk, username, password = get_params()

        if unit_pk == 0 or username == '' or password == '':
            logger.error('Username (or password or unit_pk) cannot be empty')
        else:
            await create_user(conn, unit_pk, username, password)
            logger.info('User (username)=({}) created', username)

        await conn.close()

    except UniqueViolationError as e:
        if e.constraint_name == 'users_unique_username':
            logger.error('User (username)=({}) already exists', username)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

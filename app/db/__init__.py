import pathlib

import aiosql
import asyncpg
from asyncpg.connection import Connection
from asyncpg.exceptions import InvalidPasswordError
from loguru import logger

from app.config import DB_URL

queries = aiosql.from_path(pathlib.Path(__file__).parent / 'sql', 'asyncpg')


async def get_db_connection() -> Connection:
    if not DB_URL:
        logger.critical('DB_URL config variable is not defined')
        exit(1)

    try:
        return await asyncpg.connect(DB_URL)

    except (ConnectionRefusedError, InvalidPasswordError) as e:
        logger.critical(f'Cannot connect to database with error: {e}')
        exit(2)

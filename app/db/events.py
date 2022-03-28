import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.config import DB_URL, DB_MAX_POOL_SIZE, DB_MIN_POOL_SIZE


async def connect_to_db(app: FastAPI) -> None:
    # see https://github.com/MagicStack/asyncpg/issues/875
    app.state.pool = await asyncpg.create_pool(
        DB_URL,
        min_size=DB_MIN_POOL_SIZE,
        max_size=DB_MAX_POOL_SIZE,
        server_settings={'jit': 'off'}
    )
    logger.info('Connected to database.')


async def close_db_connection(app: FastAPI) -> None:
    await app.state.pool.close()

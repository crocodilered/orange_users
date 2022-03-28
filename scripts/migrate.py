"""
Скрипт для накатывания миграций в БД.
Файлы с sql кладем в ./scripts/*.sql таким образом, чтобы они были отсортированы в том же порядке,
в каком их необходимо выполнять.
"""
import asyncio
from pathlib import Path
from typing import Optional

from asyncpg.connection import Connection
from loguru import logger

from app.db import get_db_connection


async def init_db(conn: Connection) -> None:
    """ Create migrations table if needed """
    row = await conn.fetchrow('''
        SELECT EXISTS (
            SELECT FROM information_schema.tables WHERE 
                table_schema = 'public' AND
                table_name = 'migrations'
        ) AS migrations_table_exists
    ''')

    if row['migrations_table_exists'] is False:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                filename TEXT NOT NULL,
                executed TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (filename)
            )
        ''')


async def get_last_migration_filename(conn: Connection) -> Optional[str]:
    row = await conn.fetchrow('''
        SELECT filename 
        FROM migrations 
        ORDER BY filename DESC 
        LIMIT 1
    ''')
    return None if row is None else row['filename']


async def run_migration(conn: Connection, filepath: Path) -> bool:
    with open(filepath, 'r', encoding='utf-8') as f:
        # Remove comments and empty lines
        effective_scripts = ''.join(
            [x for x in f if x[:2] != '--' and x.strip() != '']
        )
        scripts = [x for x in effective_scripts.split(';') if x.strip()]

    async with conn.transaction():
        try:
            for i, script in enumerate(scripts):
                await conn.execute(script)
        except Exception as e:
            logger.error('Migration filename={} raises exception: {}', filepath, e)
            logger.info('Migration filename={} rolled back', filepath)
            return False
        else:
            await conn.execute('''
                INSERT INTO migrations (filename, executed) 
                VALUES ($1, CURRENT_TIMESTAMP)
            ''', filepath.name)
            logger.info('Migration filename={} done', filepath)
            return True


async def main() -> None:
    conn = await get_db_connection()

    await init_db(conn)

    last_migration_filename = await get_last_migration_filename(conn)
    can_run_migration = (last_migration_filename is None)
    migrations_files = sorted(Path('migrations').glob('*.sql'))
    migrations_count = 0

    logger.debug('Last migration in DB is {}', last_migration_filename)

    for filepath in migrations_files:
        if can_run_migration:
            if await run_migration(conn, filepath):
                migrations_count += 1
            else:
                break

        can_run_migration = can_run_migration or (filepath.name == last_migration_filename)

    if migrations_count == 0:
        logger.info('No migrations to run')
    else:
        logger.info('{} migrations ran', migrations_count)

    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())

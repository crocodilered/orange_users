import pytest
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repos.users import UsersRepo
from app.libs.auth import hash_password
from app.models.users import User
from tests.fake_pool import FakePool


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application
    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        app.state.pool = await FakePool.create_pool(app.state.pool)
        yield app


@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pool


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url='http://testserver',
        headers={'Content-Type': 'application/json'},
    ) as client:
        yield client


@pytest.fixture
def test_user_password() -> str:
    return 'test'


@pytest.fixture
async def test_user(pool: Pool, test_user_password: str) -> User:
    async with pool.acquire() as conn:
        user = User(
            username='test',
            hashed_password=hash_password(test_user_password),
            is_active=True,
        )
        return await UsersRepo(conn).create(user)

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, BasicAuth
from app.models.users import User

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_login(app: FastAPI, client: AsyncClient,
                     test_user: User, test_user_password):
    u, p = test_user.username, test_user_password
    response = await client.post(
        '/api/v1/auth',
        data={'username': u, 'password': p},
        headers={'Content-type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 200, response.json()
    j = response.json()
    assert j.get('access_token'), j.get('token_type')

from fastapi import APIRouter

from app.routes import auth, users

router = APIRouter()
router.include_router(auth.router, tags=['auth'], prefix='/v1/auth')
router.include_router(users.router, tags=['users'], prefix='/v1/users')

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings as Csc

config = Config('.env')

try:
    API_TITLE: str = config('API_TITLE')
    API_PREFIX: str = config('API_PREFIX')
    API_HOST: str = config('API_HOST')
    API_PORT: int = config('API_PORT', cast=int)
    API_DEBUG: bool = config('API_DEBUG', cast=bool)

    DB_URL: str = config('DB_URL')
    DB_MAX_POOL_SIZE: int = config('DB_MAX_POOL_SIZE', cast=int)
    DB_MIN_POOL_SIZE: int = config('DB_MAX_POOL_SIZE', cast=int)

    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM')
    JWT_EXPIRE_MINUTES: int = config('JWT_EXPIRE_MINUTES', cast=int)

    CORS_ALLOWED_HOSTS: Csc = config('CORS_ALLOWED_HOSTS', cast=Csc)
except KeyError as e:
    print(f'Got config error: {e}')
    exit(1)

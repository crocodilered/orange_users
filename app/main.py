import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import (API_HOST, API_PORT, API_DEBUG, API_PREFIX, API_TITLE,
                        CORS_ALLOWED_HOSTS)
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.routes import router


def get_application() -> FastAPI:
    ret = FastAPI(title=API_TITLE, debug=False)

    ret.add_middleware(
        CORSMiddleware,
        allow_origins=list(CORS_ALLOWED_HOSTS),
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    ret.add_event_handler('startup', create_start_app_handler(ret))
    ret.add_event_handler('shutdown', create_stop_app_handler(ret))

    ret.include_router(router, prefix=API_PREFIX)

    return ret


app = get_application()


if __name__ == '__main__':
    uvicorn.run('app.main:app', host=API_HOST, port=API_PORT, reload=API_DEBUG)

from fastapi import FastAPI

from provisionr.api import init_api
from provisionr.frontend import init_frontend


def create_app() -> FastAPI:
    app = FastAPI()
    init_api(app)
    init_frontend(app)
    return app

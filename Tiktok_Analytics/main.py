'''
Filename:main.py
Created Date:
Author:

Copyright (c) 2021 Henceforth
'''
from fastapi import FastAPI
import uvicorn

from .configs.config import (
    API_PREFIX, APP_NAME, APP_VERSION, IS_DEBUG, HOST, PORT)
from .configs.event_handlers import start_app_handler, stop_app_handler
from .api.router import api_router


def get_app() -> FastAPI:
    """ Create a new instance of FastAPI with appropriate Configuration and behavior
    Returns:
        FastAPI: A modified Fast API instance
    """
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    fast_app.include_router(api_router, prefix=API_PREFIX)
    # * Startup behavior
    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    # * Shutdown behavior
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    return fast_app


def main():
    """Execute the application
    """
    # Creating Modified FastAPI instance
    app: FastAPI = get_app()
    uvicorn.run(app,port=4211, log_level="info")
